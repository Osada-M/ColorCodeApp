import tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image, ImageTk
import pyautogui
from PIL import ImageGrab
from pynput import mouse, keyboard
import threading
import time
import colorsys



## =====================================================================
## 


class ColorApp:


    def __init__(self, root):
        
        self.window_width = root.winfo_screenwidth()
        self.window_height = root.winfo_screenheight()
        
        self.width = 400
        self.height = 700
        
        self.block_width = 360
        self.block_height = 120
        
        self.x = self.window_width - 200
        self.y = 200
        
        self.old_info = None
        
        
        self.last_update_time = time.time()
        self.update_interval = 0.01
        
        
        self.root = root
        self.root.title('Color Code')
        self.root.attributes("-topmost", True)

        self.initialize_window()
                
        threading.Thread(target=self.start_listener, daemon=True).start()
    
    
    def font(self, font_size=15):
        return font.Font(family='Andale Mono', size=font_size)
    
    
    ## =====================================================================
    ## 
    

    def initialize_window(self):
        
        # self.root.geometry(f'{self.width}x{self.height}+{self.x-self.width}+{self.y}')
        
        
        y = 20
        
        ## =====================================================================
        ## リアルタイム
        
        ## 画像
        self.around_image_realtime = tk.Canvas(self.root, width=self.block_width, height=self.block_height, bg='gray')
        self.around_image_realtime.place(x=20, y=y)
        
        ## RGB (リアルタイム)
        y += self.block_height + 20
        self.rgb_canvas_realtime = tk.Canvas(self.root, width=self.block_width, height=self.block_height, bg='gray')
        self.rgb_canvas_realtime.place(x=20, y=y)  
        
        y += self.block_height + 5
        self.red_realtime = tk.Label(self.root, text='R', font=self.font(), fg='pink')
        self.red_realtime.place(x=20, y=y)
        # y += 30
        self.green_realtime = tk.Label(self.root, text='G', font=self.font(), fg='limegreen')
        self.green_realtime.place(x=150, y=y)
        # y += 30
        self.blue_realtime = tk.Label(self.root, text='B', font=self.font(), fg='cyan')
        self.blue_realtime.place(x=280, y=y)
        
        y += 20
        self.color_code_realtime = tk.Label(self.root, text='RGB :', font=self.font())
        self.color_code_realtime.place(x=20, y=y)
        
        y += 20
        self.hsv_realtime = tk.Label(self.root, text='HSV : ', font=self.font())
        self.hsv_realtime.place(x=20, y=y)
        
        
        ## =====================================================================
        ## Shift
        
        
        y += 60
        self.around_image_pressed = tk.Canvas(self.root, width=self.block_width, height=self.block_height, bg='gray')
        self.around_image_pressed.place(x=20, y=y)
        
        
        y += self.block_height + 20
        self.rgb_canvas_pressed = tk.Canvas(self.root, width=self.block_width, height=self.block_height, bg='gray')
        self.rgb_canvas_pressed.place(x=20, y=y)  
        
        y += self.block_height + 5
        self.red_pressed = tk.Label(self.root, text='R', font=self.font(), fg='pink')
        self.red_pressed.place(x=20, y=y)
        # y += 30
        self.green_pressed = tk.Label(self.root, text='G', font=self.font(), fg='limegreen')
        self.green_pressed.place(x=150, y=y)
        # y += 30
        self.blue_pressed = tk.Label(self.root, text='B', font=self.font(), fg='cyan')
        self.blue_pressed.place(x=280, y=y)
        
        y += 20
        self.color_code_pressed = tk.Label(self.root, text='RGB : ', font=self.font())
        self.color_code_pressed.place(x=20, y=y)
        
        y += 20
        self.hsv_pressed = tk.Label(self.root, text='HSV : ', font=self.font())
        self.hsv_pressed.place(x=20, y=y)
    
        y += 40
        self.root.geometry(f'{self.width}x{y}+{self.x-self.width}+{self.y}')
    
    ## =====================================================================
    ## 
    
    
    def start_listener(self):
        
        with mouse.Listener(
                on_move=self.on_move
            ) as mouse_listener, \
            keyboard.Listener(
                on_press=self.on_press,
            ) as keyboard_listener:
            
            mouse_listener.join()
            keyboard_listener.join()
    

    def on_move(self, x, y, *args):
        
        if time.time() - self.last_update_time < self.update_interval:
            return 
        
        color, around_pixels = self.get_image(x, y)
        
        self.update_color_display(color, pressed=False, around_pixels=around_pixels)
    
    
    def on_press(self, key):
        
        if key in [keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.space]:
            
            if time.time() - self.last_update_time < self.update_interval:
                color, around_pixels = self.old_info
            else:
                color, around_pixels = self.get_image(pyautogui.position().x, pyautogui.position().y)
                
            self.update_color_display(color, pressed=True, around_pixels=around_pixels)
            
    
    ## =====================================================================
    ## 
    
    
    def get_image(self, x, y):
        
        x, y = int(x), int(y)
        
        pixel = ImageGrab.grab(bbox=(x, y, x+1, y+1))
        color = pixel.getpixel((0, 0))
        
        around_pixels = ImageGrab.grab(bbox=(x-self.block_width//4, y-self.block_height//4, x+self.block_width//4, y+self.block_height//4))
        around_pixels = around_pixels.resize((self.block_width+3, self.block_height+3))
        
        self.old_info = (color, around_pixels)
        
        return color, around_pixels
    
    
    def update_color_display(self, color, pressed, around_pixels=None):
        self.last_update_time = time.time()
        self.root.after(0, lambda: self.update_gui(color, pressed, around_pixels))


    def update_gui(self, color, pressed, around_pixels=None):
        

        color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

        h, s, v = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
        color_hsv = (int(h*360), int(s*100), int(v*100))
        
        brightness = (color[0] + color[1] + color[2]) / 3

        
        if pressed:

            self.photo_pressed = ImageTk.PhotoImage(around_pixels)
            
            self.red_pressed.config(  text=f'R  {color[0]}')
            self.green_pressed.config(text=f'G  {color[1]}')
            self.blue_pressed.config( text=f'B  {color[2]}')
            
            self.color_code_pressed.config(text=f'RGB : {color[:3]}, {color_hex}')
            self.hsv_pressed.config(text=f'HSV : {color_hsv}')
            
            self.rgb_canvas_pressed.config(background=color_hex)

            self.around_image_pressed.delete('all')
            
            self.around_image_pressed.create_image(0, 0, image=self.photo_pressed, anchor=tk.NW)
            self.around_image_pressed.create_line(self.block_width//2, 0, self.block_width//2, self.block_height, fill='red') 
            self.around_image_pressed.create_line(0, self.block_height//2, self.block_width, self.block_height//2, fill='red')
            
            print(color)
        
        
        else:
            
            self.photo_realtime = ImageTk.PhotoImage(around_pixels)
            
            self.red_realtime.config(  text=f'R  {color[0]}')
            self.green_realtime.config(text=f'G  {color[1]}')
            self.blue_realtime.config( text=f'B  {color[2]}')
            
            self.color_code_realtime.config(text=f'RGB : {color[:3]}, {color_hex}')
            self.hsv_realtime.config(text=f'HSV : {color_hsv}')
            
            self.rgb_canvas_realtime.config(background=color_hex)

            self.around_image_realtime.delete('all')
            
            
            self.around_image_realtime.create_image(0, 0, image=self.photo_realtime, anchor=tk.NW)
            self.around_image_realtime.create_line(self.block_width//2, 0, self.block_width//2, self.block_height, fill='red') 
            self.around_image_realtime.create_line(0, self.block_height//2, self.block_width, self.block_height//2, fill='red')
        
        

## =====================================================================
## 


def main():
    root = tk.Tk()
    app = ColorApp(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()
