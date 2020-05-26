import os
import json
import mysql.connector

quizGameDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="aman.singh456",
    database="questions")
sql = quizGameDB.cursor()


def addQues(subject='maths'):
    mcq_op, ans_mcq, ans_tf, ans_ow = ["NUll, ", "NUll, ", "NUll, ", "NUll, "], "NULL, ", "NULL,", "NULL"
    in_question = "'" + input("\nEnter the question statement:-") + "', "
    types = [None, 'mcq', 'true/false', 'oneWord']
    in_type = "'" + types[int(input("\n1) MCQ"
                                    "\n2) True/False"
                                    "\n3) One Word"
                                    "\nEnter your choice:: "))] + "', "

    if 'mcq' in in_type:
        for i in range(4):
            mcq_op[i] = "'" + input("Enter option" + chr(65 + i) + " ::") + "', "
        ans_mcq = "'" + input("Enter the answer(a/b/c/d):: ") + "', "
    elif 'true/false' in in_type:
        ans_tf = "'" + input("Enter the answer(t/f):: ") + "', "
    elif 'oneWord' in in_type:
        ans_ow = "'" + input("Enter the answer:: ")

    sql.execute("USE questions;")
    sql.execute("SELECT MAX(Q_num) FROM sci;")
    print(sql.fetchall()[0])
    # exe_str = "INSERT INTO " + subject + " VALUES('" + last_index + in_question + in_type + \
    #           mcq_op[0] + \
    #           mcq_op[1] + \
    #           mcq_op[2] + \
    #           mcq_op[3] + \
    #           ans_mcq + \
    #           ans_tf + \
    #           ans_ow + ");"
    # sql.execute(exe_str)
    # quizGameDB.commit()


def delQues(subject='maths'):
    while True:
        print("Enter the question number to delete or enter '0' to view all the questions")
        in_qNum = int(input(":: "))
        if in_qNum == 0:
            sql.execute("USE questions;")
            sql.execute("SELECT Q_num, question FROM " + subject + ";")
            for p in sql.fetchall(): print(p)
        else:
            sql.execute("USE questions;")
            sql.execute("DELETE FROM " + subject + " WHERE Q_num = " + str(in_qNum) + ";")
            quizGameDB.commit()


def modQues(subject='maths'):
    while True:
        print("Enter the question number to modify or enter '0' to view all the questions")
        in_qNum = input(":: ")
        if in_qNum == 0:
            sql.execute("USE questions;")
            sql.execute("SELECT Q_num, question FROM " + subject + ";")
            for p in sql.fetchall(): print(p)
        else:
            sql.execute("USE questions;")
#NICE
            sql.execute("SELECT type FROM " + subject + " WHERE Q_num = " + in_qNum + ";")
            type = str(sql.fetchall()[0][0])

            if type == 'mcq':
                options = [None, 'question', 'optionA', 'optionB', 'optionC', 'optionD', 'ansMcq']
                in_option = options[int(input("\n1) Question Statement"
                                              "\n2) Option A"
                                              "\n3) Option B"
                                              "\n4) Option C"
                                              "\n5) Option D"
                                              "\n6) Answer"
                                              "\nEnter your choice:: "))] + " = '"
                new_value = input("Enter the new value:: ")
            elif type == 'true/false':
                options = [None, 'question', 'ansTf']
                in_option = options[int(input("\n1) Question Statement"
                                              "\n2) Answer"
                                              "\nEnter your choice:: "))] + " = '"
                tf = [None, 'true', 'false']
                new_value = tf[int(input("\n1) True"
                                         "\n2) False"
                                         "\nSelect the New value:: "))]
            else:
                options = [None, 'question', 'ansOw']
                in_option = options[int(input("\n1) Question Statement"
                                              "\n2) Answer"
                                              "\nEnter your choice:: "))] + " = '"
                new_value = input("Enter the new value:: ")

            sql.execute("USE questions;")
            sql.execute("UPDATE " + subject + " SET " + in_option + new_value + "' WHERE Q_num = " + in_qNum + ";")
            quizGameDB.commit()

        if 'n' in input("Modify another value? (y/n):: ").lower():
            break


def updateJson():
    questions, fields_str = {}, ''
    fields = ['question', 'type', 'optionA', 'optionB', 'optionC', 'optionD', 'ansMcq', 'ansTf', 'ansOw', ]
    for element in range(1, len(fields)):
        fields_str += (', ' + str(fields[element]))

    for subject in ['maths', 'sci', 'gk']:
        questions[subject] = []
        sql.execute("USE questions;")
        sql.execute("SELECT MAX(Q_num) FROM %s;" %subject)

        for q_num in range(sql.fetchall()[0][0]):
            print(subject, q_num)
            single_ques = {}
            sql.execute("USE questions;")
            sql.execute("SELECT question%s  FROM %s WHERE q_num = %d;" % (fields_str, subject, q_num + 1))
            field_outputs = sql.fetchall()[0]
            if field_outputs[1] == 'mcq':
                for i in range(7):
                    single_ques[fields[i]] = field_outputs[i]
            elif field_outputs[1] == 'true/false':
                for i in [0,1,-2]:
                    single_ques[fields[i]] = field_outputs[i]
            elif field_outputs[1] == 'oneWord':
                for i in [0,1,-1]:
                    single_ques[fields[i]] = field_outputs[i]
            questions[subject].append(single_ques)

    with open("questionsTEMP.json", 'w') as tempFile:
        json.dump(questions, tempFile, indent=4)


# subs = [None, 'maths', 'sci', 'gk','exit']
# subject = subs[int(input("\n1) Maths"
#                          "\n2) Science"
#                          "\n3) GK"
#                          "\n4) Exit"
#                          "\nEnter your choice:: "))]
# print("---------------------------------------------------")
# menu = int(input("1) Add Question\n"
#                  "2) Delete Question\n"
#                  "3) Modify Question\n"
#                  "Enter your choice:: "))
# print("---------------------------------------------------")
# if menu == 1:
#     addQues(subject)
# elif menu == 2:
#     delQues(subject)
# elif menu == 3:
#     modQues(subject)
# else:
#     updateJson()

updateJson()
