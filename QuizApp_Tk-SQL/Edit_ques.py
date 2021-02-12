import os
import json
import mysql.connector

quizAppDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345678",
    database="questions")
sql = quizAppDB.cursor()
line_break = '\n----------------------------------------------------------------------\n'



def checkInput(value_type, msg="Enter a value"):
    while True:
        value = input(msg + ':: ')

        if type(value_type) == type(1):
            try:
                value = int(value)
                if value not in range(1, value_type + 1):
                    print("**Invalid input**")
                else:
                    break
            except ValueError:
                print("**Invalid input**1")
        else: print("**Invalid input**1")

    return value


def addQues(subject):
    while True:
        mcq_op, ans_mcq, ans_tf, ans_ow = ["NUll", "NUll", "NUll", "NUll"], "NULL", "NULL", "NULL"
        in_question = input("\nEnter the question statement:-\n")

        types = ['mcq', 'true/false', 'oneWord']
        in_type = types[checkInput(3, line_break + \
                                   "\n1) MCQ"
                                   "\n2) True/False"
                                   "\n3) One Word"
                                   "\nEnter your choice") - 1]

        if 'mcq' in in_type:
            print(line_break)
            for i in range(4):
                mcq_op[i] = "'" + input("Enter option" + chr(65 + i) + " ::") + "'"
            ans_mcq = "'" + checkInput('mcq', line_break + 'Enter the answer(a/b/c/d)') + "'"
        elif 'true/false' in in_type:
            ans_tf = "'" + checkInput('true/false', line_break + 'Enter the answer(t/f)') + "'"
        elif 'oneWord' in in_type:
            ans_ow = "'" + input(line_break + "Enter the answer:: ") + "'"

        sql.execute("USE questions;")
        sql.execute("SELECT MAX(Q_num) FROM %s;" % subject)
        q_num = sql.fetchall()[0][0] + 1

        exe_str = "INSERT INTO %s VALUES(%d, '%s', '%s', %s, %s, %s, %s, %s, %s, %s);" \
                  % (
                      subject, q_num, in_question, in_type, mcq_op[0], mcq_op[1], mcq_op[2], mcq_op[3], ans_mcq, ans_tf,
                      ans_ow)

        sql.execute(exe_str)
        quizAppDB.commit()

        if 'n' in input("Do you want to add another question? (y/n):: ").lower():
            break

def delQues(subject):
    sql.execute("USE questions;")
    sql.execute("SELECT MAX(Q_num) FROM %s;" % subject)
    lastIndex = sql.fetchall()[0][0]
    while True:
        in_qNum = int(
            input(line_break + "Enter the question number to delete or enter '0' to view all the questions:: "))
        if in_qNum == 0:
            sql.execute("USE questions;")
            sql.execute("SELECT Q_num, question FROM %s ;" % subject)
            for p in sql.fetchall(): print(p)
        elif lastIndex >= in_qNum > 0:
            sql.execute("USE questions;")
            sql.execute("DELETE FROM %s WHERE Q_num = %d ;" % (subject, in_qNum))
            for i in range(in_qNum + 1, lastIndex + 1):
                x = i - 1
                sql.execute("UPDATE %s SET Q_num = %d WHERE Q_num = %d ;" % (subject, x, i))
            sql.execute("USE questions;")
            sql.execute("SELECT Q_num, question FROM %s ;" % subject)
            for p in sql.fetchall(): print(p)
            break
        else:
            print("**Invalid input**")


