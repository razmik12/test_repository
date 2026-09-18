


# from test_celery import send_email,celery





# @app.post("/notification")
# async def send_message():
#     result = send_message.delay("hello_this_is_celery",queue="notification_queue")
#     return {
#         "id":result.id,
#         "status":result.status,
#     }


# @app.post("/emails")
# async def send_email():
#     result = send_email.delay("razmapian73@gmail.com",queue="email_queue")
#     return {
#         "id":result.id,
#         "status":result.status,
#     }





# @app.get("/emails/{task_id}")
# async def get_emails(task_id:str):
#     result = celery.AsyncResult(task_id)
    
    
#     return {
#         "id": result.id,
#         "status": result.status,
#         "data": result.result
#     }
    

# @app.get("/notification/{task_id}")
# async def get_message(task_id:str):
#     result = celery.AsyncResult(task_id)
    
    
#     return {
#         "id": result.id,
#         "status": result.status,
#         "data": result.result
#     }    

import asyncio
import json

from fastapi import FastAPI
from contextlib import asynccontextmanager  
from rabbitmq_test import connection_rabitmq,exchange_message,send_message 
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

    
async def consume(consumer):
    async for message in consumer:
        print(message.value)




@asynccontextmanager
async def lifespan(app:FastAPI):
    connection = await connection_rabitmq(url="amqp://guest:guest@rabbitmq:5672")
    channel = await connection.channel()
    app.state.exchange = await exchange_message(channel=channel,name="notification_message")
    
    
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    app.state.producer = producer
    consumer  = AIOKafkaConsumer("orders",bootstrap_servers="kafka:9092",group_id="orders_notification")
    task = asyncio.create_task(consume(consumer))
    await consumer.start()
    await producer.start()
    yield
    await producer.stop()
    await consumer.stop()


app = FastAPI(lifespan=lifespan)




@app.post("/orders")
async def get_orders(user_id:int,data:dict):
    await app.state.producer.send_and_wait("orders",key=f"key:{user_id}",value=json.dumps(data).encode())
    
    return {"result":"access"}

    








@app.get("/hello/my_name")
async def hello(name: str):

    await send_message(routing_key="notification.send",exchange=app.state.exchange,data={"name": name})
    
    
    
    return {"message": f"Hello, {name}"}

    



@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Razmik"
    }

