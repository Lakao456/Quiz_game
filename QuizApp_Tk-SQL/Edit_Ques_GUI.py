from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
from PIL import Image, ImageTk
import mysql.connector

global subject
marks, theme = 0, 'Light'

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


def setSub(sub, root):
    global subject
    if passEntry.get() == '':
        subject = sub
        root.destroy()
        root.quit()
    else:
        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()

        messagebox.showinfo(title='Error', message='incorrect Password')

        window.deiconify()
        window.destroy()


def displayQues(q_num):
    global questionNumberLabel, questionStatementLabel, optionsFrame, lastQuesEntry

    question_statement_entry[q_num].place(relx=0.25, rely=0.18, relheight=0.09, relwidth=0.72, anchor='nw')
    question_number_label.configure(text='Q %d' % (q_num + 1))
    question_statement_label.configure(text=sql("SELECT question FROM %s WHERE Q_num = %d" % (subject, q_num + 1)),
                                       font=('Arial', 20))
    for ques in range(len(opElements)):
        for op in range(len(opElements[ques])):
            qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, ques + 1))[0][0]
            if qType == 'mcq':
                for ele in range(3):
                    opElements[ques][op][ele].place_forget()
            else:
                for ele in range(len(opElements[ques])):
                    opElements[ques][ele].place_forget()

    qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, q_num + 1))[0][0]
    if qType == 'mcq':
        for opNum in range(4):
            opElements[q_num][opNum][0].place(relx=(0.05 if opNum % 2 == 0 else 0.55),
                                              rely=(0.05 if opNum <= 1 else 0.525),
                                              relwidth=0.3, relheight=0.2)

            opElements[q_num][opNum][1].place(relx=(0.05 if opNum % 2 == 0 else 0.55),
                                              rely=(0.275 if opNum <= 1 else 0.75),
                                              relwidth=0.3, relheight=0.2)

            opElements[q_num][opNum][2].place(relx=(0.375 if opNum % 2 == 0 else 0.875),
                                              rely=(0.05 if opNum <= 1 else 0.525),
                                              relwidth=0.1, relheight=0.45)

    elif qType == 'true/false':
        for i in range(2): opElements[q_num][i].place(relx=(0.05 if i == 0 else 0.55), rely=0.3, relwidth=0.4,
                                                      relheight=0.4)
    else:
        for i in range(3):
            opElements[q_num][i].place(relx=0.1, rely=0.1 * (i + 1) + (i * 0.2), relwidth=0.8,
                                       relheight=0.2)


def recordAns(q_num, ans):
    qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, q_num + 1))[0][0]
    if qType == 'mcq':
        answers[q_num] = ['a', 'b', 'c', 'd'][ans]
        for i in range(4):
            opElements[q_num][i][2].configure(bg=('#0cfc0c' if i == ans else '#8c8c8c'))
    else:
        answers[q_num] = ['t', 'f'][ans]
        for i in range(2):
            opElements[q_num][i].configure(bg=('#0cfc0c' if i == ans else '#8c8c8c'))


select_sub_main = Tk()
select_sub_main.title('TESTS')
select_sub_main.geometry('400x400')
select_sub_main.configure(bg="#000")  # 85c6dd

topFrame = Frame(select_sub_main, bg='#85c6dd')
topFrame.place(relx=0.1, rely=0.03, relheight=0.3, relwidth=0.8)

titleLabel = Label(topFrame, text='Enter the password', bg='#85c6dd', fg='#fff', font=('Autobus-Bold', 25))
titleLabel.place(relx=0.1, rely=0.07, relheight=0.2, relwidth=0.8)

passEntry = Entry(select_sub_main, justify='center', font=('Arial', 15), show='*')
passEntry.place(relx=0.15, rely=0.12, relwidth=0.7, relheight=0.1, )

subtitleLabel = Label(topFrame, text='Select a subject to start', bg='#85c6dd', font=('Autobus', 15))
subtitleLabel.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.8)

midFrame = Frame(select_sub_main, bg='#85c6dd')
midFrame.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.6, anchor='nw')

subButtons = ['maths', 'sci', 'gk']
y = 0.13
for i in range(len(subButtons)):
    subButtons[i] = Button(midFrame, text=subButtons[i].upper(), font=('Autobus', 15),
                           command=partial(setSub, subButtons[i], select_sub_main))
    subButtons[i].place(relx=0.02, rely=y, relwidth=0.96, relheight=0.2)
    y += 0.25


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


