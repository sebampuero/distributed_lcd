import os
import asyncio
import websockets
import ssl
import requests
import logging
import boto3
import time
import json
from botocore.exceptions import ClientError
API_ENDPOINT = f"https://api.ip2loc.com/{os.environ['IP_LOG_KEY']}/"
AVOID_IP = ['158.181.79.45']

from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler(os.path.abspath("ip_log.log"), when='d')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName="RaspiQueue")

async def hello():
    uri = "wss://sebampuerom.de:8765"
    async for websocket in websockets.connect(uri, ssl=ssl_context, ping_timeout=60, close_timeout=60, ping_interval=30):
        try:
            await websocket.send("Connected")
            async for message in websocket:
                await consumer(message)
        except websockets.ConnectionClosed:
            logger.info("Disconnected, retrying")
            continue
        else:
            continue

async def consumer(message):
    logger.info(f"Received new message: {message}")
    if message in AVOID_IP:
        return
    response = requests.request('GET', API_ENDPOINT + message)
    try:
        response = response.json()
        with open(os.path.abspath('ip_logs.log'), 'a') as f:
            f.write(f"Country: {response['location']['country']['name']} City: {response['location']['city']} IP: {response['connection']['ip']}\n")
        data = {
            "Id": str(int(time.time())),
            "MessageBody": json.dumps({
                "identifier": "IPLogService",
                "timestamp": int(time.time()),
                "data": {
                    "country": f"{response['location']['city']},{response['location']['country']['name']}",
                    "ip": response['connection']['ip']
                }
            })
        }
        queue.send_messages(Entries=[data])
    except ClientError:
        logger.exception(f"Send message failed to queue {queue}")
    except:
        logging.error("Exception occurred", exc_info=True)
        

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations("/home/pi/dist_systems/ip_log/cert.pem")

if __name__ == '__main__':
    asyncio.run(hello())