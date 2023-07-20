## https://github.com/rpi-ws281x/rpi-ws281x-python
## sudo pip install rpi_ws281x
from rpi_ws281x import *
from time import strftime, sleep

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

def create_numbers_as_list():
    global num_in_leds
    num_in_leds=[
        [0,1,2,16,18,32,34,48,50,64,65,66],#0
        [2,17,18,34,50,66],#1
        [0,1,2,18,32,33,48,64,65,66],#2
        [0,1,2,18,33,34,50,64,65,66],#3
        [0,16,32,33,34,49,65],#4
        [0,1,2,16,32,33,34,50,64,65,66],#5
        [0,1,2,16,32,33,34,48,50,64,65,66],#6
        [0,1,2,18,33,49,65],#7
        [0,1,2,16,18,32,33,34,48,50,64,65,66],#8
        [0,1,2,16,18,32,33,34,50,64,65,66]#9
        ]

create_led_matrix_as_list()
create_numbers_as_list()

def clock():
    ## Hintergrund erstellen
    led_rgb=[] ## Bild als Liste erstelln
    for i in range(0,256):
        led_rgb.append((0,0,0))
    ## Hintergrund definieren
    for led_nr in leds:
        r,g,b=led_rgb[led_nr]
        strip.setPixelColor(led_nr,Color(int(r),int(g),int(b)))
    
    hour=strftime("%H")
    minute=strftime("%M")
    second=strftime("%S")

    h1_x,h1_y = 2,4
    h2_x,h2_y = 2,9
    m1_x,m1_y = 9,4
    m2_x,m2_y = 9,9

    h0_x_y = int(16*h1_x+h1_y)
    h1_x_y = int(16*h2_x+h2_y)
    m0_x_y = int(16*m1_x+m1_y)
    m1_x_y = int(16*m2_x+m2_y)

    for led in num_in_leds[int(hour[0])]:
        strip.setPixelColor(leds[led+h0_x_y],Color(0,100,0))
    
    for led in num_in_leds[int(hour[1])]:
        strip.setPixelColor(leds[led+h1_x_y],Color(0,100,0))
    
    for led in num_in_leds[int(minute[0])]:
        strip.setPixelColor(leds[led+m0_x_y],Color(0,100,0))
    
    for led in num_in_leds[int(minute[1])]:
        strip.setPixelColor(leds[led+m1_x_y],Color(0,100,0))

    pixel_seconds = [8,9,10,11,12,13,14,15,31,47,63,79,95,111,127,143,159,175,191,207,223,239,255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240,224,208,192,176,160,144,128,112,96,80,64,48,32,16,0,1,2,3,4,5,6,7]
    r=35
    g=100
    for led in range(int(second)+1):#-4):
        strip.setPixelColor(leds[pixel_seconds[led]],Color(r,g,0))
        r+=1
        g-=1

    #sec=strftime("%S")
    #wait=int(60)-int(sec)
    #print(strftime("%M"),sec, wait)
    #sleep(wait)
    strip.show()
    sleep(0.1)

if __name__ == '__main__':
    ## LED STRIP:
    LED_COUNT      = 256     # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    create_led_matrix_as_list()
    print(leds)
    try:
        print('Press ctrl-C to close.')
        x=1
        while True:
            clock()
    
    except KeyboardInterrupt:
        colorWipe()