def modQues(subject='maths'):
    sql.execute("USE questions;")
    sql.execute("SELECT MAX(Q_num) FROM %s;" % subject)
    lastIndex = sql.fetchall()[0][0]
    while True:
        while True:
            print("Enter the question number to modify or enter '0' to view all the questions")
            in_qNum = int(input(":: "))
            if in_qNum == 0:
                sql.execute("USE questions;")
                sql.execute("SELECT Q_num, question FROM %s ;" % subject)
                for p in sql.fetchall(): print(p)
            elif lastIndex >= in_qNum > 0:
                sql.execute("USE questions;")
                sql.execute("SELECT type FROM %s WHERE Q_num = %d ;" % subject, in_qNum)
                type = str(sql.fetchall()[0][0])
                if type == 'mcq':
                    options = ['question', 'optionA', 'optionB', 'optionC', 'optionD', 'ansMcq']
                    in_option = options[checkInput(6, line_break + \
                                                   "\n1) Question Statement"
                                                   "\n2) Option A"
                                                   "\n3) Option B"
                                                   "\n4) Option C"
                                                   "\n5) Option D"
                                                   "\n6) Answer"
                                                   "\nEnter your choice:: ") - 1]
                    if in_option == "andMcq":
                        new_value = checkInput('mcq', "Enter the new value")
                    else:
                        new_value = input("Enter the new value:: ")
                elif type == 'true/false':
                    options = ['question', 'ansTf']
                    in_option = options[checkInput(2, line_break + \
                                                   "\n1) Question Statement"
                                                   "\n2) Answer"
                                                   "\nEnter your choice:: ") - 1]
                    new_value = checkInput('true/false', "Enter a new value(t/f)")
                else:
                    options = ['question', 'ansOw']
                    in_option = options[int(input("\n1) Question Statement"
                                                  "\n2) Answer"
                                                  "\nEnter your choice:: ")) - 1]
                    new_value = input("Enter the new value:: ")
                sql.execute("USE questions;")
                sql.execute("UPDATE %s SET %s = '%s' WHERE Q_num = %d" % (subject, in_option, new_value, in_qNum))
                quizAppDB.commit()
            else: break
        if 'n' in input("Modify another value? (y/n):: ").lower(): break


def updateJson():
    questions, fields_str = {}, ''
    fields = ['question', 'type', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'answer', 'answer', ]
    for element in range(1, len(fields)):
        fields_str += (', ' + str(fields[element]))
    print(fields_str)

    for subject in ['maths', 'sci', 'gk']:
        questions[subject] = []
        sql.execute("USE questions;")
        sql.execute("SELECT MAX(Q_num) FROM %s;" % subject)

        for q_num in range(1, sql.fetchall()[0][0] + 1):
            single_ques = {}
            sql.execute("USE questions;")
            sql.execute("SELECT question %s  FROM %s WHERE q_num = %d;" % (fields_str, subject, q_num))
            field_outputs = sql.fetchall()[0]
            if field_outputs[1] == 'mcq':
                for i in range(7):
                    single_ques[fields[i]] = field_outputs[i]
            elif field_outputs[1] == 'true/false':
                for i in [0, 1, -2]:
                    single_ques[fields[i]] = field_outputs[i]
            elif field_outputs[1] == 'oneWord':
                for i in [0, 1, -1]:
                    single_ques[fields[i]] = field_outputs[i]
            questions[subject].append(single_ques)

    with open("QuestionsTEMP.json", 'w') as tempFile:
        json.dump(questions, tempFile, indent=4)

    os.remove("Questions.json")
    os.rename(r'QuestionsTEMP.json', r'Questions.json')


while True:
    subs = ['maths', 'sci', 'gk', 'eng']
    subject = subs[checkInput(3, line_break + \
                              "\n1) Maths"
                              "\n2) Science"
                              "\n3) GK"
                              "\n3) English"
                              "\nEnter your choice") - 1]

    menu = checkInput(4, line_break + \
                      "\n1) Add Question"
                      "\n2) Delete Question"
                      "\n3) Modify Question"
                      "\n4) Exit"
                      "\nEnter your choice")

    if menu == 1:
        addQues(subject)
    elif menu == 2:
        delQues(subject)
    elif menu == 3:
        modQues(subject)

    if input(line_break + 'Do you want to EXIT(y/n)::').lower() in 'yes': break

updateJson()
