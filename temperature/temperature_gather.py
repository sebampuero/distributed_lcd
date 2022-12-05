import boto3, time, subprocess, os, logging, json
from botocore.exceptions import ClientError
from temperatures_api import get_berlin_temperature, get_internal_temp
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler(os.path.abspath("temperature.log"), when='d')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

TIME_INTERVAL_API = 600


def main():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName="RaspiQueue")
    while True:
        try:
            last_retrieval_time = 0
            last_berlin_temp = 0.0
            if time.time() - last_retrieval_time > TIME_INTERVAL_API:
                temperature = str(get_berlin_temperature())
                last_berlin_temp = temperature
                last_retrieval_time = time.time()
            inside_temp = get_internal_temp()
            raspi_temp = subprocess.Popen("vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE)
            raspi_temp = raspi_temp.stdout.read().decode()
            raspi_temp = raspi_temp.replace("temp=", "").replace("'C", "").replace('\n', '')
            raspi_temp2 = subprocess.Popen("ssh pi@pi4g vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE)
            raspi_temp2 = raspi_temp2.stdout.read().decode()
            raspi_temp2= raspi_temp2.replace("temp=", "").replace("'C", "").replace('\n', '')
            data = {
                "Id": str(int(time.time())),
                "MessageBody": json.dumps({
                    "identifier": "TemperatureService",
                    "timestamp": int(time.time()),
                    "data": {
                        "pi2": raspi_temp,
                        "pi4": raspi_temp2,
                        "indoor": inside_temp,
                        "outdoor": last_berlin_temp
                    }
                })
            }
            queue.send_messages(Entries=[data])
        except ClientError:
            logger.exception(f"Send message failed to queue {queue}")
        except Exception:
            logger.error("General error", exc_info=True)
        finally:
            time.sleep(10)

if __name__ == '__main__':
    try:
        main()
    except:
        logger.error("Initializing", exc_info=True)
        

