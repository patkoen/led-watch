## https://github.com/rpi-ws281x/rpi-ws281x-python
## sudo pip install rpi_ws281x
from rpi_ws281x import *
import time
import csv



def colorWipe():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,Color(0,0,0))
    strip.show()

def create_led_matrix_as_list():
    global leds
    leds=[]
    ab_1_start=184
    ab_1_stop=128
    ab_2_start=56
    ab_2_stop=0
    for i in range(8):
        for led in range(ab_1_start,ab_1_stop-8,-8):
            leds.append(led)
        for led in range(ab_2_start,ab_2_stop-8,-8):
            leds.append(led)
        ab_1_start+=1
        ab_1_stop+=1
        ab_2_start+=1
        ab_2_stop+=1

    ab_1_start=248
    ab_1_stop=192
    ab_2_start=120
    ab_2_stop=64
    for i in range(8):
        for led in range(ab_1_start,ab_1_stop-8,-8):
            leds.append(led)
        for led in range(ab_2_start,ab_2_stop-8,-8):
            leds.append(led)
        ab_1_start+=1
        ab_1_stop+=1
        ab_2_start+=1
        ab_2_stop+=1

def import_csv_file():
    global led_rgb
    led_rgb = []
    for i in range(0,256):
        rgb=0,0,0
        led_rgb.append(rgb)

    with open("csv_file_live.csv", 'r')as import_file:
        reader = csv.reader(import_file, delimiter=',')
        count=0
        led_nr=0
        for rgb in reader:
            if count %2:
                pass
            else:
                r,g,b= rgb
                led_rgb[led_nr] = r,g,b
                led_nr+=1
            count+=1

def show_led():
    create_led_matrix_as_list()
    import_csv_file()

    stop=1000
    led_nr=0
    for led in leds:
        r,g,b=led_rgb[led_nr]
        strip.setPixelColor(led,Color(int(r),int(g),int(b)))
        led_nr+=1
    strip.show()
    time.sleep(1)

if __name__ == '__main__':
    # LED strip configuration:
    LED_COUNT      = 256      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print ('Press Ctrl-C to quit.')
    try:
        while True:
            show_led()

    except KeyboardInterrupt:
        colorWipe()