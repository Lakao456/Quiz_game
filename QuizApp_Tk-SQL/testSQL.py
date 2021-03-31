import sys
import time
from functools import partial
import threading
def func():
    print("This is the function you called")
    sys.exit()

def timer(seconds):
    while seconds > 0:
        print(f"{seconds//60}:{seconds}")
        time.sleep(1)
        seconds -= 1

startTime = threading.Timer(10, func)
startTime.start()

timerThread = threading.Thread(target=partial(timer, 10))
timerThread.start()

for _ in range(20):
    print('Running')
    time.sleep(1)

# timerThread.join()

# import mysql.connector
#
# quizAppDB = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="aman.singh456",
#     database="questions")
# SQL = quizAppDB.cursor()
#
# SQL.execute("USE questions;")
#
#
# def sql(exe=''):
#     SQL.execute(exe)
#     return SQL.fetchall()
#
#
# print([ans[0] for ans in sql("SELECT answer FROM maths")])

# import threading
#
#
# def fun():  # user defined function which adds +10 to given number
#
#     print("End of code")
#
#
# start_time = threading.Timer(5, fun)
# start_time.start()
#
# input('aa::')
from tkinter import *
from tkinter import ttk
import mysql.connector
from functools import partial
from PIL import ImageTk,Image



def insert_image(object, image, adjW=0, adjH=0):

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copyOfImage.resize((new_width+adjW, new_height+adjH), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        object.config(image=photo)
        object.image = photo

    inImage = Image.open(image)
    copyOfImage = inImage.copy()
    object.config(image = ImageTk.PhotoImage(inImage), borderwidth=0)
    object.bind('<Configure>', resize_image)



quiz_main = Tk()
quiz_main.title('TESTS')
quiz_main.geometry('1000x700')

bgImageLabel = ttk.Label(quiz_main)
insert_image(bgImageLabel, "Assets\\DarkTheme\\Dark_BG.png", )
bgImageLabel.place(relwidth=1, relheight=1)

btn = Button(quiz_main, bg='#1B1B1B', activebackground='#1B1B1B')
insert_image(btn, "Assets\\DarkTheme\\Dark_SubBtn_Hover.png")
btn.place(relx=0.82, rely=0.872, relheight=0.095, relwidth=0.15, anchor='nw')


mainloop()