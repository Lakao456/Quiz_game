import os
import json
import time
import pickle
import hashlib
import threading
from tkinter import *
import mysql.connector
from functools import partial
from PIL import ImageTk, Image
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkinter.scrolledtext import *

global subject
theme, timeLimit = 'Light', 100
marks, name, admin, submitted, newQuesType = 0, '', False, False, ''

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


def switchUser():
    global admin
    if admin:
        admin = False
        userEntry.config(show='')
        adminButton.config(bg='#F0F0F0')
        titleLabel.config(text='Enter your name')
    else:
        admin = True
        userEntry.config(show='*')
        adminButton.config(bg='#0CFC0C')
        titleLabel.config(text='Enter the password')


def switchTheme():
    global theme
    if theme == 'Light':
        theme = 'Dark'
        themeButton.configure(text=theme, fg='#BB86FC', bg='#202020')
    else:
        theme = 'Light'
        themeButton.configure(text=theme, fg='#6200EE', bg='#f2f2f2')


def themeCol(dark, light):
    if theme == 'Dark':
        return dark
    else:
        return light


def insert_image(imageObject, image, adjW=0, adjH=0):
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        nImage = copyOfImage.resize((new_width + adjW, new_height + adjH), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(nImage)
        imageObject.config(image=photo)
        imageObject.image = photo

    inImage = Image.open(image)
    copyOfImage = inImage.copy()
    imageObject.config(image=ImageTk.PhotoImage(inImage), borderwidth=0)
    imageObject.bind('<Configure>', resize_image)


def timer(sec):
    while sec > 0 and not submitted:
        min = sec // 60
        timerLabel.config(text=f"{min if min > 9 else '0' + str(min)}:{sec if sec > 9 else '0' + str(sec)}")
        time.sleep(1)
        sec -= 1


def setSub(sub):
    global subject, name
    if admin:
        if hashlib.md5(userEntry.get().encode()).hexdigest() == pickle.load(open("password.DAT", 'rb')):
            subject = sub
            startMenu.destroy()
            startMenu.quit()
        else:
            window = Tk()
            window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
            window.withdraw()

            messagebox.showinfo(title='Score', message='incorrect Password')

            window.deiconify()
            window.destroy()
    else:
        subject, name = sub, userEntry.get()
        startMenu.destroy()
        startMenu.quit()


def displayQues(qNum):
    global questionNumberLabel, questionStatementLabel, optionsFrame, numOfQues
    for i in range(numOfQues):
        qBtnList[i].config(bg=themeCol('#2d2d2d', '#CCCCCC') if i == qNum else themeCol('#2d2d2d', '#fff'))
    questionNumberLabel.configure(text=f'Q {qNum + 1:d}.')
    questionStatementLabel.config(text=sql(f"SELECT question FROM {subject} WHERE Q_num = {qNum + 1:d}")[0][0],
                                  font=('Arial', 20))

    qType = sql(f"SELECT qType FROM {subject} WHERE Q_num = {qNum + 1};")[0][0]
    for i in range(numOfQues):
        for j in qElements[i].keys():
            qElements[i][j].place_forget()

    if admin:
        qElements[qNum]['qEntry'].place(relx=0.25, rely=0.17, relheight=0.08, relwidth=0.72, anchor='nw')
        qElements[qNum]['delBtn'].place(relx=0.34, rely=0.878, relheight=0.075, relwidth=0.075, anchor='nw')
        if qType == 'mcq':
            for i in range(4):
                qElements[qNum][f'opBtnLabel{i}'].place(relx=(0.05 - 0.005 if i % 2 == 0 else 0.55 - 0.005),
                                                        rely=(0.05 - 0.005 if i <= 1 else 0.525 - 0.005),
                                                        relwidth=0.3 + 0.01, relheight=0.2 + 0.013)

                qElements[qNum][f'opLabel{i}'].place(relx=(0.05 if i % 2 == 0 else 0.55),
                                                     rely=(0.05 if i <= 1 else 0.525),
                                                     relwidth=0.3, relheight=0.2)

                qElements[qNum][f'opEntry{i}'].place(relx=(0.05 if i % 2 == 0 else 0.55),
                                                     rely=(0.275 if i <= 1 else 0.75),
                                                     relwidth=0.3, relheight=0.2)

                qElements[qNum][f'opBtn{i}'].place(relx=(0.375 if i % 2 == 0 else 0.875),
                                                   rely=(0.05 if i <= 1 else 0.525),
                                                   relwidth=0.1, relheight=0.45)

        elif qType == 'true/false':
            for i in range(2):
                qElements[qNum][f'opBtnLabel{i}'].place(relx=(0.05 - 0.005 if i == 0 else 0.55 - 0.005),
                                                        rely=0.2 - 0.005,
                                                        relwidth=0.4 + 0.01,
                                                        relheight=0.4 + 0.013)

                qElements[qNum][f'opBtn{i}'].place(relx=(0.05 if i == 0 else 0.55), rely=0.2, relwidth=0.4,
                                                   relheight=0.4)
        else:
            qElements[qNum]['opLabel'].place(relx=0.1, rely=0.1, relwidth=0.8,
                                             relheight=0.2)
            qElements[qNum]['opEntry'].place(relx=0.1, rely=0.4, relwidth=0.8,
                                             relheight=0.2)
    else:

        if qType == 'mcq':
            for i in range(4):
                qElements[qNum][f'opBtnLabel{i}'].place(relx=(0.05 - 0.005 if i % 2 == 0 else 0.55 - 0.005),
                                                        rely=(0.05 - 0.005 if i <= 1 else 0.5 - 0.005),
                                                        relwidth=0.4 + 0.01, relheight=0.4 + 0.013)

                qElements[qNum][f'opBtn{i}'].place(relx=(0.05 if i % 2 == 0 else 0.55), rely=(0.05 if i <= 1 else 0.5),
                                                   relwidth=0.4, relheight=0.4)

        elif qType == 'true/false':
            for i in range(2):
                qElements[qNum][f'opBtnLabel{i}'].place(relx=(0.05 - 0.005 if i == 0 else 0.55 - 0.005),
                                                        rely=0.2 - 0.005,
                                                        relwidth=0.4 + 0.01,
                                                        relheight=0.4 + 0.013)

                qElements[qNum][f'opBtn{i}'].place(relx=(0.05 if i == 0 else 0.55), rely=0.2, relwidth=0.4,
                                                   relheight=0.4)
        else:
            qElements[qNum]['opLabel'].place(relx=0.1, rely=0.1, relwidth=0.8,
                                             relheight=0.2)
            qElements[qNum]['opEntry'].place(relx=0.1, rely=0.4, relwidth=0.8,
                                             relheight=0.2)


def recordAns(qNum, ans):
    answers[qNum], qType = ans, sql(f"SELECT qType FROM {subject} WHERE Q_num = {qNum + 1:d};")[0][0]
    if qType in 'mcq':
        for i in range(4):
            qElements[qNum][f'opBtnLabel{i}'].config(
                bg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#3C4042', '#8d8d8d')),
                fg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#fff', '#121212')))

            if admin:
                qElements[qNum][f'opLabel{i}'].config(
                    bg=(themeCol('#251F2D', '#EDE7F6') if i == ans else themeCol('#121212', '#FFF')),
                    fg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#fff', '#121212')))

                qElements[qNum][f'opBtn{i}'].config(
                    bg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#3C4042', '#8d8d8d')),
                    fg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#fff', '#121212')))
            else:
                qElements[qNum][f'opBtn{i}'].config(
                    bg=(themeCol('#251F2D', '#EDE7F6') if i == ans else themeCol('#121212', '#FFF')),
                    fg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#fff', '#121212')))

    if qType in 'true/false':
        for i in range(2):
            qElements[qNum][f'opBtnLabel{i}'].config(
                bg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#3C4042', '#8d8d8d')))
            qElements[qNum][f'opBtn{i}'].config(
                bg=(themeCol('#251F2D', '#EDE7F6') if i == ans else themeCol('#121212', '#FFF')),
                fg=(themeCol('#BB86FC', '#6200EE') if i == ans else themeCol('#fff', '#121212')))


def submit():
    global submitted
    if not submitted:
        submitted = True

        if admin:
            for qNum in range(numOfQues):
                newQuesStatement = qElements[qNum]['qEntry'].get('1.0', 'end-1c')

                if newQuesStatement.strip() != '':
                    SQL.execute(f"UPDATE {subject} SET question = '{newQuesStatement}' WHERE Q_num = {qNum + 1:d}")

                qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, qNum + 1))[0][0]
                if qType == 'mcq':
                    for eNum in range(4):
                        newOption = qElements[qNum][f'opEntry{eNum}'].get()
                        if newOption.strip() != '':
                            SQL.execute(
                                f"UPDATE {subject} SET option{chr(65 + eNum)} = '{newOption}' WHERE Q_num = {qNum + 1:d}")
                    if answers[qNum] is not None:
                        SQL.execute(
                            f"UPDATE {subject} SET answer = '{chr(65 + answers[qNum]).lower()}' WHERE Q_num = {qNum + 1:d}")

                elif qType == 'true/false' and answers[qNum] is not None:
                    SQL.execute(f"UPDATE {subject} SET answer = '{answers[qNum]}' WHERE Q_num = {qNum + 1:d}")

                elif qType == 'oneWord':
                    if qElements[qNum]['opEntry'].get().strip() != '':
                        answers[qNum] = qElements[qNum]['opEntry'].get()
                        SQL.execute(f"UPDATE {subject} SET answer = '{answers[qNum]}' WHERE Q_num = {qNum + 1:d}")
            quizAppDB.commit()
            quizMain.quit()
            sys.exit()

        else:
            global marks, name, pie
            pie = {'Correct': 0, 'Wrong': 0, 'Unattempted': numOfQues}
            for qNum in range(numOfQues):

                qType = sql(f"SELECT qType FROM {subject} WHERE Q_num = {qNum + 1:d};")[0][0]
                if qType == 'mcq':
                    try:
                        answers[qNum] = chr(97 + answers[qNum])
                    except TypeError:
                        answers[qNum] = None

                elif qType == 'oneWord':
                    if qElements[qNum]['opEntry'].get().strip() != '':
                        answers[qNum] = qElements[qNum]['opEntry'].get().lower()

                if answers[qNum] == sql(f"SELECT answer FROM {subject} WHERE Q_num = {qNum + 1:d}")[0][0].lower():
                    marks += 4
                    pie['Correct'] += 1
                    pie['Unattempted'] -= 1

                elif answers[qNum] is not None:
                    marks -= 1
                    pie['Wrong'] += 1
                    pie['Unattempted'] -= 1

            window = Tk()
            window.eval(f'tk::PlaceWindow {window.winfo_toplevel()} center')
            window.withdraw()

            if (
                    0 if not scores[subject] else (
                            max([scores[subject][i]['score'] for i in range(len(scores[subject]))]))) >= marks:
                messagebox.showinfo(title='Score', message=f'Your Score is {marks:d} !')
            else:
                messagebox.showinfo(title='Score', message=f'NEW TOP SCORE ! \nYour Score is {marks:d}')

            window.deiconify()
            window.destroy()
            window.quit()

            scores[subject].append({"name": name, "score": marks})

            with open("ScoresTEMP.json", 'w') as tempFile:
                json.dump(scores, tempFile, indent=4)

            os.remove("Scores.json")
            os.rename(r'ScoresTEMP.json', r'Scores.json')

            quizMain.destroy()
            quizMain.quit()

            plt.pie([pie['Correct'], pie['Wrong'], pie['Unattempted']], labels=pie.keys(), autopct='%.2f',
                    explode=[0.05, 0.05, 0], colors=['#99ff99', '#ff9999', '#66b3ff'])

            plt.show()
            sys.exit()


def addQues():
    global numOfQues, qBtnY, newQuesType, qElements

    def setTyp(type):
        global newQuesType
        newQuesType = type
        quesType.destroy()
        quesType.quit()

    quesType = Tk()
    quesType.title('TESTS')
    quesType.geometry('400x400')
    quesType.configure(bg="#000")

    typeTopFrame = Frame(quesType, bg='#85c6dd')
    typeTopFrame.place(relx=0.1, rely=0.03, relheight=0.3, relwidth=0.8)

    typeTitleLabel = Label(typeTopFrame, text='Select Question\n Type', bg='#85c6dd', fg='#fff',
                           font=('Autobus-Bold', 20))
    typeTitleLabel.place(relx=0.1, rely=0.07, relheight=0.8, relwidth=0.8)

    typeMidFrame = Frame(quesType, bg='#85c6dd')
    typeMidFrame.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.6, anchor='nw')

    y = 0.12
    typeButtons = ['mcq', 'true/false', 'one Word']
    for i in range(len(typeButtons)):
        typeButtons[i] = Button(typeMidFrame, text=typeButtons[i].upper(), font=('Autobus', 15),
                                command=partial(setTyp, typeButtons[i].replace(" ", "")))
        typeButtons[i].place(relx=0.1, rely=y, relwidth=0.8, relheight=0.2)
        y += 0.25

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit()

    quesType.protocol("WM_DELETE_WINDOW", on_closing)
    quesType.mainloop()

    qBtnList.append(
        Button(questionButtonsFrame, text=str(numOfQues + 1), relief='ridge', fg=themeCol('#fff', '#1c1c1c'),
               bg=themeCol('#2d2d2d', '#fff'),
               command=partial(displayQues, numOfQues)))
    qBtnList[numOfQues].place(relx=(0.03 if numOfQues % 2 == 0 else 0.5), rely=qBtnY, relwidth=0.45, relheight=0.085)
    if numOfQues % 2 != 0: qBtnY += 0.1
    numOfQues += 1

    SQL.execute(
        f"INSERT INTO {subject} VALUES({numOfQues}, 'Question Statement', '{newQuesType}', NULL, NULL, NULL, NULL, 'a')")
    quizAppDB.commit()
    qElements.append({})
    answers.append(None)
    createOpElemAdmin(numOfQues - 1)


def delQues(qNum):
    global qElements, numOfQues
    if messagebox.askokcancel("Delete Question", "Do you want to delete this question?"):
        SQL.execute(f'DELETE FROM {subject} WHERE Q_num = {qNum + 1}')
        for elem in qElements[qNum].keys():
            qElements[qNum][elem].place_forget()
            qBtnList[-1].place_forget()
        qBtnList.pop()
        qElements.pop(qNum)
        numOfQues -= 1
        displayQues(qNum - 1)
        for i in range(qNum, numOfQues):
            SQL.execute(f'UPDATE {subject} SET Q_num = {i + 1} WHERE Q_num = {i + 2}')
            qBtnList[i].config(command=partial(displayQues, i))
    quizAppDB.commit()


startMenu = Tk()
startMenu.title('START MENU')
startMenu.geometry('400x600')
startMenu.configure(bg="#000")  # 85c6dd

topFrame = Frame(startMenu, bg='#85c6dd')
topFrame.place(relx=0.1, rely=0.03, relheight=0.29, relwidth=0.8)

titleLabel = Label(topFrame, text='Enter your name', bg='#85c6dd', font=('Autobus', 18))
titleLabel.place(relx=0.1, rely=0.07, relheight=0.2, relwidth=0.8)

userEntry = Entry(startMenu, justify='center', font=('Arial', 15))
userEntry.place(relx=0.15, rely=0.12, relwidth=0.7, relheight=0.1, )

subtitleLabel = Label(topFrame, text='Select a subject to start', bg='#85c6dd', font=('Autobus', 15))
subtitleLabel.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.8)

midFrame = Frame(startMenu, bg='#85c6dd')
midFrame.place(relx=0.1, rely=0.34, relwidth=0.8, relheight=0.4, anchor='nw')

subButtons, y = ['maths', 'sci', 'gk'], 0.12

for i in range(len(subButtons)):
    highScore = (0 if not scores[subButtons[i]] else (
        max([scores[subButtons[i]][j]['score'] for j in range(len(scores[subButtons[i]]))])))
    highName = ('-' if not scores[subButtons[i]] else (
        max([scores[subButtons[i]][j]['name'] for j in range(len(scores[subButtons[i]]))])))

    subButtons[i] = Button(midFrame, text=subButtons[i].upper(), font=('Autobus', 15),
                           command=partial(setSub, subButtons[i]))
    subButtons[i].place(relx=0.02, rely=y, relwidth=0.5, relheight=0.2)

    highScoreLabel = Label(midFrame, bg='#ffffff', text=f'Top Score:: {highScore:d} \nBy {highName} ',
                           font=('Arial', 12))
    highScoreLabel.place(relx=0.55, rely=y, relwidth=0.42, relheight=0.2)
    y += 0.25

bottomFrame = Frame(startMenu, bg='#85c6dd')
bottomFrame.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.2, anchor='nw')

adminButton = Button(bottomFrame, text='Admin🔒', font=('Autobus', 16), command=switchUser)
adminButton.place(relx=0.02, rely=0.12, relwidth=0.47, relheight=0.76)

themeButton = Button(bottomFrame, text=theme, font=('Autobus', 16), command=partial(switchTheme))
themeButton.place(relx=0.52, rely=0.12, relwidth=0.47, relheight=0.76)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


startMenu.protocol("WM_DELETE_WINDOW", on_closing)
startMenu.mainloop()

quizMain = Tk()
quizMain.title(f'{subject.upper()} QUIZ')
quizMain.geometry('1000x700')

bgImage = Label(quizMain)
insert_image(bgImage, f"Assets\\{theme}_BG.png")
bgImage.place(relwidth=1, relheight=1)

questionNumberLabel = Label(quizMain, bg=themeCol('#202020', '#6200EE'), fg=themeCol('#f2f2f2', '#fff'),
                            font=('Montserrat', 50))
questionNumberLabel.place(relx=0.055, rely=0.085, relheight=0.17, relwidth=0.13, anchor='nw')

# qLen = len(sql("SELECT question FROM %s WHERE Q_num = 1" % subject)[0][0])
questionStatementLabel = Label(quizMain, bg=themeCol('#1b1b1b', '#fff'), anchor='nw',
                               fg=themeCol('#f2f2f2', '#1b1b1b'),
                               font=('Montserrat', 30))

questionButtonsFrame = Frame(quizMain, bg=themeCol('#202020', '#f2f2f2'))
questionButtonsFrame.place(relx=0.03, rely=0.3, relheight=0.64, relwidth=0.19, anchor='nw')

optionsFrame = Frame(quizMain, bg=themeCol('#121212', '#fff'))
optionsFrame.place(relx=0.25, rely=0.3, relheight=0.55, relwidth=0.72, anchor='nw')

numOfQues, answers, qElements = sql(f"SELECT max(Q_num) FROM {subject}")[0][0], [], []
for i in range(numOfQues):
    qElements.append({})
    answers.append(None)


def createOpElemAdmin(qNum):
    global qElements

    qElements[qNum]['delBtn'] = Button(quizMain, text='-', bg=themeCol('#BB86FC', '#6200EE'), fg='#fff',
                                       highlightthickness=0, bd=0, font=('Arial-Bold', 50),
                                       command=partial(delQues, qNum))

    qElements[qNum]['qEntry'] = ScrolledText(quizMain, bg=themeCol('#121212', '#fff'),
                                             fg=themeCol('#fff', '#121212'),
                                             insertbackground=themeCol('#fff', '#000'),
                                             font=('Montserrat', 15))
    qType = sql(f"SELECT qType FROM {subject} WHERE Q_num = {qNum + 1:d};")[0][0]
    if qType == 'mcq':
        for eNum in range(4):
            ansMatchMcq = (True if sql("SELECT answer FROM %s WHERE Q_num = %d" % (subject, qNum + 1))[0][0] == chr(
                65 + eNum).lower() else False)

            qElements[qNum][f'opBtnLabel{eNum}'] = Label(optionsFrame, bg=themeCol('#BB86FC', '#6200EE')
            if ansMatchMcq else themeCol('#3C4042', '#8d8d8d'))

            qElements[qNum][f'opLabel{eNum}'] = Label(optionsFrame, text=
            sql(f"SELECT option{chr(65 + eNum)} FROM {subject} WHERE Q_num = {qNum + 1:d}")[0][0],
                                                      bg=themeCol('#251F2D', '#EDE7F6') if ansMatchMcq
                                                      else themeCol('#121212', '#fff'),
                                                      highlightthickness=0, bd=0,
                                                      fg=themeCol('#fff', '#121212'), font=('Montserrat', 18))

            qElements[qNum][f'opEntry{eNum}'] = Entry(optionsFrame, bg=themeCol('#121212', '#fff'),
                                                      fg=themeCol('#fff', '#121212'),
                                                      insertbackground=themeCol('#fff', '#000'),
                                                      font=('Montserrat', 13))

            qElements[qNum][f'opBtn{eNum}'] = Button(optionsFrame,
                                                     bg=themeCol('#BB86FC', '#6200EE') if ansMatchMcq
                                                     else themeCol('#3C4042', '#8d8d8d'),
                                                     highlightthickness=0, bd=0,
                                                     command=partial(recordAns, qNum, eNum))

    elif qType == 'true/false':
        tfL = ['t', 'f']
        for eNum in range(2):
            ansMatchTf = (True if sql("SELECT answer FROM %s WHERE Q_num = %d" % (subject, qNum + 1))[0][0] == tfL[
                eNum] else False)

            qElements[qNum][f'opBtnLabel{eNum}'] = Label(optionsFrame, bg=themeCol('#BB86FC', '#6200EE') if
            ansMatchTf else themeCol('#fff', '#121212'))

            qElements[qNum][f'opBtn{eNum}'] = Button(optionsFrame, text=('True' if eNum == 0 else 'False'),
                                                     bg=themeCol('#251F2D', '#EDE7F6') if
                                                     ansMatchTf else themeCol('#121212', '#fff'),
                                                     fg=themeCol('#BB86FC', '#6200EE') if
                                                     ansMatchTf else themeCol('#fff', '#121212'),
                                                     highlightthickness=0, bd=0,
                                                     font=('Montserrat', 18),
                                                     command=partial(recordAns, qNum, eNum))
    else:
        qElements[qNum]['opLabel'] = Label(optionsFrame,
                                           text=f'Answer: {sql(f"SELECT answer FROM {subject} WHERE Q_num = {qNum + 1:d}")[0][0]}',
                                           bg=themeCol('#121212', '#fff'),
                                           fg=themeCol('#fff', '#121212'), font=('Montserrat', 20))
        qElements[qNum]['opEntry'] = Entry(optionsFrame, bg=themeCol('#121212', '#fff'),
                                           fg=themeCol('#fff', '#121212'),
                                           insertbackground=themeCol('#fff', '#000'),
                                           font=('Montserrat', 17))


if admin:
    questionStatementLabel.place(relx=0.25, rely=0.07, relheight=0.12, relwidth=0.72, anchor='nw')
    for qNum in range(numOfQues):
        createOpElemAdmin(qNum)
else:
    for qNum in range(numOfQues):
        qType = sql(f"SELECT qType FROM {subject} WHERE Q_num = {qNum + 1:d};")[0][0]
        if qType == 'mcq':
            for eNum in range(4):
                qElements[qNum][f'opBtnLabel{eNum}'] = Label(optionsFrame, bg=themeCol("#3C4042", "#8d8d8d"))

                qElements[qNum][f'opBtn{eNum}'] = Button(optionsFrame, text=
                sql(f"SELECT option{chr(65 + eNum)} FROM {subject} WHERE Q_num = {qNum + 1:d}")[0][0],
                                                         bg=themeCol('#121212', '#fff'), highlightthickness=0, bd=0,
                                                         fg=themeCol('#fff', '#121212'), font=('Montserrat', 18),
                                                         command=partial(recordAns, qNum, eNum))

        elif qType == 'true/false':
            for eNum in range(2):
                qElements[qNum][f'opBtnLabel{eNum}'] = Label(optionsFrame, bg=themeCol("#3C4042", "#8d8d8d"))

                qElements[qNum][f'opBtn{eNum}'] = Button(optionsFrame, text=('True' if eNum == 0 else 'False'),
                                                         bg=themeCol('#121212', '#fff'),
                                                         highlightthickness=0, bd=0,
                                                         fg=themeCol('#fff', '#121212'), font=('Montserrat', 18),
                                                         command=partial(recordAns, qNum, (
                                                             't' if answers[qNum] == 0 else 'f' if answers[
                                                                                                       qNum] == 1 else None)))

        else:
            qElements[qNum]['opLabel'] = Label(optionsFrame, text='Enter your answer', bg=themeCol('#121212', '#fff'),
                                               fg=themeCol('#fff', '#121212'), font=('Montserrat', 14))
            qElements[qNum]['opEntry'] = Entry(optionsFrame, bg=themeCol('#121212', '#fff'),
                                               fg=themeCol('#fff', '#121212'),
                                               insertbackground=themeCol('#fff', '#000'),
                                               font=('Montserrat', 13))

submitButton = Button(quizMain, text=('APPLY' if admin else 'SUBMIT'), command=submit, bg='#03DAC6',
                      font=('Montserrat-ExtraBold', 25),
                      activebackground='#03DAC6', fg="#fff")
submitButton.place(relx=0.835, rely=0.87, relheight=0.095, relwidth=0.15, anchor='nw')

qBtnList, qBtnY = [], 0.005
for i in range(numOfQues):
    qBtnList.append(Button(questionButtonsFrame, text=str(i + 1), relief='ridge', fg=themeCol('#fff', '#1c1c1c'),
                           bg=themeCol('#2d2d2d', '#fff'),
                           command=partial(displayQues, i)))
    qBtnList[i].place(relx=(0.03 if i % 2 == 0 else 0.5), rely=qBtnY, relwidth=0.45, relheight=0.085)
    if i % 2 != 0:
        qBtnY += 0.1

if admin:
    questionStatementLabel.place(relx=0.25, rely=0.06, relheight=0.09, relwidth=0.72, anchor='nw')

    addButton = Button(quizMain, text='+', bg=themeCol('#BB86FC', '#6200EE'), fg='#fff', highlightthickness=0, bd=0,
                       font=('Montserrat-Semibold', 50), command=addQues)
    addButton.place(relx=0.26, rely=0.878, relheight=0.075, relwidth=0.075, anchor='nw')

else:
    questionStatementLabel.place(relx=0.25, rely=0.1, relheight=0.15, relwidth=0.72, anchor='nw')

    timerLabel = Label(text='00:00', bg=themeCol('#251F2D', '#3700B3'), font=('Montserrat-Semibold', 30), fg="#fff")
    timerLabel.place(relx=0.26, rely=0.87, relheight=0.095, relwidth=0.15, anchor='nw')

    startTime = threading.Timer(timeLimit, submit)
    startTime.start()

    timerThread = threading.Thread(target=partial(timer, timeLimit))
    timerThread.setDaemon(True)
    timerThread.start()

displayQues(0)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


quizMain.protocol("WM_DELETE_WINDOW", on_closing)
quizMain.mainloop()
