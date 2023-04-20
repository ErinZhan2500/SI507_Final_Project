#########################################
##### Name: Erin Zhan               #####
##### Uniqname: zerin               #####
#########################################


import requests
import textwrap 
import json 
from flask import Flask, render_template, url_for, request



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



#Walmart data
def search_item(search_term):
    walmart_api_key = 'E9C7639899284F44A6CE9CF440B4EC85'
    walmart_baseurl = 'https://api.bluecartapi.com/request'

    params = {
        'api_key': walmart_api_key,
        'type': 'search',
        'search_term': search_term,
        'sort_by': 'best_seller'
}

    response = make_request_with_cache(walmart_baseurl, params=params)
    return response


# print the JSON response from BlueCart API
#print(search_item("Apple"))


    #spoontacular data
def get_id(query, cuisine):
    
    spoon_api_key = '225f60550c4e4e1b8fa8aeaf780bafe5'
    spoon_baseurl = 'https://api.spoonacular.com/recipes/complexSearch'
    
    params = {
        "apiKey": spoon_api_key,
        "query": query,
        "cuisine": cuisine,
        "addRecipeInformation": True,
        "addRecipeNutrition": True
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

def main():
    
    print("Welcome to the Personalized Meal Plan Guide!")
    print("Answer the following questions to get a personalized meal plan.")

    get_recipes()
    
    

if __name__ == "__main__":
    main()



app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



