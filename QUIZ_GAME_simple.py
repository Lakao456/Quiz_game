import time

maths_question = [{'type' : 'mcq', 'question' :'abc', 'answer' : 'a', 'options' : 'A) opa B) opb C) D)' },
                  {'type' : 'mcq', 'question' :'abc', 'answer' : 'b', 'options' : 'A) opa B) opb C) D)' },
                  {'type' : 'true/false', 'question' :'abc', 'answer' : 'true'},
                  {'type' : 'true/false', 'question' :'abc', 'answer' : 'false'},
                  {'type' : 'one word', 'question' :'abc', 'answer' : 'xyz'},
                  {'type' : 'one word', 'question' :'abc', 'answer' : 'xyz'}]

sci_question = [{'type' : 'mcq', 'question' :'abc', 'answer' : 'xyz', 'options' : 'A) opa B) opb C) D)' },
                  {'type' : 'mcq', 'question' :'abc', 'answer' : 'xyz', 'options' : 'A) opa B) opb C) D)' },
                  {'type' : 'true/false', 'question' :'abc', 'answer' : 'true'},
                  {'type' : 'true/false', 'question' :'abc', 'answer' : 'false'},
                  {'type' : 'one word', 'question' :'abc', 'answer' : 'xyz'},
                  {'type' : 'one word', 'question' :'abc', 'answer' : 'xyz'}]

gk_question = [{'type' : 'mcq', 'question' :'abc', 'answer' : 'xyz', 'options' : 'A) opa B) opb C) D)' },
                  {'type' : 'mcq', 'question' :'abc', 'answer' : 'xyz', 'options' : 'A) opa B) opb C) D)' },
                  {'type' : 'true/false', 'question' :'abc', 'answer' : 'true'},
                  {'type' : 'true/false', 'question' :'abc', 'answer' : 'false'},
                  {'type' : 'one word', 'question' :'abc', 'answer' : 'xyz'},
                  {'type' : 'one word', 'question' :'abc', 'answer' : 'xyz'}]

play = True
q_time = 0.5 # in Minuets

