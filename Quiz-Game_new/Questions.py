# questions[*subject*][*Ques_num*][*Ques_attr*]
# TEMPLATES
"""
 MCQ                     {'type': 'mcq',
                          'question': '',
                          'answer': '', # (a/b/c/d)
                          'optionA': '',
                          'optionB': '',
                          'optionC': '',
                          'optionD': ''}, # Q1

True/False               {'type': 'true/false',
                          'question': 'abc',
                          'answer': 'true'}, # Q1

One Word                 {'type': 'one word',
                          'question': '',
                          'answer': ''}, # Q1
"""

print("**Questions Imported**")

questions = {
             "Maths": [
                       {'type': 'mcq',
                        'question': 'For some integer m, every \n odd integer is of the form, ',
                        'answer': 'd',
                        'optionA': 'm',
                        'optionB': 'm + 1',
                        'optionC': '2m',
                        'optionD': '2m + 1'}, # M1

                       {'type': 'mcq',
                        'question': 'The pair of equations x + 2y – 5 = 0\nand −3x – 6y + 15 = 0 have:',
                        'answer': 'c',
                        'optionA': 'A unique solution',
                        'optionB': 'Exactly two solutions',
                        'optionC': 'Infinitely many solutions',
                        'optionD': 'No solution'}, # M2

                       {'type': 'true/false',
                        'question': 'The length of tangents drawn from an external point to a circle are equal',
                        'answer': 'true'}, # M3

                       {'type': 'true/false',
                        'question': 'The slope of a vertical line is undefined.',
                        'answer': 'true'}, # M4

                       {'type': 'one word',
                        'question': 'What is the median when it is given that mode and mean are 8 and 9 respectively.',
                        'answer': '8.67'}, # M5

                       {'type': 'one word',
                        'question': 'What is the range of the first 10 prime numbers ? (Statistics)',
                        'answer': '27'}  # M6
                      ],


             "Science": [
                         {'type': 'mcq',
                          'question': 'What is known as the powerhouse of the cell',
                          'answer': 'c',
                          'optionA': 'Ribosomes',
                          'optionB': 'Nucleus',
                          'optionC': 'Mitochondria',
                          'optionD': 'Vacuole'}, # S1

                         {'type': 'mcq',
                          'question': 'The pair of equations x + 2y – 5 = 0\nand −3x – 6y + 15 = 0 have:',
                          'answer': 'c',
                          'optionA': 'A unique solution',
                          'optionB': 'Exactly two solutions',
                          'optionC': 'Infinitely many solutions',
                          'optionD': 'No solution'}, # S2

                         {'type': 'true/false',
                          'question': 'abc',
                          'answer': 'true'}, # S3

                         {'type': 'true/false',
                          'question': 'abc',
                          'answer': 'false'}, # S4

                         {'type': 'one word',
                          'question': 'abc',
                          'answer': 'xyz'}, # S5

                         {'type': 'one word',
                          'question': 'abc',
                          'answer': 'xyz'}  # S6
                        ],


             "GK": [
                         {'type': 'mcq',
                          'question': 'abc',
                          'answer': 'a',
                          'optionA': 'a',
                          'optionB': 'b',
                          'optionC': 'c',
                          'optionD': 'd'}, # G1

                         {'type': 'mcq',
                          'question': 'def',
                          'answer': 'b',
                          'optionA': 'a',
                          'optionB': 'b',
                          'optionC': 'c',
                          'optionD': 'd'}, # G2

                         {'type': 'true/false',
                          'question':'abc',
                          'answer': 'true'}, # G3

                         {'type': 'true/false',
                          'question':'abc',
                          'answer': 'false'}, # G4

                         {'type': 'one word',
                          'question':'abc',
                          'answer': 'xyz'}, # G5

                         {'type': 'one word',
                          'question': 'abc',
                          'answer': 'xyz'}  # G6
                   ]
            }
