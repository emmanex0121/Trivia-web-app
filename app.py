#!/usr/bin/python3
import json
import random
import asyncio
from flask import Flask, render_template, redirect, url_for, jsonify, request
# from flask_session import Session
# from models.data import secret_key, get_questions_from_url, get_scores
# from models.data import get_question_at_index, get_correct_answers
from models.data import *
# from uuid import uuid4


app = Flask(__name__)
# app.secret_key = secret_key()
app.config['SECRET_KEY'] = secret_key()
# unique_ID = str(uuid4())
secret_key = secret_key()


@app.route('/')
def index():
    """
        Index Page: Route that serves default home page
    """
    return render_template('index.html')

@app.route('/play_now', strict_slashes=False)
def play_now():
    """
        Play Now: Route that handles instant play with random settings 
    """
    # Logic to manipulate GET request data

    # For random questions 10
    url = 'https://opentdb.com/api.php?amount=10&type=multiple'
    print("muhehe")

    # question_list = get_questions(url)
    asyncio.run(get_questions_from_url(url, secret_key))
    # await get_questions_from_url(url, secret_key)

    return redirect(url_for('play_page', route_id=0))

@app.route('/play_now/<int:route_id>', strict_slashes=False)
def play_page(route_id):
    """
        Play Page
    """
    print("testing")
    my_list = asyncio.run(get_question_at_index(route_id, secret_key))

    # my_list = await get_question_at_index(route_id, secret_key)

    if not my_list:
        return "No questions and answers available", 404

    question = {"id": route_id, "text": my_list[0]}
    answers_list = [
        {"id": 1, "text": my_list[1]},
        {"id": 2, "text": my_list[2]},
        {"id": 3, "text": my_list[3]},
        {"id": 4, "text": my_list[4]}
    ]

    random.shuffle(answers_list)

    return render_template('start.html', question=question, answers_list=answers_list)

@app.route('/submit_mode', methods=['POST', 'GET'])
def submit_mode():
    """
        Submit mode: Route that handles mode selections
    """
    print("Test")
    difficulty = request.form.get('trivia_difficulty')
    category = request.form.get('trivia_category')

    print(dict(request.form))
    print(difficulty, category)
    # print(dict(request.headers))

    url = 'https://opentdb.com/api.php?amount=10'
    if difficulty != 'any':
        url += f'&difficulty={difficulty}'
    if category != 'any':
        url += f'&category={category}'

    # Ensure the async function completes
    asyncio.run(get_questions_from_url(url, secret_key))
    
    redirect_url = url_for('play_page', route_id=0)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'redirect_url': redirect_url})
    else:
        return redirect(redirect_url)


@app.route('/score', methods=['POST'])
def submit_play():
    """
        Submit Play: From score page, route that restartsthe game using
        Existing settings
    """
    # print('hello')
    
    # Parse the JSON string from the form field
    submitted_answers = request.form['selected_answers']
    answers_list = json.loads(submitted_answers)

    for key, value in answers_list.items():
        print(key, value)
    
    score = get_scores(answers_list, secret_key)

    if score < 5:
        comment = "Not Great!"
        # comment_subtitle = "You can do better! You Whackamole!"
        comment_subtitle = "You brought the guru intense shame. He has perished!"
        restart = "Try Again Gasbag"
    elif score < 9:
        comment = "Good!"
        comment_subtitle = "The guru is only mildly impressed."
        restart = "Try Again"
    else:
        comment = "Awesome!!!"
        # comment_subtitle = "Now that &aposs how you do it!!"
        comment_subtitle = "The guru has reached enlightenment!"
        restart = "Play Again" 

    return render_template('score.html', score=score, comment=comment, comment_subtitle=comment_subtitle, restart=restart)

@app.route('/results', strict_slashes=False)
def results():
    """
        Results Page: Provides the results
    """
    questions = []


    for item in range(10):
        # Run the coroutine and get the result
        question_data = asyncio.run(get_question_at_index(item, secret_key))
        
        if not question_data:
            continue  # Skip if no data is returned
        
        # Unpack the result
        question = question_data[0]
        correct_answer = question_data[1]
        answers = question_data[1:5]  # correct and incorrect answers
        random.shuffle(answers)

        # Add the question data to the list
        questions.append({
            'question_id': item,
            'question': question,
            'correct_answer': correct_answer,
            'answers': answers
        }) # questions_object['item'] = get_question_at_index(item)
    

    correct_answers_list = json.dumps(get_correct_answers(secret_key))
    # correct_answers_list = get_correct_answers()

    print (correct_answers_list)
    print (questions[0])
    print (answers)

    return render_template('results.html', questions=questions, correct_answers_list=correct_answers_list)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
