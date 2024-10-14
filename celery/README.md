
# Redis + Celery 

celery is used for tasks managements .
celery works with RabbitMQ by default



 <br>

### How to see redis content ? 
+ with ``` redis insight databases ``` 

redis is a database 
managing between microservices 

with celery we can manage tasks in redis

when we use celery ?
when a task is time consuming , we may get error 408 which means ```requestTimeout error ``` 
in this situation we use queue , to run proccesses and tasks in a asyncronous way . 


in our case , ai process like inferencing model and working with files may take time to send data into backend . 

celery is going to save data into redis . 
redis is only a database , but it is the celery that do all managemnets between microservices .

celery is going to save tasks in redis 

### we can use from celery as :
+ broker 
+ client 

# how to run :
## 1_ Launch a broker/backend

```
docker run --name myredis -p 6379:6379 -d redis
```

### 2_ before running functions in app.ipynb file we have to run celery container . and celery should be up for this task :

so , in venv : 
here we want to use from celery as a worker :

```
celery --app init_celery_tasks.py worker --loglevel=info

or

celery -A init_celery_tasks worker --pool=solo -l info --concurrency=1

or 

celery --app CELERY_FILENAME worker --concurrency=1 --loglevel=DEBUG

```
if it run correctly the output will be like this : 
```
--- ***** ----- 
-- ******* ---- 
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x143b105efe0
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
```
now redis module is ready to use from it in code .
here we can run app.ipynb file 

### 3_ now we can run app.ipynb 
<br>

# how to run api.py :
in venv : (venv/Scripts/activate)
``` 
fastapi dev api.py
```

