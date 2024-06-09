from path_in_IT_bot.readers.questions_reader import questions_list as questions

questions_with_answers = []
for q in questions:
    question_with_answers = q.question + "\n"
    for i, a in enumerate(q.answers.keys()):
        question_with_answers += f'\n{i + 1}) {a}\n'
    questions_with_answers += [question_with_answers]