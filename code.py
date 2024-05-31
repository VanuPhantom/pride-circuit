from adafruit_circuitplayground import cp

BLUE = 0x5BCEFA
WHITE = 0xFFFFFF
# PINK = 0xF5A9B8
PINK = 0xFF5050

while True:
    cp.pixels.brightness = 0.05

    for index in range(10):
        color = WHITE

        relative_index = index % 5

        if relative_index in [0, 4]:
            color = BLUE
        elif relative_index in [1, 3]:
            color = PINK

        print(f"{index} {color}")
        
        cp.pixels[index] = color

