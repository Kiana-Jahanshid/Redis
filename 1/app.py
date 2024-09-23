import time
import json
from flask import Flask ,jsonify
import requests
import redis
import uvicorn
import http.client

# here we have 3 microservice :
# our api 
# used api 
# our redis docker

app = Flask(__name__)
r = redis.Redis(host="localhost" , port=6379 , decode_responses=True   )


@app.route("/" , methods=["GET"])
def women_casts():
    start = time.time()
    if r.get("money heist women") is not None : # first of all it will ckeck redis cache , if it was vailable in redis , it will cache data
         women_list = r.get("money heist women")
         print("hi")
    else : # if data was not in redis , read data from main database
        women_list = []
        for cast in range(1 , 29) :
            response =http.client.HTTPSConnection("project-heist-rahulv07.vercel.app"  )
            response.request("GET", f"/characters/{cast}")
            response = response.getresponse()
            data = response.read()
            data = data.decode("utf-8")
            data = json.loads(data)
            response.close()
            if data["gender"] == "Female" :
                women_list.append(data)
    
    women_list = json.dumps(women_list)
    r.set("money heist women" , women_list)
    end = time.time()
    duration = end - start
    print(duration)
    return women_list


if __name__ == "__main__":
    app.run(debug=True  )


# in first request , data will be cached from main database 
# BUT , AFTER SECOND TIME OF REQUESTING , it will be cached from redis cache

# in terminal :
# fastapi run api.py / or / uvicorn api:app
# 