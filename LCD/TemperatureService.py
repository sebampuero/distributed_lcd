from DisplayService import DisplayService
import json
from PIL import Image

class TemperatureService(DisplayService):
    
    def __init__(self, id: str, width: int, height: int) -> None:
        super().__init__(id,width,height)
        self.load_config()
        self.pi_logo_img = Image.open("/home/pi/dist_systems/LCD/pi_logo.png").convert("RGBA")
        self.txt_font = "/home/pi/dist_systems/LCD/OpenSans-Regular.ttf"
        self.fa = "/home/pi/dist_systems/LCD/fontawesome-webfont.ttf"

    def load_config(self):
        # read config and load into local vars, draw could also read config to dynamically change
        with open("/home/pi/dist_systems/LCD/coords_config.json", "r") as f:
            temp_config = json.loads(f.read())['TemperatureService']
        self.line = tuple(map(lambda x: self.width -1 if x == -1 else x, temp_config['separation_line']))
        self.pi2_logo = temp_config['pi2_logo']
        self.pi4_logo = temp_config['pi4_logo']
        self.pi2_temp = temp_config['pi2_temp']
        self.pi4_temp = temp_config['pi4_temp']
        self.retropie_logo = temp_config['retropie_logo']
        self.retropie_temp = temp_config['retropie_temp']
        self.indoor_temp_logo = temp_config['indoor_temp_logo']
        self.indoor_temp = temp_config['indoor_temp']
        self.outdoor_temp_logo = temp_config['outdoor_temp_logo']
        self.outdoor_temp = temp_config['outdoor_temp']

    def _update_values(self, vals: dict):
        self.pi2_temp_val = vals['pi2'][0:-2]
        self.pi4_temp_val = vals['pi4'][0:-2]
        self.retropie_temp_val = vals['retropie'][0:-2]
        self.indoor_temp_val = str(round(float(vals['indoor']), 1))
        self.outdoor_temp_val = str(round(float(vals['outdoor']), 1))

    def display(self, draw, values):
        self._update_values(values)
        self.load_config()
        draw.line(self.line, fill="white")
        size = self.pi2_logo['size']
        draw.bitmap(tuple(self.pi2_logo['coords']), self.pi_logo_img.resize((size,size)), fill="white")
        size = self.pi4_logo['size']
        draw.bitmap(tuple(self.pi4_logo['coords']), self.pi_logo_img.resize((size,size)), fill="white")
        draw.text(tuple(self.pi2_temp['coords']), text=self.pi2_temp_val, font=self.load_font(self.txt_font, self.pi2_temp['size']), fill="white")
        draw.text(tuple(self.pi4_temp['coords']), text=self.pi4_temp_val, font=self.load_font(self.txt_font, self.pi4_temp['size']), fill="white")
        draw.text(tuple(self.retropie_logo['coords']), text="\uf11b", font=self.load_font(self.fa, self.retropie_logo['size']),fill="white")
        draw.text(tuple(self.retropie_temp['coords']), text=self.retropie_temp_val, font=self.load_font(self.txt_font, self.retropie_temp['size']),fill="white")
        draw.text(tuple(self.indoor_temp_logo['coords']), text="\uf015", font=self.load_font(self.fa, self.indoor_temp_logo['size']),fill="white")
        draw.text(tuple(self.indoor_temp['coords']), text=self.indoor_temp_val, font=self.load_font(self.txt_font, self.indoor_temp['size']),fill="white")
        draw.text(tuple(self.outdoor_temp_logo['coords']), text="\uf2c8", font=self.load_font(self.fa, self.outdoor_temp_logo['size']),fill="white")
        draw.text(tuple(self.outdoor_temp['coords']), text=self.outdoor_temp_val, font=self.load_font(self.txt_font, self.outdoor_temp['size']),fill="white")