from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from init_celery_tasks import *
from redis import Redis
from redis.lock import Lock


# SERVER is : fastapi 
# WORKER is : celery
# BROKER is : redis

app2 = FastAPI()

redis_instance = Redis.from_url("redis://localhost:6379")
lock = Redis.lock(redis_instance , name="task_id")
REDIS_TASKKEY = "new-locking"



class TaskOutputs(BaseModel):
    id :str
    status : str



@app2.get("/start")
def start() -> TaskOutputs :  # -> means : output of this method is a type of TaskOutputs class
    out1 = dummy_2.delay()
    return TaskOutputs(id=out1.task_id , status=out1.status)


@app2.get("/check_status")
def stat(task_id) -> TaskOutputs :
    out2 = app.AsyncResult(task_id)
    return TaskOutputs(id=out2.task_id , status=out2.status)



@app2.get("/1task_start")
def locked_start() -> TaskOutputs :
    try:
        if not lock.acquire(blocking_timeout=4):
            raise HTTPException(status_code=500, detail="Could not acquire lock")
        task_id = redis_instance.get(REDIS_TASKKEY)
        if task_id is None or app.AsyncResult(task_id).ready():# no task was ever run, or the last task finished already
            out3 = dummy_task.delay()
            redis_instance.set(REDIS_TASKKEY, out3.task_id)
            return TaskOutputs(id=out3.task_id , status=out3.status)
        else:# the last task is still running!            
            raise HTTPException(status_code=400, detail="A task is already being executed")
    finally:
        lock.release()



@app2.get("/1task_status")    
def locked_status(task_id) -> TaskOutputs :
    task_id = task_id or redis_instance.get(REDIS_TASKKEY)
    if task_id is None:
        raise HTTPException(status_code=400, detail=f"Could not determine task {task_id}")
    out4 = app.AsyncResult(task_id)
    return TaskOutputs(id=out4.task_id , status=out4.status)



# how to run ?
# in venv : (venv/Scripts/activate)
# fastapi dev api.py

# then open this url http://127.0.0.1:8000 in postman 
# 