while play:
    start_time = time.time()
    game_end = False
    while time.time() - start_time <= 60*q_time and not game_end:
        print("1--Maths",
              "2--Science",
              "3--General knowledge",
              sep='\n',end="\n ----------------------------- \n")

        subject, score= int(input("Select a subject:: ")), 0

        if subject == 1:
            for i in range(len(maths_question)):
                print("----------------------------------------------------------------------------------")
                print('Question ', i+1, ') ', maths_question[i]['question'])


                if maths_question[i]['type'] == 'mcq':
                    print(maths_question[i]['options'])
                    input_ans = input('Enter your answer (a,b,c,d):: ')

                    if maths_question[i]['answer'] in input_ans.lower():
                        score += 4
                        maths_question[i]['Given_ans'] = 'correct'
                        print ('Time elapsed: ', (time.time()-start_time)//1)
                    else:
                        score -= 1
                        maths_question[i]['Given_ans'] = 'Wrong'
                        print('Time elapsed: ', (time.time() - start_time) // 1)


                elif maths_question[i]['type'] == 'true/false':
                    input_ans = input('Enter your answer (true/false):: ')

                    given_ans = False
                    while not given_ans:

                        if maths_question[i]['answer'] == 'true':
                            if 't' in input_ans.lower() or 'y' in input_ans.lower():
                                score += 4
                                maths_question[i]['Given_ans'] = 'Correct'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            elif 'f' in input_ans.lower() or 'n' in input_ans.lower():
                                score -= 1
                                maths_question[i]['Given_ans'] = 'Wrong'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            else:
                                print('wrong input')

                        if maths_question[i]['answer'] == 'false':
                            if 'f' in input_ans.lower() or 'n' in input_ans.lower():
                                score += 4
                                maths_question[i]['Given_ans'] = 'correct'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            elif 't' in input_ans.lower() or 'y' in input_ans.lower():
                                score -= 1
                                maths_question[i]['Given_ans'] = 'Wrong'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            else:
                                print('wrong input')


                elif maths_question[i]['type'] == 'one word':
                    input_ans = input('Enter your answer (one word):: ')

                    if maths_question[i]['answer'] == input_ans.lower():
                        score += 4
                        maths_question[i]['Given_ans'] = 'correct'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
                    else:
                        score -= 1
                        maths_question[i]['Given_ans'] = 'Wrong'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
            game_end = True

        if subject == 2:
            for i in range(len(sci_question)):
                print("----------------------------------------------------------------------------------")
                print('Question ', i + 1, ') ', sci_question[i]['question'])

                if sci_question[i]['type'] == 'mcq':
                    print(sci_question[i]['options'])
                    input_ans = input('Enter your answer (a,b,c,d):: ')

                    if sci_question[i]['answer'] in input_ans.lower():
                        score += 4
                        sci_question[i]['Given_ans'] = 'correct'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
                    else:
                        score -= 1
                        sci_question[i]['Given_ans'] = 'Wrong'
                        print('Time elapsed: ', (time.time() - start_time) // 1)


                elif sci_question[i]['type'] == 'true/false':
                    input_ans = input('Enter your answer (true/false):: ')

                    given_ans = False
                    while not given_ans:

                        if sci_question[i]['answer'] == 'true':
                            if 't' in input_ans.lower() or 'y' in input_ans.lower():
                                score += 4
                                sci_question[i]['Given_ans'] = 'Correct'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            elif 'f' in input_ans.lower() or 'n' in input_ans.lower():
                                score -= 1
                                sci_question[i]['Given_ans'] = 'Wrong'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            else:
                                print('wrong input')

                        if sci_question[i]['answer'] == 'false':
                            if 'f' in input_ans.lower() or 'n' in input_ans.lower():
                                score += 4
                                sci_question[i]['Given_ans'] = 'correct'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            elif 't' in input_ans.lower() or 'y' in input_ans.lower():
                                score -= 1
                                sci_question[i]['Given_ans'] = 'Wrong'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            else:
                                print('wrong input')


                elif sci_question[i]['type'] == 'one word':
                    input_ans = input('Enter your answer (one word):: ')

                    if sci_question[i]['answer'] == input_ans.lower():
                        score += 4
                        sci_question[i]['Given_ans'] = 'correct'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
                    else:
                        score -= 1
                        sci_question[i]['Given_ans'] = 'Wrong'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
            game_end = True

        if subject == 3:
            for i in range(len(gk_question)):
                print("----------------------------------------------------------------------------------")
                print('Question ', i + 1, ') ', gk_question[i]['question'])

                if gk_question[i]['type'] == 'mcq':
                    print(gk_question[i]['options'])
                    input_ans = input('Enter your answer (a,b,c,d):: ')

                    if gk_question[i]['answer'] in input_ans.lower():
                        score += 4
                        gk_question[i]['Given_ans'] = 'correct'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
                    else:
                        score -= 1
                        gk_question[i]['Given_ans'] = 'Wrong'
                        print('Time elapsed: ', (time.time() - start_time) // 1)


                elif gk_question[i]['type'] == 'true/false':
                    input_ans = input('Enter your answer (true/false):: ')

                    given_ans = False
                    while not given_ans:

                        if gk_question[i]['answer'] == 'true':
                            if 't' in input_ans.lower() or 'y' in input_ans.lower():
                                score += 4
                                gk_question[i]['Given_ans'] = 'Correct'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            elif 'f' in input_ans.lower() or 'n' in input_ans.lower():
                                score -= 1
                                gk_question[i]['Given_ans'] = 'Wrong'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            else:
                                print('wrong input')

                        if gk_question[i]['answer'] == 'false':
                            if 'f' in input_ans.lower() or 'n' in input_ans.lower():
                                score += 4
                                gk_question[i]['Given_ans'] = 'correct'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            elif 't' in input_ans.lower() or 'y' in input_ans.lower():
                                score -= 1
                                gk_question[i]['Given_ans'] = 'Wrong'
                                print('Time elapsed: ', (time.time() - start_time) // 1)
                                given_ans = True
                            else:
                                print('wrong input')


                elif gk_question[i]['type'] == 'one word':
                    input_ans = input('Enter your answer (one word):: ')

                    if gk_question[i]['answer'] == input_ans.lower():
                        score += 4
                        gk_question[i]['Given_ans'] = 'correct'
                        print('Time elapsed: ', (time.time() - start_time) // 1)
                    else:
                        score -= 1
                        gk_question[i]['Given_ans'] = 'Wrong'
                        print('Time elapsed: ', (time.time() - start_time) // 1)

            game_end = True

    print("Time Over !",
          "your score is ", score,
          sep='\n')
    print("Your correctness")

    if subject == 1:
        for i in range (len(maths_question)):
            try:
                print('Ans ', i+1, ') ', maths_question[i]["Given_ans"])
            except:
                print("end of ans")
    if subject == 2:
        for i in range (len(sci_question)):
            try:
                print('Ans ', i+1, ') ', sci_question[i]["Given_ans"])
            except:
                print("end of ans")
    if subject == 3:
        for i in range (len(gk_question)):
            try:
                print('Ans ', i+1, ') ', gk_question[i]["Given_ans"])
            except:
                print("end of ans")

    if input("Do you want to play again (Y/N)").lower() != 'y':
        play = False

print("Thank you for playing !")