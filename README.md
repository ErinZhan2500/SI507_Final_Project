# SI507_Final_Project

This program is a recipe recommendation system that prompts the user with a series of questions to determine their desired cuisine and type of dish. 
The program uses a decision tree to guide the user through the process of selecting a recipe. 
Once the user has selected a recipe, the program uses the Spoonacular API to provide a list of ingredients and instructions.
User can enter the ingredients they are missing for making the dish, and the program can accesse Kroger database to give users the price of each missing ingredient to help them with grocery budgeting.

Special requirements:

Python 3
Flask
Requests
textwrap 

Instructions:

Clone the repository to your local machine.
Install the required packages using pip.
Obtain an authorization code from the Kroger API by visiting the authorization URL in your web browser and completing the authentication flow.
Update the auth_code, client_id, and client_secret variables at the bottom of FinalProject.py with your own values.
Run FinalProject.py.
The flask will be runnning and you can see "Running on http://127.0.0.1:5000".
Go to the link and the application will open in a browser. 

Data Structure: 

I'm using a decision tree to guide users in selecting a recipe based on their cuisine preference and dish type. At the top level, there is a dictionary containing a 'question' key that prompts the user to select a type of cuisine they would like to cook. The 'answers' key contains a list of possible choices the user can make, which are Italian, Asian, or Mexican.

The 'nodes' key then contains another list of dictionaries, where each dictionary represents a branching point in the decision tree. Each of these dictionaries contains a 'question' key that prompts the user to select a more specific dish within the cuisine they chose. The 'answers' key then contains a list of possible choices for that specific dish.

The final layer of each branch contains a dictionary with a 'result' key that stores the top 5 recipe search results from the FinalProject module for the chosen dish and cuisine.

All of this information is stored in a JSON file called 'decision_tree.json' using the 'json' library in Python.






