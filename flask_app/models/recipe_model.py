# Import function to return an instance of the database connection
from flask import flash
from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model

# Modeling the class after the recipes table
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']

    # Create class methods for queries
    
    # Obtains all the recipes
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query)
        
        if results:
            # Create empty list to store all the instances
            recipes = []

            # Iterating through all the results to store recipe
            for recipe in results:
                recipes.append(cls(recipe))
            
            return recipes
        
        return False

    # Save a new recipe
    @classmethod
    def save_recipe(cls,data):
        query = """
            INSERT INTO recipes(name,description,instructions,date_made,under_thirty,owner_id)
            VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_thirty)s,%(owner_id)s);
        """
        # data dictionary will pass will be passed onto saved method from server.py

        return connectToMySQL(DATABASE).query_db(query,data)

    # Obtains a specific recipe
    @classmethod
    def get_one_recipe_with_user(cls,id):
        query = """SELECT * FROM recipes
                JOIN users ON recipes.owner_id = users.id
                WHERE recipes.id = %(id)s;"""
        data = {'id': id}
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        
        recipe = cls(results[0])
        owner_data = {
                **results[0],
                'id': results[0]['users.id'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
            }
        recipe.owner = user_model.User(owner_data)

        return recipe
    
    # Obtains all the recipes and their users
    @classmethod
    def get_all_recipes_with_users(cls):
        query = """SELECT * FROM recipes
                    JOIN users ON recipes.owner_id = users.id"""
        
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        if results:
            # Create empty list to store all the instances
            

            # Iterating through all the results to store user along
            # with recipe information for each user
            for recipe in results:
                one_recipe = cls(recipe)              
                owner_data = {
                    **recipe,
                    'id': recipe['users.id'],
                    'created_at': recipe['users.created_at'],
                    'updated_at': recipe['users.updated_at'],
                }
                one_recipe.owner = user_model.User(owner_data)
                recipes.append(one_recipe)
        
        return recipes

    # Updates recipe info
    @classmethod
    def update_recipe(cls,data):
        query = """UPDATE recipes
                    SET name = %(name)s,
                        description = %(description)s,
                        instructions = %(instructions)s,
                        date_made = %(date_made)s,
                        under_thirty = %(under_thirty)s,
                        updated_at = NOW()
                    WHERE id = %(id)s;"""
        
        # Call the connectToMySQL function to connect to the database
        connectToMySQL(DATABASE).query_db(query,data)

    # Removes recipe
    @classmethod
    def remove_recipe(cls,data):
        query = """DELETE FROM recipes
                    WHERE id = %(id)s;"""
        
        # Call the connectToMySQL function to connect to the database
        connectToMySQL(DATABASE).query_db(query,data)

    
    # Validates recipe information to register it
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        
        # Verifies mininum recipe name length
        if len(recipe['name']) < 3:
            flash('Recipe name must be at least 3 characters.','name')
            is_valid = False
        # Verifies that recipe name has no numbers or special characters
        elif not recipe['name'].isalpha():
            flash('Recipe name must not have any numbers or special characters.','name')
            is_valid = False

        # Verifies description isn't empty
        if len(recipe['description']) < 1:
            flash('Description field must not be empty.','description')
            is_valid = False
        
        # Verifies instructions aren't empty
        if len(recipe['instructions']) < 1:
            flash('Instructions field must not be empty.','instructions')
            is_valid = False
        
        # Verifies date isn't empty
        if len(recipe['date_made']) < 10:
            flash('Must provide a valid date.','date_made')
            is_valid = False

        # Verifies under_thirty isn't empty
        if 'under_thirty' not in recipe:
            flash('Must select is recipe was made under thirty minutes.','under_thirty')
            is_valid = False

        # If no conditionals triggered, returns true
        return is_valid