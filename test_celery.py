# import os
# from celery import Celery

# REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# celery = Celery(
#     "my-celery",
#     broker=f"redis://{REDIS_HOST}:6379/0",
#     backend=f"redis://{REDIS_HOST}:6379/1"
# )

# @celery.task(name="email_send",autoretry_for=(ConnectionError,),
#              max_retries=3)
# def send_email(email:str):
#         return email
    
# @celery.task(name="notification_send",autoretry_for=(ConnectionError,),
#              max_retries=3)
# def send_notification(message:str):
#     return message

    
    
    
    
