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
Open a web browser and go to http://localhost:5000 to interact with the program.
