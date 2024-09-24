'''
REDIS list commands :
-----------------------------------------
LPUSH : adds a new element to the head of a list;
RPUSH : adds to the tail.
LPOP  : removes and returns an element from the head of a list; 
RPOP  : does the same but from the tails of a list. 
LLEN  : returns the length of a list.

'''

from flask import Flask , jsonify
import redis
import datetime

app = Flask(__name__)

new_redis_client = redis.Redis(host="localhost" , port=6379 , decode_responses=True , db=0)
user_id = "3434"


@app.route("/" , methods=["GET"])
def rate_limiter():
    
    now = datetime.datetime.now().timestamp()
    # اینجا تایم استمپ فعلی رو مخوایم ذخیره کنیم 
    # اگر از تابع ست استفاده کنیم هر بار تایم استمپ جدید اووررایت میشه
    # پس باید به لیست مون اپند کنیم ، تایم استمپ جدید رو 
    # APPEND item to redis list  : RPUSH
    new_redis_client.lpush(f"requests_list:{user_id}" , now )
    new_redis_client.ltrim(f"requests_list:{user_id}" , start=0 , end=5)
    new_redis_client.expire(f"requests_list:{user_id}" , time=60 , nx=True)
    len_list = new_redis_client.llen(f"requests_list:{user_id}") 
    x = new_redis_client.lrange(f"requests_list:{user_id}" , 0 , len_list )

    if len_list > 5 :
        return jsonify({"limit rate error " : "Request LIMIT EXCEEDED" })

    return jsonify({"request":f"{x}"})

if __name__ == "__main__" :
    app.run(debug=True)


