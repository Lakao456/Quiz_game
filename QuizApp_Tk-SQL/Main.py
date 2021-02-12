import json
import os
from functools import partial
from tkinter import *
from tkinter import messagebox

import matplotlib.pyplot as plt
import mysql.connector
from PIL import ImageTk, Image

global subject
marks, theme = 0, 'Light'

try:
    with open('Scores.json') as f:
        scores = json.load(f)
except FileNotFoundError:
    with open('Scores.json', 'w') as f:
        json.dump({"maths": [], "sci": [], "gk": []}, f, indent=4)
    with open('Scores.json') as f:
        scores = json.load(f)

quizAppDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345678",
    database="questions")
SQL = quizAppDB.cursor()

SQL.execute("USE questions;")


def sql(exe=''):
    SQL.execute(exe)
    return SQL.fetchall()


def switchTheme():
    global theme
    if theme == 'Light':
        theme = 'Dark'
        themeButton.configure(text=theme, fg='#BB86FC', bg='#202020')
    else:
        theme = 'Light'
        themeButton.configure(text=theme, fg='#6200EE', bg='#f2f2f2')


def admin():
    exec(open('Edit_ques_GUI.py').read())


def themeCol(dark, light):
    if theme == 'Dark':
        return dark
    else:
        return light


def insert_image(object, image, adjW=0, adjH=0):
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copyOfImage.resize((new_width + adjW, new_height + adjH), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        object.config(image=photo)
        object.image = photo

    inImage = Image.open(image)
    copyOfImage = inImage.copy()
    object.config(image=ImageTk.PhotoImage(inImage), borderwidth=0)
    object.bind('<Configure>', resize_image)


def setSub(sub, root):
    global subject, name
    subject, name = sub, nameEntry.get()
    print(subject)
    root.destroy()
    root.quit()


def displayQues(qNum):
    global question_number_label, question_statement_label, options_frame

    question_number_label.configure(text='Q %d.' % (qNum + 1))
    question_statement_label.config(text=sql("SELECT question FROM %s WHERE Q_num = %d" % (subject, qNum + 1)),
                                    font=('Arial', 20))

    for i in range(len(opElements)):
        for j in opElements[i]:
            j.place_forget()
    qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, qNum + 1))[0][0]
    if qType == 'mcq':
        for i in range(4):
            opElements[qNum][i].place(relx=(0.05 if i % 2 == 0 else 0.55), rely=(0.05 if i <= 1 else 0.5),
                                      relwidth=0.4, relheight=0.4)
    elif qType == 'true/false':
        for i in range(2): opElements[qNum][i].place(relx=(0.05 if i == 0 else 0.55), rely=0.2, relwidth=0.4,
                                                     relheight=0.4)
    else:
        for i in range(2): opElements[qNum][i].place(relx=0.1, rely=(0.1 if i == 0 else 0.4), relwidth=0.8,
                                                     relheight=0.2)


def recordAns(qNum, ans):
    answers[qNum], qType = ans, sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, qNum + 1))[0][0]
    if qType in 'mcq true/false':
        for i in range(len(opElements[qNum])):
            opElements[qNum][i].configure(bg=('#8c8c8c' if i == ans else '#fff'))
    print(answers)


def submit(root):
    global marks, name, pie
    pie = {'Correct': 0, 'Wrong': 0, 'Unattempted': len(answers)}
    for qNum in range(len(answers)):
        qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, qNum + 1))[0][0]
        if qType == 'mcq':
            answers[qNum] = chr(97 + answers[qNum])

        elif qType == 'true/false':
            answers[qNum] = ('t' if answers[qNum] == 0 else 'f' if answers[qNum] == 1 else None)
        else:
            if opElements[qNum][1].get() != '':
                answers[qNum] = opElements[qNum][1].get()

        if answers[qNum] == sql("SELECT answer FROM %s WHERE Q_num = %d" % (subject, qNum + 1))[0][0]:
            marks += 4
            pie['Correct'] += 1
            pie['Unattempted'] -= 1

        elif answers[qNum] != None:
            marks -= 1
            pie['Wrong'] += 1
            pie['Unattempted'] -= 1

    window = Tk()
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
    window.withdraw()

    if (
            0 if not scores[subject] else (
                    max([scores[subject][i]['score'] for i in range(len(scores[subject]))]))) >= marks:
        messagebox.showinfo(title='Score', message='Your Score is %d !' % marks)
    else:
        messagebox.showinfo(title='Score', message='NEW TOP SCORE ! \nYour Score is %d' % marks)

    window.deiconify()
    window.destroy()
    window.quit()

    scores[subject].append({"name": name, "score": marks})

    with open("ScoresTEMP.json", 'w') as tempFile:
        json.dump(scores, tempFile, indent=4)

    os.remove("Scores.json")
    os.rename(r'ScoresTEMP.json', r'Scores.json')

    root.destroy()
    root.quit()

    plt.pie([pie['Correct'], pie['Wrong'], pie['Unattempted']], labels=pie.keys(), autopct='%.2f',
            explode=[0.05, 0.05, 0], colors=['#99ff99', '#ff9999', '#66b3ff'])

    plt.show()


select_sub_main = Tk()
select_sub_main.title('TESTS')
select_sub_main.geometry('400x600')
select_sub_main.configure(bg="#000")  # 85c6dd

topFrame = Frame(select_sub_main, bg='#85c6dd')
topFrame.place(relx=0.1, rely=0.03, relheight=0.29, relwidth=0.8)

titleLabel = Label(topFrame, text='Enter your name', bg='#85c6dd', font=('Autobus', 18))
titleLabel.place(relx=0.1, rely=0.07, relheight=0.2, relwidth=0.8)

