from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()
root.title("Title")
root.geometry('1000x700')
root.configure(bg="#000")

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

image = Image.open("Assets\\DarkTheme\\Dark_BG.png")
copy_of_image = image.copy()
label = ttk.Label(root, image = ImageTk.PhotoImage(image))
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)

root.mainloop()