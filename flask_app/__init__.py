#__init__.py
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "i am stuck in this tree, send help"
bcrypt = Bcrypt(app)    # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

DATABASE = "recipes_schema"