from tkinter import *

from PIL import Image, ImageTk


def animate(counter):
    canvas.itemconfig(image, image=sequence[counter])
    root.after(20, lambda: animate((counter + 1) % len(sequence)))


root = Tk()
root.geometry('400x400')
root.configure(bg="#000")

canvas = Canvas(master=root, width=400, height=400)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

sequence = [ImageTk.PhotoImage(Image.open(r'DarkLight-%d.png' % i)) for i in range(176)]
# sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(r'DarkLight.gif'))]

image = canvas.create_image(200, 200, image=sequence[0])

animate(1)

mainloop()
