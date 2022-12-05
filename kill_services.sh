#!/bin/bash
kill -9 $(ps aux | grep '[p]ython3 /home/pi/dist_systems/LCD/lcd_main.py' | awk '{print $2}')
kill -9 $(ps aux | grep '[p]ython3 /home/pi/dist_systems/temperature/temperature_gather.py' | awk '{print $2}')
kill -9 $(ps aux | grep '[p]ython3 /home/pi/dist_systems/ip_log/websocket_ip_logger.py' | awk '{print $2}')