def submit(root):
    img = ImageTk.PhotoImage(Image.open('C:\\Users\\Aman\\PycharmProjects\\Quiz App\\QuizApp_Tk-SQL\\Assets\\DarkLightSwitch\\logo.jpg'))
    questionNumberLabel.configure(image = img)
    for q_num in range(numOfQues):
        qStatement = question_statement_entry[q_num].get('1.0', 'end-1c')
        qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, q_num + 1))[0][0]
        if qType == 'mcq' and not qStatement.isspace():
            SQL.execute("UPDATE %s SET question = '%s' WHERE Q_num = %d" % (subject, qStatement[q_num], q_num + 1))
            quizAppDB.commit()
            print(qStatement)
        elif qType == 'true/false' and not qStatement.isspace():
            print(qStatement)


select_sub_main.protocol("WM_DELETE_WINDOW", on_closing)
select_sub_main.mainloop()

answers = [ans[0] for ans in sql("SELECT answer FROM %s" % subject)]

quiz_main = Tk()
quiz_main.title('TESTS')
quiz_main.geometry('1000x700')
quiz_main.configure(bg="#85c6dd")
#, bg='#80c1ff'
questionNumberLabel = Label(quiz_main, font=('Arial', 30))
questionNumberLabel.place(relx=0.03, rely=0.03, relheight=0.24, relwidth=0.2, anchor='nw')

qLen = len(sql("SELECT question FROM %s WHERE Q_num = 1;" % subject)[0][0])
questionStatementLabel = Label(quiz_main, bg='#ffcccc', anchor='nw',
                               font=('Arial', 1200 // qLen))
questionStatementLabel.place(relx=0.25, rely=0.03, relheight=0.14, relwidth=0.72, anchor='nw')

question_buttons_frame = Frame(quiz_main, bg='#fcfcfc')
question_buttons_frame.place(relx=0.03, rely=0.3, relheight=0.6, relwidth=0.2, anchor='nw')

optionsFrame = Frame(quiz_main, bg='#3c3c3c')
optionsFrame.place(relx=0.25, rely=0.3, relheight=0.47, relwidth=0.72, anchor='nw')

numOfQues, opElements, question_statement_entry = sql("SELECT max(Q_num) FROM %s" % subject)[0][0], [], []
for i in range(numOfQues):
    opElements.append([])

for q_num in range(numOfQues):
    question_statement_entry.append(ScrolledText(quiz_main))
    qType = sql("SELECT qType FROM %s WHERE Q_num = %d;" % (subject, q_num + 1))[0][0]
    if qType == 'mcq':
        for opNum in range(4):
            opElements[q_num].append([])
            opElements[q_num][opNum].append(Label(optionsFrame, text=
            sql("SELECT option%s FROM %s WHERE Q_num = %d" % (chr(65 + opNum), subject, q_num + 1))[0][0]))
            opElements[q_num][opNum].append(Entry(optionsFrame))
            opElements[q_num][opNum].append(Button(optionsFrame, bg=themeCol('#BB86FC', '#6200EE') if
            sql("SELECT answer FROM %s WHERE Q_num = %d" % (subject, q_num + 1))[0][0] == chr(
                65 + opNum).lower() else themeCol('#3C4042', '#8d8d8d'), command=partial(recordAns, q_num, opNum)))
    elif qType == 'true/false':
        tfL = ['t', 'f']
        for bNum in range(2):
            opElements[q_num].append(Button(optionsFrame, text=('True' if bNum == 0 else 'False'), bg='#0cfc0c' if
            sql("SELECT answer FROM %s WHERE Q_num = %d" % (subject, q_num + 1))[0][0] == tfL[bNum] else '#8c8c8c',
                                            command=partial(recordAns, q_num, bNum)))

    else:
        opElements[q_num].append(Label(optionsFrame, text='Enter any new answer in the space given'))
        opElements[q_num].append(
            Label(optionsFrame, text=sql("SELECT answer FROM %s WHERE Q_num = %d" % (subject, q_num + 1))[0][0]))
        opElements[q_num].append(Entry(optionsFrame))

displayQues(0)

bottom_frame = Frame(quiz_main, bg='#0c0cff')
bottom_frame.place(relx=0.25, rely=0.8, relheight=0.1, relwidth=0.72, anchor='nw')

submit_button = Button(bottom_frame, text='SUBMIT', font=('Arial', 25), command=partial(submit, quiz_main))
submit_button.place(relx=0.6, rely=0.1, relheight=0.8, relwidth=0.2, anchor='nw')

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
