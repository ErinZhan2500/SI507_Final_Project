import json
from FinalProject import search_recipe


class MealPlanNode:
    def __init__(self, question, options):
        self.question = question
        self.options = options
        self.children = {}

    def add_child(self, key, child_node):
        self.children[key] = child_node

class MealPlanTree:
    def __init__(self):
        # Initialize the root node
        self.root = MealPlanNode('Are you a vegeterian?', ['Yes', 'No'])

        # Add child nodes
        Vegeterian_node = MealPlanNode('What is your preferred protein source?', ['Tofu', 'Beans', 'Quinoa'])
        Meat_node = MealPlanNode('What is your preferred protein source?', ['Beef', 'Chicken', 'Fish'])
        
        # Add grandchild nodes for vegetarian node
        tofu_node = MealPlanNode('What type of cuisine do you prefer?', ['Chinese', 'Mexican', 'European'])
        beans_node = MealPlanNode('What type of cuisine do you prefer?', ['Chinese', 'Mexican', 'European'])
        quinoa_veg = MealPlanNode('What type of cuisine do you prefer?', ['Chinese', 'Mexican', 'European'])

        # Add grandchild nodes for meat-eater node
        beef_node = MealPlanNode('What type of cuisine do you prefer?', ['Chinese', 'Mexican', 'European'])
        chicken_node = MealPlanNode('What type of cuisine do you prefer?', ['Chinese', 'Mexican', 'European'])
        fish_node = MealPlanNode('What type of cuisine do you prefer?', ['Chinese', 'Mexican', 'European'])

        # Add great-grandchild nodes for vegetarian node
        asian_node = MealPlanNode('What is your preferred cooking time?', ['15 minutes', '30 minutes', '60 minutes'])
        mexican_node = MealPlanNode('What is your preferred cooking time?', ['15 minutes', '30 minutes', '60 minutes'])
        italian_node_veg = MealPlanNode('What is your preferred cooking time?', ['15 minutes', '30 minutes', '60 minutes'])
        indian_node = MealPlanNode('What is your preferred cooking time?', ['15 minutes', '30 minutes', '60 minutes'])


    #def tree_to_dict(self, node):
        #if not node.children:
            #return node.options
        #else:
            #return {node.question: {k: MealPlanTree.tree_to_dict(v) for k, v in node.children.items()}}
    

    # Save dictionary as JSON file
    #with open('meal_plan_tree.json', 'w') as f:
        #json.dump(tree_dict, f)




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
                    'answers': ['Ravioli', 'Lasagna', 'Fettuccine'],
                    'nodes': [
                        {
                            'result': search_recipe('Ravioli', 'Italian')['results'][0:5]
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


with open('decision_tree.json', 'w') as f:
    json.dump(tree, f)