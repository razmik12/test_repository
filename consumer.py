import aio_pika
from aio_pika.abc import AbstractChannel,AbstractExchange,AbstractConnection, ExchangeType,AbstractIncomingMessage,AbstractQueue
import json

async def income_message_consumer(message:AbstractIncomingMessage):
    async with message.process():
        get_message = json.loads(message.body)
        print(get_message["names"],flush=True)
        
    


async def consumer_await():
    connection =  await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672")
    channel = await connection.channel()
    exchnage = await channel.declare_exchange(name="notification_message",type=ExchangeType.DIRECT)
    queue = await channel.declare_queue(name="notification_queue")
    await queue.bind(exchange=exchnage,routing_key="notification.send")
    await queue.consume(income_message_consumer)