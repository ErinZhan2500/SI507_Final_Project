#########################################
##### Name: Erin Zhan               #####
##### Uniqname: zerin               #####
#########################################


import requests
import json 

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


#recipe_data = search_recipe("Pasta", "Italian")['results'][0:5]
#print(recipe_data)

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

#define the decision tree
tree = {
    'question': 'What type of cuisine do you prefer?',
    'answers': ['Italian', 'Asian', 'Mexican'],
    'nodes':[
        {
            'question': 'What type of Italian dish would you like to cook?',
            'answers': ['Pasta', 'Pizza', 'Risotto'],
            'nodes': [
                {
                    'question': 'What type of pasta would you like to make?',
                    'answers': ['Spaghetti', 'Lasagna', 'Fettuccine'],
                    'nodes': [
                        {
                            'result': search_recipe('Spaghetti', 'Italian')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Lasagna', 'Italian')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Fettuccine', 'Italian')['results'][0:5]
                        }
                    ]
                },
                {
                    'question': 'What type of pizza would you like to make?',
                    'answers': ['Margherita', 'Pepperoni', 'Vegetarian'],
                    'nodes': [
                        {
                            'result': search_recipe('Margherita', 'Italian')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Pepperoni', 'Italian')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Vegetarian', 'Italian')['results'][0:5]
                        }
                    ]
                },
                {
                    'question': 'What type of risotto would you like to make?',
                    'answers': ['Mushroom', 'Seafood', 'Asparagus'],
                    'nodes': [
                        {
                            'result': search_recipe('Mushroom', 'Italian')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Seafood', 'Italian')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Asparagus', 'Italian')['results'][0:5]
                        }
                    ]
                }
            ]
        },
        {
            'question': 'What type of Asian dish would you like to cook?',
            'answers': ['Chinese', 'Japanese', 'Thai'],
            'nodes': [
                {
                    'question': 'What type of Chinese dish would you like to make?',
                    'answers': ['Stir Fry', 'Dumplings', 'Hot Pot'],
                    'nodes': [
                        {
                            'result': search_recipe('Stir Fry', 'Chinese')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Dumplings', 'Chinese')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Hot Pot', 'Chinese')['results'][0:5]
                        }
                    ]
                },
                {
                    'question': 'What type of Japanese dish would you like to make?',
                    'answers': ['Sushi', 'Ramen', 'Teriyaki'],
                    'nodes': [
                        {
                            'result': search_recipe('Sushi', 'Japanese')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Ramen', 'Japanese')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Teriyaki', 'Japanese')['results'][0:5]
                        }
                    ]
                },
                {
                    'question': 'What type of Thai dish would you like to make?',
                    'answers': ['Curry', 'Pad Thai', 'Tom Yum'],
                    'nodes': [
                        {
                            'result': search_recipe('Curry', 'Thai')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Pad Thai', 'Thai')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Tom Yum', 'Thai')['results'][0:5]
                        }
                    ]
                }
            ]
        },
        {
            'question': 'What type of Mexican dish would you like to cook?',
            'answers': ['Tacos', 'Enchiladas', 'Chiles Rellenos'],
            'nodes': [
                {
                    'question': 'What type of filling would you like for your tacos?',
                    'answers': ['Beef', 'Chicken', 'Vegetarian'],
                    'nodes': [
                        {
                            'result': search_recipe('Beef Tacos', 'Mexican')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Chicken Tacos', 'Mexican')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Vegetarian Tacos', 'Mexican')['results'][0:5]
                        }
                    ]
                },
                {
                    'question': 'What type of sauce would you like for your enchiladas?',
                    'answers': ['Red Sauce', 'Green Sauce', 'Mole Sauce'],
                    'nodes': [
                        {
                            'result': search_recipe('Enchiladas with Red Sauce', 'Mexican')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Enchiladas with Green Sauce', 'Mexican')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Enchiladas with Mole Sauce', 'Mexican')['results'][0:5]
                        }
                    ]
                },
                {
                    'question': 'What type of stuffing would you like for your chiles rellenos?',
                    'answers': ['Cheese', 'Beef', 'Vegetables'],
                    'nodes': [
                        {
                            'result': search_recipe('Cheese Stuffed Chiles Rellenos', 'Mexican')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Beef Stuffed Chiles Rellenos', 'Mexican')['results'][0:5]
                        },
                        {
                            'result': search_recipe('Vegetable Stuffed Chiles Rellenos', 'Mexican')['results'][0:5]
                        }
                    ]
                }
            ]
        }]}
    

def decision_tree(node):
    if isinstance(node, dict) and 'answers' in node:
        print(node['answers'])
        answer = input(node['question'])
        while answer not in node['answers']:
            print("Invalid answer. Please try again.")
            answer = input(node['question'])
        next_node = node['nodes'][node['answers'].index(answer)]
        return decision_tree(next_node)
    else:
        return node

def get_recipes():
    results = decision_tree(tree)['results']
    print_recipes(results)

# Results in the form of a JSON dictionary
def print_recipes(results):
    print("Here are the matching recipes:\n")
    print(json.dumps(results, indent=2))


def main():
    print("Welcome to the Personalized Meal Plan Guide!")
    print("Answer the following questions to get a personalized meal plan.")
    get_recipes()

if __name__ == "__main__":
    main()




