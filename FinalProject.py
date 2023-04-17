#########################################
##### Name: Erin Zhan               #####
##### Uniqname: zerin               #####
#########################################


import requests
import json 
import webbrowser

CACHE_FILE = "usda_cache.json"
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
def search_recipe(query, cuisine):
    
    spoon_api_key = '225f60550c4e4e1b8fa8aeaf780bafe5'
    spoon_baseurl = 'https://api.spoonacular.com/recipes/complexSearch'
    
    params = {
        "apiKey": spoon_api_key,
        "query": query,
        "cuisine": cuisine
    }
    
    response = make_request_with_cache(spoon_baseurl, params=params)
    return response


recipe_data = search_recipe("Pasta", "Italian")
print(recipe_data)

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
print(search_item("Apple"))

#define the decision tree
tree = {
    'question': 'What type of cuisine do you prefer?',
    'answers': ['Italian', 'Asian', 'American', 'Mexican', 'Mediterranean'],
    'nodes': "What's your"
}

def decision_tree(node):
    if isinstance(node, dict):
        answer = input(node['question'])
        while answer not in node['answers']:
            print("Invalid answer. Please try again.")
            answer = input(node['question'])
        next_node = node['nodes'][node['answers'].index(answer)]
        decision_tree(next_node)
    else:
        get_recipes()








def main():

    print("Welcome to the Personalized Meal Plan Guide!")
    root = ("What type of cuisine do you prefer?", None, None)





