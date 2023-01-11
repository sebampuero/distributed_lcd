from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735
from logging.handlers import RotatingFileHandler
import time, boto3, json, os, importlib, logging, sys

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = RotatingFileHandler("/home/pi/dist_systems/LCD/lcd.log", maxBytes=5*1024*1024, backupCount=1)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

serial = spi()
args = {
    "active_low": False,
    "rotate": 2
}
device = st7735(serial_interface=serial, **args)
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName="RaspiQueue")

def load_class_dynamically(service_id, device):
    for entry in os.scandir("/home/pi/dist_systems/LCD"):
        if (entry.name.endswith(".py") and not entry.name == "DisplayService.py"): #Abstract class
            loaded_service_id = os.path.splitext(entry.name)[0]
            if loaded_service_id == service_id:
                service = getattr(importlib.import_module(name=f"{loaded_service_id}"), loaded_service_id)
                # see how to assert it is DisplayService!!
                return service(service_id, device.width, device.height)

def main():
    services_dict = {}
    while True:
        messages = queue.receive_messages(MessageAttributeNames=['All'], MaxNumberOfMessages=1, WaitTimeSeconds=20)
        for msg in messages:
            try:
                body = json.loads(msg.body)
                service = load_class_dynamically(body['identifier'], device)
                if not service:
                    logger.info(f"bad service: {msg.body['identifier']}")
                vals = body['data']
                services_dict[service.id] = {
                    "service": service,
                    "data": vals
                }
                with canvas(device) as draw:
                    for v in services_dict.values():
                        v['service'].display(draw,v['data'])
                logger.info(f"Processed: {body}")
            except json.JSONDecodeError:
                logger.error("bad format", exc_info=True)
            except Exception:
                logger.error("General error", exc_info=True)
            finally:
                time.sleep(1)
                msg.delete()

if __name__ == '__main__':
    try:
        main()
    except:
        logger.error("Initializing", exc_info=True)
