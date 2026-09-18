import aio_pika
from aio_pika.abc import AbstractChannel,AbstractExchange,AbstractConnection, ExchangeType
import json


async def connection_rabitmq(url)->AbstractConnection:
    return await aio_pika.connect_robust(url=url)


async def exchange_message(channel:AbstractChannel,name:str):
    return await channel.declare_exchange(name=name,type=ExchangeType.DIRECT)

async def send_message(routing_key:str,exchange:AbstractExchange,data:dict|str):
    message = aio_pika.Message(json.dumps(data).encode())
    await exchange.publish(message=message,routing_key=routing_key)
    
