import random, requests, json, os, asyncio, aiohttp
import aiofiles
from uuid import uuid4

# unique_ID = str(uuid4())


def secret_key():
    try:
        with open('../secret_key', 'r', encoding='utf-8') as file:
            key = file.read()
    except FileNotFoundError:
        with open('secret_key', 'w', encoding='utf-8') as file:
            secret_key = str(uuid4())
            os.environ['SECRET_KEY'] = secret_key
            key = secret_key

    return key


# def rearrange_list(input_list):
#     # Use random.shuffle() to shuffle the elements of the list in place
#     new_list = input_list.copy()
#     random.shuffle(new_list)
#     return new_list

# async def get_questions_from_url(url_api, uid):
#     """
#         collects the data from the API, strips it,
#         takes only the needed questions and answers information,
#         stores the data in a file, 
#         returns the a new list with trimmed data
#     """
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_api) as response:
#             data = await response.json()
#             # print(data)
#             # data = data['results']
#             data = data.get('results', [])
#             # print(data)

#             new_data = [
#                     {'question': index['question'],
#                     'correct_answer': index['correct_answer'],
#                     'incorrect_answers': index['incorrect_answers']}
#                     for index in data
#                 ]
            
#             # json_file = f'json/request_dump_{unique_ID}.json'
#             json_file = f'json/request_dump_{uid}.json'

#             try:
#                 # Ensure the directory exists
#                 os.makedirs(os.path.dirname(json_file), exist_ok=True)

#                 with open(json_file, 'w', encoding='utf-8') as file:
#                     json.dump(new_data, file)
#                 print('File saved successfully')

#             except FileNotFoundError:
#                 print('File not found error occurred')
#             except PermissionError:
#                 print('Permission error occurred')
#             except Exception as e:
#                 print(f'Unexpected error occurred: {e}')


async def get_questions_from_url(url_api, uid):
    """
    Gets questions and ansers from the url and saves them in a json file
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as response:
            data = await response.json()
            data = data.get('results', [])
            print(f"Fetched {len(data)} questions")

            new_data = [
                {'question': index['question'],
                 'correct_answer': index['correct_answer'],
                 'incorrect_answers': index['incorrect_answers']}
                for index in data
            ]
            print(f"Fetched {len(new_data)} questions-new_data")


            json_file = f'json/request_dump_{uid}.json'

            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(json_file), exist_ok=True)

                async with aiofiles.open(json_file, 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(new_data))
                # print('File saved successfully')
                print(f"Saved {len(new_data)} questions to {json_file}")

            except Exception as e:
                print(f'Unexpected error occurred: {e}')

async def get_question_at_index(index, uid):
    """
        gets a question from an index
    """
    json_file = f'json/request_dump_{uid}.json'

    if not os.path.exists(json_file):
        print(f'File {json_file} does not exist.')
        return []

    try:
        async with aiofiles.open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.loads(await file.read())
            print(f"File loaded successfully from {json_file}")
            print(f"Number of questions in the file: {len(json_data)}")

            if len(json_data) <= index:
                print(f"Requested index {index} is out of range.")
                return []

            data = json_data[index]
            print(f"Fetched question data at index {index}: {data}")

            # Verify the structure
            if 'question' not in data or 'correct_answer' not in data or len(data.get('incorrect_answers', [])) < 3:
                print(f"Question data at index {index} is missing expected fields or has insufficient incorrect answers.")
                return []

            questions_answers_list = [
                data['question'],
                data['correct_answer'],
                data['incorrect_answers'][0],
                data['incorrect_answers'][1],
                data['incorrect_answers'][2]
            ]
    except FileNotFoundError as e:
        print('File not found', e)
        return []
    except IndexError as e:
        print('Index out of range', e)
        return []
    except Exception as e:
        print('An error occurred', e)
        return []

    return questions_answers_list

# async def get_question_at_index(index, uid):
#     """
#         Returns a list of question and the answers at index provided
#         index 0 is the correct answer
#         index 1 - 4 are the wrong answers
#     """

#     json_file = f'json/request_dump_{uid}.json'
#     questions_answers_list = None #initializing questions and asnwers list

#     if not os.path.exists(json_file):
#         print(f'File {json_file} does not exist.')
#         return []

#     try:
#         with open(json_file, 'r', encoding='utf-8') as file:
#             json_data = json.load(file)
#             print("file loaded succesfully")

#             data = json_data[index]
#             questions_answers_list = [data['question'],
#                data['correct_answer'],
#                data['incorrect_answers'][0],
#                data['incorrect_answers'][1],
#                data['incorrect_answers'][2]
#                ]
#     except FileNotFoundError as e:
#         print('file not found', e)
#     except IndexError as e:
#         print('Index out of range', e)
#         # print('json_data is being called before it is assigned', e)
#     except Exception as e:
#         print('An error occured', e)

#     return questions_answers_list if questions_answers_list is not None else []

def get_correct_answers(uid):
    """
        This function loads the modified json file created to extract
        the rest of the data as needed.
    """
    json_file = f'json/request_dump_{uid}.json'
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    my_list = []
    for item in data:
        my_list.append(item['correct_answer'])
    return my_list

def get_scores(dict, uid):
    my_answer_list = []
    correct_answer_list = get_correct_answers(uid)
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