import mysql.connector

quizGameDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="aman.singh456",
    database="questions")
sql = quizGameDB.cursor()

sql.execute("USE questions;")
sql.execute("SELECT question, type, optionA, optionB, optionC, optionD, ansMcq, ansTf, ansOw  FROM maths WHERE q_num = 20;")

x = sql.fetchall()[0]
print(x)
#
# fields, fields_str = ['question', 'type', 'optionA', 'optionB', 'optionC', 'optionD', 'ansMcq', 'ansTf', 'ansOw',], ''
# for element in range(1, len(fields)):
#     fields_str += (', '+str(fields[element]))
#
# print(' question'+fields_str)
# print(fields)


# while True:
#     value = input("Enter a number:: ")
#     try:
#         value = int(value)
#         if value not in range(1,5+1):
#             print("invalid input")
#         else: break
#     except ValueError:
#         print("invalid input")
# print("cool")

# if type(5) == type(1):
#     print("cool")
