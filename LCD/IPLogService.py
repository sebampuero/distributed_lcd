from DisplayService import DisplayService
import json

class IPLogService(DisplayService):

    def __init__(self, id: str, width: int, height: int) -> None:
        super().__init__(id, width, height)
        self.txt_font = "/home/pi/dist_systems/LCD/OpenSans-Regular.ttf"
        self.fa = "/home/pi/dist_systems/LCD/fontawesome-webfont.ttf"

    def load_config(self):
        # read config and load into local vars, draw could also read config to dynamically change
        with open("/home/pi/dist_systems/LCD/coords_config.json", "r") as f:
            temp_config = json.loads(f.read())['IPLogService']
        self.line = tuple(map(lambda x: self.width -1 if x == -1 else x, temp_config['separation_line']))
        self.flag_logo = temp_config['flag_logo']
        self.country_text = temp_config['country_text']
        self.globe_logo = temp_config['globe_logo']
        self.ip_text = temp_config['ip_text']


    def _update_values(self, vals: dict):
        self.country = vals['country']
        self.ip = vals['ip']

    def display(self, draw, values):
        self._update_values(values)
        self.load_config()
        draw.line(self.line, fill="white")
        draw.text(tuple(self.flag_logo['coords']), text="\uf024", font=self.load_font(self.fa, self.flag_logo['size']), fill="white")
        draw.text(tuple(self.country_text['coords']), text=self.country, font=self.load_font(self.txt_font, self.country_text['size']), fill="white")
        draw.text(tuple(self.globe_logo['coords']), text="\uf0ac", font=self.load_font(self.fa, self.globe_logo['size']),fill="white")
        draw.text(tuple(self.ip_text['coords']), text=self.ip, font=self.load_font(self.txt_font, self.ip_text['size']),fill="white")
