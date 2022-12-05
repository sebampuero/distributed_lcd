from abc import ABC, abstractmethod
from PIL import ImageFont

class DisplayService(ABC):

    def __init__(self, id: str, width: int, height: int) -> None:
        self.id = id
        self.width = width
        self.height = height
        #sqs config load

    @abstractmethod
    def display(self, draw, values: dict):
        pass

    @abstractmethod
    def load_config(self):
        pass

    def load_font(self, font: str, size: int):
        return ImageFont.truetype(font, size=size)

    @abstractmethod
    def _update_values(self, vals: dict):
        pass # poll from sqs