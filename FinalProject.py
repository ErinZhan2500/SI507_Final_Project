#########################################
##### Name: Erin Zhan               #####
##### Uniqname: zerin               #####
#########################################


import requests
import textwrap 
import json 
from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup


with open('decision_tree.json') as f:
    tree = json.load(f)

CACHE_FILE = "cache.json"
CACHE_DICT = {}


def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILE, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILE,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    response = requests.get(baseurl, params=params)
    return response.json()

def make_request_with_cache(baseurl, params):
    '''Check the cache for a saved result for this baseurl+params
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("cache hit!", request_key)
        return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

CACHE_DICT = open_cache()


#spoontacular data
def get_id(query, cuisine):
    
    spoon_api_key = '225f60550c4e4e1b8fa8aeaf780bafe5'
    spoon_baseurl = 'https://api.spoonacular.com/recipes/complexSearch'
    
    params = {
        "apiKey": spoon_api_key,
        "query": query,
        "cuisine": cuisine
    }
    
    response = make_request_with_cache(spoon_baseurl, params=params)
    return response


def decision_tree(node):
    if isinstance(node, dict) and 'answers' in node:
        #print answers
        for i in range(1, len(node['answers']) + 1):
            print(str(i) + ". " + node['answers'][i-1])
        answer = input("Enter the number of your answer: ")

        while answer <= "0" or answer >= str(len(node['answers']) + 1):
            print("Invalid answer. Please try again.")
            answer = input("Enter the number of your answer: ")
        next_node = node['nodes'][int(answer)-1]
        return decision_tree(next_node)
    else:
        return node

def get_recipes():
    recipes = decision_tree(tree)['result']
    for i in range(len(recipes)):
        recipe = recipes[i]
        print(f"{i+1}. {recipe['title']}")

    recipe_num = input("Enter the number of the recipe you want to view: ")
    try:
        recipe_num = int(recipe_num)
        if recipe_num < 1 or recipe_num > len(recipes):
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a number between 1 and", len(recipes))
        return

    selected_recipe = recipes[recipe_num - 1]
    id = selected_recipe['id']
    print(f"You selected: {selected_recipe['title']}")

    spoon_api_key = '225f60550c4e4e1b8fa8aeaf780bafe5'
    spoon_baseurl = f'https://api.spoonacular.com/recipes/{id}/information'

    params = {
        "apiKey": spoon_api_key,
        "includeNutrition": True
    }
    
    response = make_request_with_cache(spoon_baseurl, params=params)
    #response = json.dumps(response, indent=1) pprint json
    #keys: extendedIngredients, instructions, title
    print(response['title'])
    print("Ingredient List:")
    for ingredient in response['extendedIngredients']:
        print("\t" + ingredient['name'])
    instructions = '\n'.join(textwrap.wrap(response['instructions'], 70, break_long_words=False))
    print(instructions)
    #print(response)
    return


#Price api from kroger
def kroger_access(auth_code):
    token_url = 'https://api.kroger.com/v1/connect/oauth2/token'

    qd = {'grant_type': 'authorization_code',
          'code': auth_code,
          'redirect_uri': redirect_uri,
          'client_id': client_id,
          'client_secret': client_secret}

    response = requests.post(token_url, data=qd, timeout=60)
    response = response.json()

    if 'error' in response.keys():
        return print("Access Unsuccessfully Granted! Please try again!")
    else:
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        return ["Access Successfully Granted!",access_token, refresh_token]

def kroger_auth(client_id,redirect_uri):
    auth_params = {'scope': 'product.compact',
                   'response_type': 'code',
                   'client_id': client_id,
                   'redirect_uri': redirect_uri,
                   }

    html = requests.get("https://api.kroger.com/v1/connect/oauth2/authorize",
                        params = auth_params)

    # Print the link to the approval page
    return print(html.url)

def kroger_refresh(refresh_token):
    token_url = 'https://api.kroger.com/v1/connect/oauth2/token'

    qd = {'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id': client_id,
          'client_secret': client_secret}

    response = requests.post(token_url, data=qd, timeout=60)
    response = response.json()

    if 'error' in response.keys():
        return print("Access Unsuccessfully Granted! Please try again!")
    else:
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        return ["Access Successfully Granted!",access_token, refresh_token]

client_id = 'erinfinalproject-03e19ff3eb54ebc908f4f8d8b54f31987134382640670711017'
client_secret = 'mlyKMCZF-d77Qh-GEn1yTtKQysdNPCsOM5U1Ee6E'
redirect_uri = 'http://localhost:8888'


class Data():
    lines = []
    cuisine_mode = True
    recipe_mode = False
    error_message = ""
    app_node = tree
    done = False
    loaded = False
    priceoutput = False
    def reset(self):
        self.lines = []
        self.cuisine_mode = True
        self.recipe_mode = False
        self.error_message = ""
        self.app_node = tree
        self.done = False

data = Data()

app = Flask(__name__)


@app.route("/")
def index():
    '''Create the main Index '/' in the Web API
    Parameters
    ----------
    Data: Class that holds necessary information so
          Translate our program to a web service
    Returns
    -------
    HTML of our index
    '''
    if data.done:
        data.lines.append("If you have any missing ingredients enter them below:")
        pass
    elif isinstance(data.app_node, dict) and 'answers' in data.app_node and data.error_message == '':
        data.cuisine_mode = True
        data.recipe_mode = False
        data.lines = []
        data.lines.append(data.app_node['question'])
        for i in range(1, len(data.app_node['answers']) + 1):
            data.lines.append(str(i) + ". " + data.app_node['answers'][i-1])
    elif data.error_message == '':
        data.cuisine_mode = False
        data.recipe_mode = True
        recipes = data.app_node['result']
        data.lines = []
        for i in range(len(recipes)):
            recipe = recipes[i]
            data.lines.append(f"{i+1}. {recipe['title']}")
    

    return render_template('home.html', Data = data)

@app.route("/send_answer/", methods=['POST'])
def send_answer():
    '''Handles answer posts from users
    Parameters
    ----------
    answer: When a user inputs an answer
            We error check to see if it valid
            as well as the type of question
            we were asking
    Answer Post API
    '''
    answer = request.form['answer']
    if(data.cuisine_mode):
        if answer <= "0" or answer >= str(len(data.app_node['answers']) + 1):
            data.error_message = "Invalid answer. Please try again."
        else:
            data.app_node = data.app_node['nodes'][int(answer)-1]
            data.error_message = ""
    if(data.recipe_mode):
        recipes = data.app_node['result']
        if answer < "1" or answer > str(len(recipes)):
            data.error_message = "Invalid answer. Please try again."
        else:
            data.error_message = ""
            data.recipe_mode = False
            selected_recipe = recipes[int(answer) - 1]
            id = selected_recipe['id']
            data.lines.append(f"You selected: {selected_recipe['title']}")

            spoon_api_key = '225f60550c4e4e1b8fa8aeaf780bafe5'
            spoon_baseurl = f'https://api.spoonacular.com/recipes/{id}/information'

            params = {
                "apiKey": spoon_api_key,
                "includeNutrition": True
            }
            
            response = make_request_with_cache(spoon_baseurl, params=params)
            data.lines.append(response['title'])
            data.lines.append("Ingredient List:")
            for ingredient in response['extendedIngredients']:
                data.lines.append("\t" + ingredient['name'])
            instructions = '\n'.join(textwrap.wrap(response['instructions'], 70, break_long_words=False))
            data.lines.append(instructions)
            data.done = True
    return index()

client_id = 'erinfinalproject-03e19ff3eb54ebc908f4f8d8b54f31987134382640670711017'
client_secret = 'mlyKMCZF-d77Qh-GEn1yTtKQysdNPCsOM5U1Ee6E'
auth_code = 'Cl-hR_SozI1VZdfv1M8q97YTr_gRq36MTW0Pwv8m'
redirect_uri = 'http://localhost:8888'
# Get access token to Kroger API
kroger_auth(client_id,redirect_uri)
if not data.loaded:
    access = kroger_access(auth_code)
    access_token = access[1]
    data.loaded = True

@app.route("/send_answer_text", methods=['POST'])
def index_end():
    answer = request.form['answer']
    headers = {"content-type": "application/json; charset=UTF-8",'Authorization':'Bearer {}'.format(access_token)}
    ingredients = answer.split(",")
    # Loop through each ingredient and scrape the price information
    for ingredient in ingredients:
    # Construct the search URL for the ingredient
        search_url = 'https://api.kroger.com/v1/products?filter.term='+ingredient+'&filter.locationId=01400441&filter.limit='+str(1)

    # Send a GET request to the search URL and store the response
        response = requests.get(search_url, headers=headers)
        jason = response.json()
        price = jason['data'][0]['items'][0]['price']['regular']
        data.lines.append(f"{ingredient}: ${price}")
    data.priceoutput = True
    return render_template('home.html', Data = data)

@app.route("/reset/", methods=['POST'])
def reset():
    '''Debugging API to reset the questionairre
    '''
    data.reset()
    return index()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



