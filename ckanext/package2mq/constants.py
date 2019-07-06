import pika
#contain some config variables
RABBITMQ_ACCOUNT_NAME="root"
RABBITMQ_ACCOUNT_PASSWORD="root"
RABBITMQ_HOST="localhost"
RABBITMQ_PORT=5672
RABBITMQ_QUEUE="message_BC"
credentials=pika.PlainCredentials(RABBITMQ_ACCOUNT_NAME,RABBITMQ_ACCOUNT_PASSWORD)
