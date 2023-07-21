# LED_MATRIX
# Patrick Koenigstorfer

import tkinter
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from random import randint
from time import strftime
import json
import csv


class MyApp(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        '''Groeße der Matrix'''
        self.leds_y = int(16)
        self.leds_x = int(16)

        '''Aktive RGB-Arbeitsliste erstellen'''
        self.RGB_code = []
        led_rgb = 50 
        x=1
        for i in range(0, self.leds_y*self.leds_x):
            self.RGB_code.append((led_rgb,led_rgb,led_rgb))
            led_rgb+=x
            if led_rgb == 100:
                x=-1
            if led_rgb == 50:
               x=1

        '''Ausgabe counter für CSV und TXT Datein'''
        self.pic_nr=0
        
        '''Farben aus Hex und RGB Werten erstellen'''
        self.color = "black"
        self.R, self.G, self.B  = 0,0,0

        self.create_gui()
        self.LED_Raster()
    def create_gui(self):
        '''Layer LED Raster Platzieren'''
        self.LED_Matrix_layer = tkinter.Label(self)
        self.LED_Matrix_layer.grid(row=1, column=0, padx=0, pady=0)
        
        """Layer Farbauswahl + Optionen"""
        self.color_layer = tkinter.Label(self)
        self.color_layer.grid(row=1, column=1, padx=0, pady=0)
        ## Befehl Buttons
        self.control_layer = tkinter.Label(self.color_layer)
        self.control_layer.grid(row=0, column=0, padx=0, pady=0)
        ## RGB Vorschau
        self.vorschau_rgb = tkinter.Label(self.color_layer)
        self.vorschau_rgb.grid(row=1, column=0, padx=0, pady=0)
        ## RGB regler
        self.rgb_slicer = tkinter.Label(self.color_layer)
        self.rgb_slicer.grid(row=2, column=0, padx=0, pady=0)
        ## Farbauswahl Buttons
        self.farben_vorauswahl = tkinter.Label(self.color_layer)
        self.farben_vorauswahl.grid(row=3, column=0, padx=0, pady=0)

        '''Befehl Buttons'''
        self.bu_all_black = tkinter.Button(self.control_layer, height=2, width=10, text="all on black", command=self.clear)
        self.bu_all_black.grid(row=0, column=0, padx=0, pady=0)
        self.bu_all_white= tkinter.Button(self.control_layer, height=2, width=10, text="all on white", command=self.all_white)
        self.bu_all_white.grid(row=0, column=1, padx=0, pady=0)
        self.bu_all_gray= tkinter.Button(self.control_layer, height=2, width=10, text="all on gray ", command=self.all_gray)
        self.bu_all_gray.grid(row=0, column=2, padx=0, pady=0)

        self.bu_all_red = tkinter.Button(self.control_layer, height=2, width=10, text="all on red", command=self.all_red)
        self.bu_all_red.grid(row=1, column=0, padx=0, pady=0)
        self.bu_all_green= tkinter.Button(self.control_layer, height=2, width=10, text="all on green", command=self.all_green)
        self.bu_all_green.grid(row=1, column=1, padx=0, pady=0)
        self.bu_all_blue= tkinter.Button(self.control_layer, height=2, width=10, text="all on blue", command=self.all_blue)
        self.bu_all_blue.grid(row=1, column=2, padx=0, pady=0)

        self.bu_selected_color = tkinter.Button(self.control_layer, height=2, width=10,text="selected_color", command=self.selected_color)
        self.bu_selected_color.grid(row=2, column=0, padx=0, pady=0)
        self.bu_rainbow_bw = tkinter.Button(self.control_layer, height=2, width=10, text="rainbow b/w", command=self.rainbow_b_w)
        self.bu_rainbow_bw.grid(row=2, column=1, padx=0, pady=0)
        self.bu_NOTHING = tkinter.Button(self.control_layer, height=2, width=10, text="all random", command=self.all_random)
        self.bu_NOTHING.grid(row=2, column=2, padx=0, pady=0)

        self.bu_NOTHING = tkinter.Button(self.control_layer, height=2, width=10, text="open", command=self.open_file)
        self.bu_NOTHING.grid(row=3, column=0, padx=0, pady=0)
        self.bu_NOTHING= tkinter.Button(self.control_layer, height=2, width=10, text="rainbow", command=self.rainbow)
        self.bu_NOTHING.grid(row=3, column=1, padx=0, pady=0)
        self.bu_NOTHING= tkinter.Button(self.control_layer, height=2, width=10)#, text="rotation_y_02", command=self.rotation_y_02)
        self.bu_NOTHING.grid(row=3, column=2, padx=0, pady=0)

        self.bu_livescreen = tkinter.Button(self.control_layer, height=2, width=10, text="rotation_x", command=self.rotation_x)
        self.bu_livescreen.grid(row=4, column=0, padx=0, pady=0)
        self.bu_NOTHING = tkinter.Button(self.control_layer, height=2, width=10, text="rotation_y", command=self.rotation_y)
        self.bu_NOTHING.grid(row=4, column=1, padx=0, pady=0)
        self.bu_NOTHING = tkinter.Button(self.control_layer, height=2, width=10, text="rotation_z", command=self.rotation_z)
        self.bu_NOTHING.grid(row=4, column=2, padx=0, pady=0)

        self.bu_create_save_files = tkinter.Button(self.control_layer, height=2, width=10, text="save", command=self.create_csv_and_txt_file)
        self.bu_create_save_files.grid(row=5, column=0, padx=0, pady=0)
        self.bu_import_csv= tkinter.Button(self.control_layer, height=2, width=10, text="return to last\nsavepoint", command=self.import_csv_savepoint)
        self.bu_import_csv.grid(row=5, column=1, padx=0, pady=0)
        self.bu_print_idle= tkinter.Button(self.control_layer, height=2, width=10, text="print idle", command=self.print_idle)
        self.bu_print_idle.grid(row=5, column=2, padx=0, pady=0)

        '''Button RGB Farb Auswahl'''
        self.vorschau_titel = tkinter.Label(self.vorschau_rgb, text="Color Preview:")
        self.vorschau_titel.grid(row=0, column=0, padx=0, pady=0)
        self.RGB_Color = tkinter.Button(self.vorschau_rgb, height=2, width=35, bg='black', command=self.ask_color_chosser)
        self.RGB_Color.grid(row=1, column=0, padx=0, pady=0)

        '''RGB Regler'''
        self.slicer_R = tkinter.Scale(self.rgb_slicer, from_=0, to=255, resolution=1, orient='horizontal',highlightbackground='red', bg='white', length=256, command=self.RGB_R)
        self.slicer_R.grid(row=0, column=0, padx=0, pady=0)

        self.slicer_G = tkinter.Scale(self.rgb_slicer, from_=0, to=255, resolution=1, orient='horizontal',highlightbackground='green', bg='white', length=256, command=self.RGB_G)
        self.slicer_G.grid(row=1, column=0, padx=0, pady=0)

        self.regler_b = tkinter.Scale(self.rgb_slicer, from_=0, to=255, resolution=1, orient='horizontal',highlightbackground='blue', bg='white', length=256, command=self.RGB_B)
        self.regler_b.grid(row=2, column=0, padx=0, pady=0,)
        
        '''Farbauswahl Buttons'''
        self.button_black = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='black', command=self.pen_black)
        self.button_black.grid(row=0, column=0, padx=0, pady=0)
        self.button_red = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='red', command=self.pen_red)
        self.button_red.grid(row=0, column=1, padx=0, pady=0)
        self.button_blue = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='blue', command=self.pen_blue)
        self.button_blue.grid(row=0, column=2, padx=0, pady=0)
        self.button_green = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='green', command=self.pen_green)
        self.button_green.grid(row=0, column=3, padx=0, pady=0)

        self.button_yellow = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='yellow', command=self.pen_yellow)
        self.button_yellow.grid(row=1, column=0, padx=0, pady=0)
        self.button_violet = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='violet', command=self.pen_violet)
        self.button_violet.grid(row=1, column=1, padx=0, pady=0)
        self.button_cyan = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='cyan', command=self.pen_cyan)
        self.button_cyan.grid(row=1, column=2, padx=0, pady=0)
        self.button_white = tkinter.Button(self.farben_vorauswahl, height=2, width=5, bg='white', command=self.pen_white)
        self.button_white.grid(row=1, column=3, padx=0, pady=0)

    '''LED Panel'''
    def LED_Raster(self):
        def matrix(x, y, led):
            new=globals()["self.LED"+str(led)]
            new.configure(bg=self.color)
            color_active = (self.R, self.G, self.B)
            self.RGB_code[led] = color_active
            self.create_livescreen()
        ## LEDs als Raster aufbauen
        led=0
        for y in range(0, self.leds_y):
            for x in range(0, self.leds_x):
                globals()["self."+"LED"+str(led)] = tkinter.Button(self.LED_Matrix_layer)
                new_button=globals()["self."+"LED"+str(led)]
                new_button["bg"]="#%02x%02x%02x" % (self.RGB_code[led])
                new_button["text"]=led
                new_button["height"]=2
                new_button["width"]=5
                new_button["command"] = lambda x=x, y=y, led=int(led): matrix(y, x, led)
                new_button.grid(row=y, column=x)
                led+=1
    
    '''Funktions Buttons'''
    def rotation_y(self):
        rotation_RGB_code=[]
        rotation_work=[]
        for led_rgb in self.RGB_code:
            if len(rotation_work) <= self.leds_x:
                rotation_work.append(led_rgb)
                if len(rotation_work) == self.leds_x:
                    for i in reversed(rotation_work):
                        rotation_RGB_code.append(i)
                    rotation_work=[]
        led_nr=0
        for rotation_rgb in rotation_RGB_code:
            new=globals()["self.LED"+str(led_nr)]
            r,g,b= rotation_rgb
            color_change = "#%02x%02x%02x" % (int(r),int(g),int(b))
            new.configure(bg=color_change)
            self.RGB_code[led_nr] = (int(r),int(g),int(b))
            led_nr+=1
        self.create_livescreen()

    def rotation_x(self):
        rotation_RGB_code=[]
        rotation_work=[]
        for led_rgb in reversed(self.RGB_code):
            if len(rotation_work) <= self.leds_x:
                rotation_work.append(led_rgb)
                if len(rotation_work) == self.leds_x:
                    for i in reversed(rotation_work):
                        rotation_RGB_code.append(i)
                    rotation_work=[]
        led_nr=0
        for rotation_rgb in rotation_RGB_code:
            new=globals()["self.LED"+str(led_nr)]
            r,g,b= rotation_rgb
            color_change = "#%02x%02x%02x" % (int(r),int(g),int(b))
            new.configure(bg=color_change)
            self.RGB_code[led_nr] = (int(r),int(g),int(b))
            led_nr+=1
        self.create_livescreen()

    def rotation_z(self):
        rotation_RGB_code=[]
        rotation_work=[]
        rotation_RGB_code_turn=[]
        for column in range(self.leds_y):
            x=column
            for i in range(self.leds_x):
                rotation_RGB_code.append(x)
                x+=self.leds_x

        for i in rotation_RGB_code:
            if len(rotation_work) <= self.leds_x:
                rotation_work.append(self.RGB_code[i])
            if len(rotation_work) == self.leds_x:
                for i in reversed(rotation_work):
                    rotation_RGB_code_turn.append(i)
                rotation_work=[]       

        led_nr=0
        for rotation_rgb in rotation_RGB_code_turn:
            new=globals()["self.LED"+str(led_nr)]
            r,g,b= rotation_rgb
            color_change = "#%02x%02x%02x" % (int(r),int(g),int(b))
            new.configure(bg=color_change)
            self.RGB_code[led_nr] = (int(r),int(g),int(b))
            led_nr+=1

        self.create_livescreen()

    def rotation_y_02(self):
        mirror_RGB_code=[]
        for led_nr in reversed(self.RGB_code):
            mirror_RGB_code.append(led_nr)
        led_nr=0
        for mirror_rgb in mirror_RGB_code:
            new=globals()["self.LED"+str(led_nr)]
            r,g,b=mirror_rgb
            color_change = "#%02x%02x%02x" % (int(r),int(g),int(b))
            new.configure(bg=color_change)
            self.RGB_code[led_nr] = (int(r),int(g),int(b))
            led_nr+=1
        self.create_livescreen()
        
    def clear(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            new.configure(bg='black')
            self.RGB_code[i] = 0,0,0
        self.create_livescreen()

    def all_white(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (255,255,255)
            new.configure(bg='white')
            self.RGB_code[i] = 255,255,255
        self.create_livescreen()

    def all_gray(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (136,136,136)
            new.configure(bg=color_change)
            self.RGB_code[i] = 136,136,136
        self.create_livescreen()

    def all_red(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (255,0,0)
            new.configure(bg=color_change)
            self.RGB_code[i] = 255,0,0
        self.create_livescreen()
            
    def all_green(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (0,255,0)
            new.configure(bg=color_change)
            self.RGB_code[i] = 0,255,0
        self.create_livescreen()
            
    def all_blue(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (0,0,255)
            new.configure(bg=color_change)
            self.RGB_code[i] = 0,0,255
        self.create_livescreen()

    def all_random(self):
        for i in range(0,self.leds_y*self.leds_x):
            r,g,b = randint(0,255),randint(0,255),randint(0,255)
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (r,g,b)
            new.configure(bg=color_change)
            self.RGB_code[i] = r,g,b
        self.create_livescreen()

    def rainbow_b_w(self):
        led_rgb = 50
        x=1
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (led_rgb,led_rgb,led_rgb)
            new.configure(bg=color_change)
            self.RGB_code[i] = led_rgb,led_rgb,led_rgb
            led_rgb+=x
            if led_rgb == 100:
                x=-1
            if led_rgb == 50:
               x=1
        self.create_livescreen()

    def rainbow(self):
        if self.leds_x*self.leds_x >= 257:
            step_rgb = 1
            led_r = 1
            led_g = 1
            led_b = 1
        else:
            step_rgb = 4
            led_r = 30
            led_g = 30
            led_b = 30
        
        for i in range(0,self.leds_y*self.leds_x):

            if i <= int(self.leds_y*self.leds_x/5):
                new=globals()["self.LED"+str(i)]
                color_change = "#%02x%02x%02x" % (led_r,led_g,led_b)
                new.configure(bg=color_change)
                self.RGB_code[i] = led_r,led_g,led_b
                led_r+=step_rgb

            if i <= int(self.leds_y*self.leds_x/5*2) and i >= int(self.leds_y*self.leds_x/5):
                new=globals()["self.LED"+str(i)]
                color_change = "#%02x%02x%02x" % (led_r,led_g,led_b)
                new.configure(bg=color_change)
                self.RGB_code[i] = led_r,led_g,led_b
                led_g+=step_rgb

            if i <= int(self.leds_y*self.leds_x/5*3) and i >= int(self.leds_y*self.leds_x/5*2):
                new=globals()["self.LED"+str(i)]
                color_change = "#%02x%02x%02x" % (led_r,led_g,led_b)
                new.configure(bg=color_change)
                self.RGB_code[i] = led_r,led_g,led_b
                led_r-=step_rgb

            if i <= int(self.leds_y*self.leds_x/5*4)-1 and i >= int(self.leds_y*self.leds_x/5*3):
                new=globals()["self.LED"+str(i)]
                color_change = "#%02x%02x%02x" % (led_r,led_g,led_b)
                new.configure(bg=color_change)
                self.RGB_code[i] = led_r,led_g,led_b
                led_b+=step_rgb

            if i <= int(self.leds_y*self.leds_x/5*5) and i >= int(self.leds_y*self.leds_x/5*4):
                new=globals()["self.LED"+str(i)]
                color_change = "#%02x%02x%02x" % (led_r,led_g,led_b)
                new.configure(bg=color_change)
                self.RGB_code[i] = led_r,led_g,led_b
                led_g-=step_rgb
        self.create_livescreen()

    def selected_color(self):
        for i in range(0,self.leds_y*self.leds_x):
            new=globals()["self.LED"+str(i)]
            color_change = "#%02x%02x%02x" % (self.R,self.G,self.B)
            new.configure(bg=color_change)
            self.RGB_code[i] = self.R,self.G,self.B
        self.create_livescreen()
            
    '''Farbauswahl Buttons'''
    def pen_black(self):
        self.R, self.G, self.B = 0,0,0
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg='black')
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_red(self):
        self.R, self.G, self.B = 255,0,0
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_blue(self):
        self.R, self.G, self.B = 0,0,255
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_green(self):
        self.R, self.G, self.B = 0,255,0
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_yellow(self):
        self.R, self.G, self.B = 255,255,0
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_violet(self):
        self.R, self.G, self.B = 255,0,255
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_cyan(self):
        self.R, self.G, self.B = 0,255,255
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)

    def pen_white(self):
        self.R, self.G, self.B = 255,255,255
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)
        self.vorschau()
        self.slicer_R.set(self.R)
        self.slicer_G.set(self.G)
        self.regler_b.set(self.B)
        
    '''RGB Slicer auslesen'''
    def RGB_R(self, event):
        self.R = self.slicer_R.get()
        self.vorschau()

    def RGB_G(self, event):
        self.G = self.slicer_G.get()
        self.vorschau()

    def RGB_B(self, event):
        self.B = self.regler_b.get()
        self.vorschau()

    '''RGB kombinieren und vorschau auf auswahl button zeigen'''
    def vorschau(self):
        self.color = "#%02x%02x%02x" % (self.R, self.G, self.B)
        self.RGB_Color.configure(bg=self.color)

    def ask_color_chosser(self):
        chosser_rgb,chosser_hx = askcolor(title="Tkinter Color Chooser")
        try:
            self.color = chosser_hx
            self.R,self.G,self.B = chosser_rgb
            self.slicer_R.set(self.R)
            self.slicer_G.set(self.G)
            self.regler_b.set(self.B)
            self.vorschau()
        except TypeError:
            pass

    '''RGB Werte ausgeben'''
    def print_idle(self):
        print("\n","Liste:","\n", len(self.RGB_code))
        print(self.RGB_code)

    def create_csv_and_txt_file(self):
        self.file_typ_txt = ".txt"
        self.file_typ_csv = ".csv"
        self.timestamp = strftime('%d%b%y_%H%M%S')
        self.name_file_txt = "pic_{0}_from_{1}{2}".format(self.pic_nr, self.timestamp , self.file_typ_txt)
        self.name_file_csv = "pic_{0}_from_{1}{2}".format(self.pic_nr, self.timestamp , self.file_typ_csv)
        self.pic_nr+=1
        with open(self.name_file_txt, "w") as file:
            json.dump(self.RGB_code, file)

        with open(self.name_file_csv, "w") as csv_file:
            for i in self.RGB_code:
                writer = csv.writer(csv_file)
                writer.writerow(i)

    def create_livescreen(self):
        self.live_file = "csv_file_live.csv"
        with open(self.live_file, "w") as csv_file:
            for i in self.RGB_code:
                writer = csv.writer(csv_file)
                writer.writerow(i)
    
    '''RGB Einlesen'''
    def open_file(self):
        try:
            filename = filedialog.askopenfilename(initialdir= "examples_csv", title = "open csv file", filetypes=[("CSV", ".csv")])
            print(filename)
            with open(filename, 'r')as import_file:
                reader = csv.reader(import_file, delimiter=',')
                count=0
                list_nr=0
                for rgb in reader:
                    if count %2:
                        pass
                    else:
                        r,g,b= rgb
                        new=globals()["self.LED"+str(list_nr)]
                        color_change = "#%02x%02x%02x" % (int(r),int(g),int(b))
                        new.configure(bg=color_change)
                        self.RGB_code[list_nr] = r,g,b
                        list_nr+=1
                    count+=1
            self.create_livescreen()
        except AttributeError:
            pass
        except FileNotFoundError:
            pass

    def import_csv_savepoint(self):
        with open(self.name_file_csv, 'r')as import_file:
            reader = csv.reader(import_file, delimiter=',')
            count=0
            list_nr=0
            for rgb in reader:
                if count %2:
                    pass
                else:
                    r,g,b= rgb
                    new=globals()["self.LED"+str(list_nr)]
                    color_change = "#%02x%02x%02x" % (int(r),int(g),int(b))
                    new.configure(bg=color_change)
                    self.RGB_code[list_nr] = r,g,b
                    list_nr+=1
                count+=1
        self.create_livescreen()

root = tkinter.Tk()
root.title('LED Matrix')
app = MyApp(root)
app.mainloop()
