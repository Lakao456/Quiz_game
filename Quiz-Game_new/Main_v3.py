from tkinter import *
from tkinter import messagebox
import time
import winsound
from functools import partial
import sys

global questions, subject
score, answers, op_buttons = 0, [], {}


def create_buttons(root, parent_frame, buttons_list, column_num=1, job='select_sub'):
    global b_height, text, answers, questions

    def set_sub(n):
        global subject
        subject = buttons_list[n]
        for i in range(len(questions[subject])):
            answers.append(None)
        root.quit()
        root.destroy()

    def button_click(n=0):
        click_sound()
        if "sub" in job.lower():
            buttons[n].config(command=set_sub(n))
        elif "ques" in job.lower():
            buttons[n].config(command=display_ques(n))

    if len(buttons_list) % 2 == 0:
        buttons_qty = len(buttons_list)
    else:
        buttons_qty = len(buttons_list) + 1

    buttons, left_i, right_i = [], 0, 0

    for i in range(len(buttons_list)):

        if "ques" in job.lower():
            text = str(i + 1)
        elif "sub" in job.lower():
            text = buttons_list[i]

        if column_num == 2:
            b_height = 1.88 / buttons_qty
            if i % 2 == 0:
                left_i += 1
                buttons.append(
                    Button(parent_frame, text=text, bg="#8c8c8c", font=('Autobus Bold', 20),
                           relief=GROOVE,
                           command=partial(button_click, i)))
                buttons[-1].place(relx=0.01,
                                  rely=0.01 + (0.005 + b_height) * (left_i - 1),
                                  relheight=b_height,
                                  relwidth=0.485)
            else:
                right_i += 1
                buttons.append(
                    Button(parent_frame, text=text, bg="#8c8c8c", font=('Autobus Bold', 20),
                           relief=GROOVE,
                           command=partial(button_click, i)))
                buttons[-1].place(relx=0.505,
                                  rely=0.01 + (0.005 + b_height) * (left_i - 1),
                                  relheight=b_height,
                                  relwidth=0.485)
        elif column_num == 1:
            b_height = 1.3 / buttons_qty
            buttons.append(Button(parent_frame, text=text, bg="#8c8c8c", font=('Autobus Bold', 20),
                                  relief=GROOVE,
                                  command=partial(button_click, i)))
            buttons[-1].place(relx=0.1,
                              rely=0.01 + (0.005 + b_height) * i,
                              relheight=b_height,
                              relwidth=0.8)


def click_sound():
    winsound.PlaySound(".\\Resources\\Sounds\\Click.wav", winsound.SND_ASYNC)


def stop_watch():
    global start_time
    time_str = (time.time() - start_time) // 1
    time_label.config(text=time_str)
    time_label.after(1000, stop_watch)


def del_buttons(ques_num):
    global op_buttons
    for i in range(len(op_buttons)):
        print(op_buttons)
        try:
            op_buttons[ques_num][i].place_forget()
        except:
            print('o')


def create_lists():
    for ques_num in range(len(questions[subject])):
        if questions[subject][ques_num]['type'] == 'mcq':
            op_buttons[ques_num] = {'status': 0, 'button': []}
            for btn_num in range(4):
                x = lambda a: questions[subject][ques_num][a]
                op_buttons[ques_num]['button'].append(Button(options_frame, text=x('option' + chr(65+btn_num)),
                                    command=partial(store_ans, ques_num, chr(97 + btn_num), btn_num+1)))
        elif questions[subject][ques_num]['type'] == 'true/false':
            op_buttons[ques_num] = {'status': 0, 'button': []}
            op_buttons[ques_num]['button'].append(Button(options_frame, text='TRUE',
                                command=partial(store_ans, ques_num, 'true', 0)))
            op_buttons[ques_num]['button'].append(Button(options_frame, text='TRUE',
                                command=partial(store_ans, ques_num, 'true', 1)))
    print(op_buttons)
        # elif 'type' == 'true/false':f


def store_ans(ques_num, ans=None, btn=None):
    for i in range(op_buttons[ques_num]['button']):
        if op_buttons[ques_num]['status'] == 0: # if button is inactive
            op_buttons[ques_num]['status'] = btn
            colour = '#0c0c0c'
        elif op_buttons[ques_num]['status'] == btn: 
            op_buttons[ques_num]['status'] = 0
            colour = '#5c5c5c'
    global answers, questions
    op_buttons[ques_num][btn]['status'] = 1
    if questions[subject][ques_num]['type'] == 'mcq':
        if questions[subject][ques_num]['type'] == ans:
            answers[ques_num] = 'Correct'
        else:
            answers[ques_num] = 'Wrong'


    # else:
    #     print('count=0')
    #     op_buttons[btn].config(bg='#5c5c5c')
    #     active_button[ques_num] = 1
    #     if ans == questions[subject][ques_num]["answer"]:
    #         answers[ques_num] = 'correct'
    #     else:
    #         answers[ques_num] = 'wrong'
    # print(active_button, answers)


