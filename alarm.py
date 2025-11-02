from lifxlan import Light, Group
import time
import settings

# Set up LIFX objects
light_1 = Light(settings.light_1_mac, settings.light_1_ip)
light_2 = Light(settings.light_2_mac, settings.light_2_ip)
g = Group([light_1, light_2])

# Minor settings processing
fade_in_stage_milliseconds = settings.fade_in_stage_seconds * 1000

# Run wake-up sequence
g.set_power(0, 1)
g.set_color(settings.start_stage_color, 1)
g.set_power(1, 1)
g.set_color(settings.fade_in_stage_color, fade_in_stage_milliseconds)
time.sleep(settings.fade_in_stage_seconds)
g.set_color(settings.end_stage_color, 1)
time.sleep(settings.end_stage_seconds)
g.set_power(0, 1)
