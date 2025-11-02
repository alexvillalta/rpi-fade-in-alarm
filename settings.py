from dotenv import load_dotenv
import os

# Wake-up time parameters in seconds

fade_in_stage_seconds = 30
end_stage_seconds = 15 

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