def display_ques(ques_num):
    global questions, ex_buttons
    question_number_label.config(text="Q) " + str(ques_num + 1))
    question_statement = questions[subject][ques_num]["question"]
    question_statement_label.config(text=question_statement, font=('Arial', 20))  # 1200//len(question_statement)

    # if active_button[ques_num] == 1:
    #     colour = '#5c5c5c'
    # elif active_button[ques_num] == 0:
    #     colour = '#6c6c6c'

    if questions[subject][ques_num]['type'] == 'mcq':
        del_buttons(ques_num)
        y = lambda b: op_buttons[ques_num]['button'][b]
        y(0).place(relx='0.05', rely='0.05', relwidth='0.4', relheight='0.4')
        y(1).place(relx='0.55', rely='0.05', relwidth='0.4', relheight='0.4')
        y(2).place(relx='0.05', rely='0.50', relwidth='0.4', relheight='0.4')
        y(3).place(relx='0.55', rely='0.50', relwidth='0.4', relheight='0.4')

    elif questions[subject][ques_num]['type'] == 'true/false':
        del_buttons(ques_num)
        b_true = Button(options_frame, text="TRUE")
        b_true.place(relx='0.05', rely='0.2', relwidth='0.4', relheight='0.4')

        b_false = Button(options_frame, text="FALSE")
        b_false.place(relx='0.55', rely='0.2', relwidth='0.4', relheight='0.4')

        ex_buttons = [b_true, b_false]

    elif questions[subject][ques_num]['type'] == 'one word':
        del_buttons(ques_num)

        one_word_label = Label(options_frame, text='Enter your answer')
        one_word_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)

        ans_entry = Entry(options_frame)
        ans_entry.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)

        enter_ans_button = Button(options_frame, text='ENTER', font=('Arial', 20))
        enter_ans_button.place(relx=0.25, rely=0.7, relwidth=0.45, relheight=0.2)

        ex_buttons = [one_word_label, ans_entry, enter_ans_button]


play = True
while play:
    select_sub_main = Tk()
    select_sub_main.title('TESTS')
    select_sub_main.geometry('400x400')
    select_sub_main.configure(bg="#85c6dd")

    select_subject_label = Label(select_sub_main, text='Which subject do you want to chose ?', bg='#ffffff',
                                 font=('Arial', 17))
    select_subject_label.place(relx=0, rely=0.03, relheight=0.24, relwidth=1, anchor='nw')

    select_subject_frame = Frame(select_sub_main, bg='#fcfcfc')
    select_subject_frame.place(relx=0.35, rely=0.3, relheight=0.55, relwidth=0.30, anchor='nw')

    create_buttons(select_sub_main, select_subject_frame, list(questions.keys()), 1, 'select_sub')


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit()


    select_sub_main.protocol("WM_DELETE_WINDOW", on_closing)
    select_sub_main.mainloop()

    quiz_main = Tk()
    quiz_main.title('TESTS')
    quiz_main.geometry('1000x700')
    quiz_main.configure(bg="#85c6dd")

    quiz_main_frame = Frame(quiz_main, bg='#80c1ff')
    quiz_main_frame.place(relx=0.5, rely=0.15, relheight=0.8, relwidth=0.7, anchor='n')

    question_number_label = Label(quiz_main, bg='#80c1ff', font=('Arial', 30))
    question_number_label.place(relx=0.03, rely=0.03, relheight=0.24, relwidth=0.2, anchor='nw')

    question_statement_label = Label(quiz_main, bg='#ffcccc', anchor='nw',
                                     font=('Arial', 1200 // len(questions[subject][0]["question"])))
    question_statement_label.place(relx=0.25, rely=0.03, relheight=0.24, relwidth=0.72, anchor='nw')

    question_buttons_frame = Frame(quiz_main, bg='#fcfcfc')
    question_buttons_frame.place(relx=0.03, rely=0.3, relheight=0.6, relwidth=0.2, anchor='nw')

    options_frame = Frame(quiz_main, bg='#3c3c3c')
    options_frame.place(relx=0.25, rely=0.3, relheight=0.47, relwidth=0.72, anchor='nw')

    create_lists()
    display_ques(0)

    bottom_frame = Frame(quiz_main, bg='#0c0cff')
    bottom_frame.place(relx=0.25, rely=0.8, relheight=0.1, relwidth=0.72, anchor='nw')

    time_label = Label(bottom_frame, font=('calibri', 20, 'bold'),
                       background='purple',
                       foreground='white')
    time_label.place(relx=0.05, rely=0.1, relheight=0.8, relwidth=0.3, anchor='nw')

    done_button = Button(bottom_frame, text='DONE', font=('Arial', 30))
    done_button.place(relx=0.6, rely=0.1, relheight=0.8, relwidth=0.2, anchor='nw')

    create_buttons(quiz_main, question_buttons_frame, questions[subject], 2, 'select_ques')


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit()


    quiz_main.protocol("WM_DELETE_WINDOW", on_closing)
    quiz_main.mainloop()
