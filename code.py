from adafruit_circuitplayground import cp
import audiobusio
import board
from time import time
import math
from array import array

NUM_SAMPLES = 160

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))

def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)

def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))

def mean(values):
    return sum(values) / len(values)

samples = array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 500

def get_sound_level():
    global mic, samples, input_floor, input_ceiling

    mic.record(samples, len(samples))

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    return log_scale(constrain(magnitude, input_floor, input_ceiling),
                  input_floor, input_ceiling, 0, 9)

BLUE = 0x5BCEFA
WHITE = 0xFFFFFF
PINK = 0xFF5050

def flag(colors):
    return lambda index, tick, context: colors[index if index < 5 else 4 - index % 5]

def trans_pride(index, tick, context):
    relative_index = index % 5

    if relative_index in [0, 4]:
        return BLUE
    elif relative_index in [1, 3]:
        return PINK
    else:
        return WHITE

lesbian_pride = flag([0xD62800, 0xFF9B56, 0xFFFFFF,  0xD462A6, 0xA40062])
bisexual_pride = flag([0xD60270, 0xD60270, 0x9B4F96, 0x0038A8, 0x0038A8])

def solid_color(color):
    return lambda index, tick, context: color

def spin(renderer):
    return lambda index, tick, context: renderer((index + tick) % 10, tick, context)

def sound_sensitive(renderer1, renderer2):
    return lambda index, tick, context: (renderer1 if context["sound_level"] > index else renderer2)(index, tick, context)

def spinny_dot(renderer):
    return lambda index, tick, context: 0x00FF00 if tick % 10 == index else renderer(index, tick, context)

modes = [trans_pride, lesbian_pride, bisexual_pride, spin(trans_pride), sound_sensitive(solid_color(0x00FF00), trans_pride)]
mode_index = 0

def button_press_getter(get_down):
    previous_button_state = False
    
    def get_press():
        nonlocal previous_button_state

        current_button_state = get_down()
        
        try:
            if previous_button_state != current_button_state:
                return current_button_state
            else:
                return False
        finally:
            previous_button_state = current_button_state
            
    return get_press

get_button_a_press = button_press_getter(lambda: cp.button_a)
get_button_b_press = button_press_getter(lambda: cp.button_b)

while True:
    cp.pixels.brightness = 0.05

    tick = time()
    context = dict()

    context["sound_level"] = get_sound_level()

    if get_button_a_press():
        mode_index -= 1
    if get_button_b_press():
        mode_index += 1

    if mode_index < 0:
        mode_index = len(modes) - 1
    elif mode_index >= len(modes):
        mode_index = 0
    
    mode = modes[mode_index]
    upright = cp.switch

    for index in range(10):
        cp.pixels[index] = mode(index if upright else (index + 5) % 10, tick, context)
