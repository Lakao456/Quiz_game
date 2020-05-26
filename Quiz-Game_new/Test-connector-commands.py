# import mysql.connector
#
# quizGameDB = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="aman.singh456",
#     database="questions")
# sql = quizGameDB.cursor()
#
# sql.execute("USE questions;")
# sql.execute("SELECT question, type FROM sci WHERE q_num = 1;")
#
#
# print(sql.fetchall()[0][0])
#
fields, fields_str = ['question', 'type', 'optionA', 'optionB', 'optionC', 'optionD', 'ansMcq', 'ansTf', 'ansOw',], ''
for element in range(1, len(fields)):
    fields_str += (', '+str(fields[element]))

print(' question'+fields_str)
print(fields)
