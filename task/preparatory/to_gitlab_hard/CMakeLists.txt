Project(TST_APP)

set(CMAKE_CXX_STANDARD 14)

add_executable(test_app main.cpp)

INSTALL( 
     TARGETS test_app
     RUNTIME DESTINATION bin
) 
