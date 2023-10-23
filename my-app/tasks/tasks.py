from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests, os
from configparser import ConfigParser
import httpx
import asyncio

task_app = FastAPI()

worker_host = os.getenv("WORKER_HOST", "localhost")
psql_name = os.getenv("PSQL_NAME", "localhost")

SQLALCHEMY_DATABASE_URL = f"postgresql://myuser:mypassword@{psql_name}:5432/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
OpenSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TaskDataModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    a = Column(Integer)
    b = Column(Integer)
    action = Column(String)
    result = Column(Integer)

Base.metadata.create_all(bind=engine)

class TaskCreateDataModel(BaseModel):
    description: str
    a: int
    b: int
    action: str

# Create task

@task_app.post("/tasks/", response_model=dict)

def create_task(task: TaskCreateDataModel):
    db_task = TaskDataModel(
        description=task.description,
        a=task.a,
        b=task.b,
        action=task.action,

    )

    db = OpenSession()
    db.add(db_task)
    db.commit()
    task_id = db_task.id 
    response = requests.post(f"http://{worker_host}:5051/execute_operation/", json={"task_id": task_id})
    worker_result = response.json()
    db_task.result = worker_result["result"]
    db.commit()

    return {"task_id": db_task.id}


# Get task result

@task_app.get("/tasks/{task_id}/result", response_model=dict)
def get_task_result(task_id: int):
    db = OpenSession()
    task = db.query(TaskDataModel).filter(TaskDataModel.id == task_id).first()
    db.close()

    return {"result": task.result}


# Get tasks | try to use async

def get_db():
    db = OpenSession()
    try:
        yield db
    finally:
        db.close()

@task_app.get("/tasks/")
async def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TaskDataModel).offset(skip).limit(limit).all()
    return tasks


# Get task by id

class TaskResponse(BaseModel):
    id: int
    description: str
    a: int
    b: int
    action: str

@task_app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int):
    db = OpenSession()
    task = db.query(TaskCreateDataModel).filter(TaskCreateDataModel.id == task_id).first()
    db.close()

    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return TaskResponse(
        id=task.id,
        description=task.description,
        a=task.a,
        b=task.b,
        action=task.action
    )

# Delete task

@task_app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = OpenSession()
    task = db.query(TaskCreateDataModel).filter(TaskCreateDataModel.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    db.delete(task)
    db.commit()
    db.close()
    return {"message": f"Задача с идентификатором {task_id} удалена успешно"}


# add config for healthcheck

config = ConfigParser()
config.read("config.conf")

retry_interval = int(config.get("WorkerConnection", "retry_interval"))

if __name__ == "__main__":
    import uvicorn

    async def startup():
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.get(f"http://{worker_host}:5051/healthcheck")
                    response.raise_for_status()
                    print("Worker is healthy")
                    break
                except httpx.RequestError as exc:
                    print(f"Worker is not healthy: {exc}")
                    print(f"Retrying in {retry_interval} seconds")
                    await asyncio.sleep(retry_interval)

    @task_app.on_event("startup")
    async def on_startup():
        await startup()

    uvicorn.run(task_app, host="0.0.0.0", port=5050)