import os 
from time import sleep
from datetime import datetime 
from celery import Celery

# we need 2 redis :
# one for input tasks (broker), and onother for storing result(backend)
# but here we use only one (same) address (used one redis) for both broker and backend 
app = Celery("tasks" , broker="redis://localhost:6379" , backend="redis://localhost:6379")


@app.task
def hello_world():
    return "hellooooo worlddddd"


@app.task
def dummy_task():
    os.makedirs("./tmp/celery" , exist_ok=True)
    now = datetime.now().strftime("%m-%d-%Y")
    with open(f"./tmp/celery/task-{now}.txt" , "w") as f :
        f.write("HELLLLLOOOO")


@app.task
def dummy_2(name="me"):
    sleep(10)
    return f"hi {name}"


@app.task
def addfunc(num1 , num2):
    print("sum function")
    return num1 + num2





# how to use venv : (instead of using with main python)
# we use venv when we want to use a special version of libraries , other than original installed version in our system 

# 1) virtualenv -p python3.10.1 venv 
# 2) venv/Scripts/activate  -----> now we are in that virtual environment
# 3) pip install celery redis "fastapi[standard]"

