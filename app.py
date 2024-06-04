#!/usr/bin/python3
import json, random, asyncio
from flask import Flask, render_template, redirect, url_for, jsonify, request
# from flask_session import Session
from models.data import *
# from uuid import uuid4


app = Flask(__name__)
# app.secret_key = secret_key()
app.config['SECRET_KEY'] = secret_key()
# unique_ID = str(uuid4())
secret_key = secret_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_now', strict_slashes=False)
async def play_now():
    # Logic to manipulate GET request data

    # For random questions 10
    url = 'https://opentdb.com/api.php?amount=10&type=multiple'

    # question_list = get_questions(url)
    await get_questions_from_url(url, secret_key)

    return redirect(url_for('play_page', route_id=0))

@app.route('/play_now/<int:route_id>', strict_slashes=False)
def play_page(route_id):

    my_list = get_question_at_index(route_id, secret_key)
    if not my_list:
        return "No questions and answers available", 404
    question = {"id": route_id, "text": my_list[0]}

    answers_list = [
        {"id": 1, "text": my_list[1]},
        {"id": 2, "text": my_list[2]},
        {"id": 3, "text": my_list[3]},
        {"id": 4, "text": my_list[4]}
    ]
    print(answers_list[0])
    random.shuffle(answers_list)
    print(answers_list[0])

    return render_template('start.html', question=question, answers_list=answers_list)

@app.route('/submit_mode', methods=['POST', 'GET'])
async def submit_mode():
    difficulty = request.form.get('trivia_difficulty')
    category = request.form.get('trivia_category')

    print(dict(request.form))
    print(difficulty, category)
    print(dict(request.headers))

    if (difficulty == 'any' and category == 'any'):
        redirect_url = url_for('play_now')
    elif difficulty == 'any':
        url = f'https://opentdb.com/api.php?amount=10&category={category}&type=multiple'
        await get_questions_from_url(url, secret_key)
        redirect_url = url_for('play_page', route_id=0)
    elif category == 'any':
        url = f'https://opentdb.com/api.php?amount=10&difficulty={difficulty}&type=multiple'
        await get_questions_from_url(url, secret_key)
        redirect_url = url_for('play_page', route_id=0)
    else:
        url = f'https://opentdb.com/api.php?amount=10&category={category}&difficulty={difficulty}&type=multiple'
        await get_questions_from_url(url, secret_key)
        redirect_url = url_for('play_page', route_id=0)
    
    # return redirect(url_for('play_page', route_id=0))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'redirect_url': redirect_url})
    else:
        return redirect(redirect_url)

@app.route('/score', methods=['POST'])
def submit_play():
    print('hello')
    
    # Parse the JSON string from the form field
    submitted_answers = request.form['selected_answers']
    answers_list = json.loads(submitted_answers)

    for key, value in answers_list.items():
        print(key, value)
    
    score = get_scores(answers_list, secret_key)

    if score < 5:
        comment = "Not Great!"
        # comment_subtitle = "You can do better! You Whackamole!"
        comment_subtitle = "You brought the guru intense shame. He has perished"
        restart = "Try Again Gasbag"
    elif score < 9:
        comment = "Good!"
        comment_subtitle = "This guru is only mildly impressed"
        restart = "Try Again"
    else:
        comment = "Awesome!!!"
        # comment_subtitle = "Now that &aposs how you do it!!"
        comment_subtitle = "The guru has reached enlightenment!"
        restart = "Play Again" 

    return render_template('score.html', score=score, comment=comment, comment_subtitle=comment_subtitle, restart=restart)

@app.route('/results', strict_slashes=False)
def results():
    questions = []

    for item in range(10):
        question = get_question_at_index(item, secret_key)[0]
        correct_answer = get_question_at_index(item, secret_key)[1]
        answers = [get_question_at_index(item, secret_key)[1], get_question_at_index(item, secret_key)[2], get_question_at_index(item, secret_key)[3], get_question_at_index(item, secret_key)[4]]
        random.shuffle(answers)
        shuffle_answers = answers
        questions.append({'question_id': item, 'question': question, 'correct_answer': correct_answer, 'answers': shuffle_answers})
        # questions_object['item'] = get_question_at_index(item)
    

    correct_answers_list = json.dumps(get_correct_answers(secret_key))
    # correct_answers_list = get_correct_answers()

    print (correct_answers_list)
    print (questions[0])
    print (shuffle_answers)

    return render_template('results.html', questions=questions, correct_answers_list=correct_answers_list)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
