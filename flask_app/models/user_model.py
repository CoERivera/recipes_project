# Import function to return an instance of the database connection
from flask_app import app, DATABASE, bcrypt
from flask_app.models import recipe_model
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Obtain all users
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query)
        
        if results:
            # Create empty list to store all the instances
            users = []

            # Iterating through all the results to store user
            for user in results:
                users.append(cls(user))
            
            return users
        
        return False

    #Create a new account for a user
    @classmethod
    def create_user(cls,data):
        query = """INSERT INTO users(first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"""

        return connectToMySQL(DATABASE).query_db(query,data)

    # Obtains a specific email
    @classmethod
    def get_email(cls,data):
        query = """SELECT * FROM users
                WHERE email = %(email)s;"""
        
        # Call the connectToMySQL function to connect to the database
        user = connectToMySQL(DATABASE).query_db(query,data)

        if user:
            return cls(user[0])
            
        return False


    # Updates user info
    @classmethod
    def update_user(cls,data):
        query = """UPDATE users
                    SET first_name = %(first_name)s,
                        last_name = %(last_name)s,
                        email = %(email)s,
                        password = %(password)s,
                        updated_at = NOW()
                    WHERE id = %(id)s;"""
        
        # Call the connectToMySQL function to connect to the database
        connectToMySQL(DATABASE).query_db(query,data)

    # Removes user
    @classmethod
    def delete_user(cls,data):
        query = """DELETE FROM users
                    WHERE id = %(id)s;"""
        
        # Call the connectToMySQL function to connect to the database
        connectToMySQL(DATABASE).query_db(query,data)

    
    
    # Validates user information to register them
    @staticmethod
    def validate_registration(user):
        is_valid = True
        
        # Verifies mininum first name length
        if len(user['first_name']) < 3:
            flash('First name must be at least 3 characters.','first_name')
            is_valid = False
        # Verifies that first name has no numbers or special characters
        elif not user['first_name'].isalpha():
            flash('First name must not have any numbers or special characters.','first_name')
            is_valid = False

        # Verifies mininum last name length
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 characters.','last_name')
            is_valid = False
        # Verifies that first name has no numbers or special characters
        elif not user['first_name'].isalpha():
            flash('Last name must not have any numbers or special characters.','last_name')
            is_valid = False
        
        # Verifies mininum email length
        if len(user['email']) < 5:
            flash('Email address must be at least 5 characters.','email')
            is_valid = False
        # Verifies correct email format
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address format.",'email')
            is_valid = False
        # Verifies email address not already in database
        elif User.get_email(user) != False:
            flash('Email address already registered.','email')
            is_valid = False

        # Verifies mininum password length
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.','password')
            is_valid = False

        # Verifies password and confirm_password match
        elif user['password'] != user['confirm_password']:
            flash('Passwords must match.','confirm_password')
            is_valid = False
        
        # If no conditionals triggered, returns true
        return is_valid

    # Ensures email and password are correct to create the session and log them in
    @staticmethod
    def validate_login(user):
        # If either email or password fields are empty, returns false
        if len(user['password']) < 1 or len(user['email']) < 1:
            return False
        
        login_check = User.get_email(user)
        # Compares hash to user password to see if they match
        if not bcrypt.check_password_hash(login_check.password, user['password']):    
            return False
        
        return login_check