"""
lights.py

Usage:
    This script is meant to be run as a cron job set by set_alarm.py.
"""

from lifxlan import Light, Group
from dotenv import load_dotenv
import os
import time

# Wake-up time parameters in seconds

fade_in_stage_seconds = 600
end_stage_seconds = 300 

# Light color stages
#   From https://github.com/mclarkk/lifxlan: 
#       Each color is a HSBK list of values: [hue (0-65535), saturation (0-65535), brightness (0-65535), Kelvin (2500-9000)]

start_stage_color = [0, 0, 0, 7000]
fade_in_stage_color = [0, 0, 65535, 7000]
end_stage_color = [0, 0, 32807, 2000]

# Retrieve LIFX light mac and ip from a .env file in this script's directory
# See https://github.com/mclarkk/lifxlan for details on getting these using lifxlan

load_dotenv()
light_1_mac = os.getenv("LIGHT_1_MAC")
light_1_ip = os.getenv("LIGHT_1_IP")
light_2_mac = os.getenv("LIGHT_2_MAC")
light_2_ip = os.getenv("LIGHT_2_IP")

# Set up LIFX objects

light_1 = Light(light_1_mac, light_1_ip)
light_2 = Light(light_2_mac, light_2_ip)
g = Group([light_1, light_2])

# Run wake-up sequence

fade_in_stage_milliseconds = fade_in_stage_seconds * 1000
g.set_power(0, 1)
g.set_color(start_stage_color, 1)
g.set_power(1, 1)
g.set_color(fade_in_stage_color, fade_in_stage_milliseconds)
time.sleep(fade_in_stage_seconds)
g.set_color(end_stage_color, 1)
time.sleep(end_stage_seconds)
g.set_power(0, 1)
