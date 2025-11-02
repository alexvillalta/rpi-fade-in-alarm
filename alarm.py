from lifxlan import Light, Group
import time
import settings

# Set up LIFX objects
light_1 = Light(light_1_mac, light_1_ip)
light_2 = Light(light_2_mac, light_2_ip)
g = Group([light_1, light_2])

# Minor settings processing
fade_in_stage_milliseconds = fade_in_sec * 1000

# Run wake-up sequence
g.set_power(0, 1)
g.set_color(start_stage_color, 1)
g.set_power(1, 1)
g.set_color(fade_in_stage_color, fade_in_stage_milliseconds)
time.sleep(fade_in_stage_seconds)
g.set_color(end_stage_color, 1)
time.sleep(end_stage_color)
g.set_power(0, 1)