nameEntry = Entry(select_sub_main, justify='center', font=('Arial', 15))
nameEntry.place(relx=0.15, rely=0.12, relwidth=0.7, relheight=0.1, )

subtitleLabel = Label(topFrame, text='Select a subject to start', bg='#85c6dd', font=('Autobus', 15))
subtitleLabel.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.8)

midFrame = Frame(select_sub_main, bg='#85c6dd')
midFrame.place(relx=0.1, rely=0.34, relwidth=0.8, relheight=0.4, anchor='nw')

subButtons, y = ['maths', 'sci', 'gk'], 0.12
for i in range(len(subButtons)):
    highScore = (0 if not scores[subButtons[i]] else (
        max([scores[subButtons[i]][j]['score'] for j in range(len(scores[subButtons[i]]))])))
    highName = ('-' if not scores[subButtons[i]] else (
        max([scores[subButtons[i]][j]['name'] for j in range(len(scores[subButtons[i]]))])))

    subButtons[i] = Button(midFrame, text=subButtons[i].upper(), font=('Autobus', 15),
                           command=partial(setSub, subButtons[i], select_sub_main))
    subButtons[i].place(relx=0.02, rely=y, relwidth=0.5, relheight=0.2)

    highScoreLabel = Label(midFrame, bg='#ffffff', text='Top Score:: %d \nBy %s ' % (highScore, highName),
                           font=('Arial', 12))
    highScoreLabel.place(relx=0.55, rely=y, relwidth=0.42, relheight=0.2)
    y += 0.25

bottomFrame = Frame(select_sub_main, bg='#85c6dd')
bottomFrame.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.2, anchor='nw')

adminButton = Button(bottomFrame, text='Admin🔒', font=('Autobus', 16), command=partial(admin))
adminButton.place(relx=0.02, rely=0.12, relwidth=0.47, relheight=0.76)

themeButton = Button(bottomFrame, text=theme, font=('Autobus', 16), command=partial(switchTheme))
themeButton.place(relx=0.52, rely=0.12, relwidth=0.47, relheight=0.76)
switchTheme()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


select_sub_main.protocol("WM_DELETE_WINDOW", on_closing)
select_sub_main.mainloop()

quiz_main = Tk()
quiz_main.title('TESTS')
quiz_main.geometry('1000x700')

bgImage = Label(quiz_main)
insert_image(bgImage, f"Assets\\{theme}Theme\\{theme}_BG.png")
bgImage.place(relwidth=1, relheight=1)

question_number_label = Label(quiz_main, bg=themeCol('#202020', '#6200EE'), fg=themeCol('#f2f2f2', '#fff'),
                              font=('Montserrat', 50))
question_number_label.place(relx=0.065, rely=0.085, relheight=0.17, relwidth=0.13, anchor='nw')

# qLen = len(sql("SELECT question FROM %s WHERE Q_num = 1" % subject)[0][0])
question_statement_label = Label(quiz_main, bg=themeCol('#1b1b1b', '#fff'), anchor='nw',
                                 fg=themeCol('#f2f2f2', '#1b1b1b'),
                                 font=('Montserrat', 30))
question_statement_label.place(relx=0.25, rely=0.1, relheight=0.15, relwidth=0.72, anchor='nw')

question_buttons_frame = Frame(quiz_main, bg=themeCol('#202020', '#f2f2f2'))
question_buttons_frame.place(relx=0.03, rely=0.3, relheight=0.64, relwidth=0.19, anchor='nw')

options_frame = Frame(quiz_main, bg='#3c3c3c')
options_frame.place(relx=0.25, rely=0.3, relheight=0.47, relwidth=0.72, anchor='nw')

numOfQues, answers, opElements = sql("SELECT max(Q_num) FROM %s" % subject)[0][0], [], []
for i in range(numOfQues):
    opElements.append([])
    answers.append(None)

for qNum in range(numOfQues):

    qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, qNum + 1))[0][0]
    if qType == 'mcq':

        for bNum in range(4):
            opElements[qNum].append(Button(options_frame, text=
            sql("SELECT option%s FROM %s WHERE Q_num = %d" % (chr(65 + bNum), subject, qNum + 1))[0][0], bg='#fff',
                                           command=partial(recordAns, qNum, bNum)))

    elif qType == 'true/false':
        for bNum in range(2):
            opElements[qNum].append(Button(options_frame, text=('True' if bNum == 0 else 'False'), bg='#fff',
                                           command=partial(recordAns, qNum, bNum)))

    else:
        opElements[qNum].append(Label(options_frame, text='Enter your answer'))
        opElements[qNum].append(Entry(options_frame))

submit_button = Button(quiz_main, command=partial(submit, quiz_main), bg=themeCol('#1B1B1B', '#f2f2f2'),
                       activebackground=themeCol('#1B1B1B', '#f2f2f2'))
insert_image(submit_button, f"Assets\\{theme}Theme\\{theme}_SubBtn_Hover.png")
submit_button.place(relx=0.81, rely=0.87, relheight=0.095, relwidth=0.15, anchor='nw')

displayQues(0)

qBtnLen, qBtnList, y = numOfQues, [], 0.005
for i in range(qBtnLen):
    qBtnList.append(Button(question_buttons_frame, text=str(i + 1), relief='ridge', command=partial(displayQues, i)))
    qBtnList[i].place(relx=(0.03 if i % 2 == 0 else 0.5), rely=y, relwidth=0.45, relheight=0.085)
    if i % 2 != 0: y += 0.1


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


quiz_main.protocol("WM_DELETE_WINDOW", on_closing)
quiz_main.mainloop()
