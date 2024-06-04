import random, requests, json, os, asyncio, aiohttp
from uuid import uuid4

# unique_ID = str(uuid4())


def secret_key():

    try:
        with open('../secret_key', 'r') as file:
            key = file.read()
    except FileNotFoundError:
        with open('secret_key', 'w') as file:
            secret_key = str(uuid4())
            os.environ['SECRET_KEY'] = secret_key
            file.write(secret_key)
            key = secret_key

    return key

# def rearrange_list(input_list):
#     # Use random.shuffle() to shuffle the elements of the list in place
#     new_list = input_list.copy()
#     random.shuffle(new_list)
#     return new_list

async def get_questions_from_url(url_api, uid):
    """
        collects the data from the API, strips it,
        takes only the needed questions and answers information,
        stores the data in a file, 
        returns the a new list with trimmed data
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as response:
            data = await response.json()
            # print(data)
            # data = data['results']
            data = data.get('results')
            # print(data)
            
    # response = await requests.get(url_api)
    # data = response.json()['results']
            # print(data)
            new_data = []

            for index in data:
                new_data.append({'question': index['question'],
                                'correct_answer': index['correct_answer'],
                                'incorrect_answers': index['incorrect_answers']})

            # json_file = f'json/request_dump_{unique_ID}.json'
            json_file = f'json/request_dump_{uid}.json'

            with open(json_file, 'w') as file:
                json.dump(new_data, file)
            
            # try:
            #     with open(json_file, 'r') as file:
            #         json_data = json.load(file)
            # except FileNotFoundError as e:
            #     print('file not found', e)


def get_question_at_index(index):
    """
        Returns a list of question and the answers at index provided
        index 0 is the correct answer
        index 1 - 4 are the wrong answers
    """

    json_file = f'json/request_dump_{secret_key()}.json'
    # json_file = f'json/request_dump_{unique_ID}.json'
    questions_answers_list = None #initializing questions and asnwers list

    try:
        with open(json_file, 'r') as file:
            json_data = json.load(file)

            data = json_data[index]
            questions_answers_list = [data['question'],
               data['correct_answer'],
               data['incorrect_answers'][0],
               data['incorrect_answers'][1],
               data['incorrect_answers'][2]
               ]
    except FileNotFoundError as e:
        print('file not found', e)
    except IndexError as e:
        print('Index out of range', e)
        # print('json_data is being called before it is assigned', e)
    except Exception as e:
        print('An error occured', e)

    return questions_answers_list if questions_answers_list is not None else []

def get_correct_answers():
    """
        This function loads the modified json file created to extract
        the rest of the data as needed.
    """
    json_file = f'json/request_dump_{secret_key()}.json'
    with open(json_file, 'r') as file:
        data = json.load(file)

    my_list = []
    for item in data:
        my_list.append(item['correct_answer'])
    return my_list

def get_scores(dict):
    my_answer_list = []
    correct_answer_list = get_correct_answers()
    for key, value in dict.items():
        my_answer_list.append(value)
    
    score = 0
    for i in range(len(my_answer_list)):
        if my_answer_list[i] == correct_answer_list[i]:
            score += 1
    return score

if __name__ == '__main__':
    original_list = [1, 2, 3, 4, 5]
    rearranged_list = random.shuffle(original_list)
    print("Original list:", original_list)
    print("Rearranged list:", rearranged_list)