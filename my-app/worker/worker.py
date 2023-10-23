from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy.sql import text
import os

worker_app = FastAPI()

worker_host = os.getenv("WORKER_HOST", "localhost")
psql_name = os.getenv("PSQL_NAME", "localhost")

SQLALCHEMY_DATABASE_URL = f"postgresql://myuser:mypassword@{psql_name}:5432/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Perform math

@worker_app.post("/execute_operation/")
def execute_operation(task_data: dict):
    task_id = task_data.get("task_id")
    db = SessionLocal()
    query = text(f"SELECT a, b, action FROM tasks WHERE id = :task_id")
    task_info = db.execute(query, {"task_id": task_id}).first()

    if not task_info:
        db.close()
        raise HTTPException(status_code=404, detail="Задача не найдена")

    a, b, action = task_info

    if action == "plus":
        result = a + b
    elif action == "minus":
        result = a - b
    elif action == "multiplication":
        result = a * b
    elif action == "division":
        result = a / b

    update_query = text(f"UPDATE tasks SET result = :result WHERE id = :task_id")
    db.execute(update_query, {"result": result, "task_id": task_id})
    db.commit()
    db.close()

    return {"result": result}



@worker_app.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(worker_app, host="0.0.0.0", port=5051)
