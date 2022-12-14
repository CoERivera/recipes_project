from flask_app import app
from flask import request, render_template, redirect, flash, session
from flask_app.models import user_model, recipe_model


@app.route('/dashboard')
def dashboard():
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')

    return render_template('dashboard.html',recipes=recipe_model.Recipe.get_all_recipes_with_users())

@app.route('/recipes/new')
def new_recipe():
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    return render_template('add.html')

@app.route('/recipes/add', methods=["POST"])
def add_recipe():
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        **request.form,
        'owner_id': session['uid']
    }

    if request.form['under_thirty'] == "Yes":
        data['under_thirty'] = True
    else:
        data['under_thirty'] = False
    recipe =  recipe_model.Recipe.save_recipe(data)

    if not recipe:
        flash('Error in adding recipe.','recipe')
        return redirect('/recipes/new') 
    
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')

    return render_template('view.html',recipe=recipe_model.Recipe.get_one_recipe_with_user(id))

@app.route('/recipes/update/<int:id>', methods=["POST"])
def update_recipe(id):
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    data = {
        **request.form,
        'id': id
    }

    if request.form['under_thirty'] == "Yes":
        data['under_thirty'] = True
    else:
        data['under_thirty'] = False
    
    recipe_model.Recipe.update_recipe(data)
    
    return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    
    recipe = recipe_model.Recipe.get_one_recipe_with_user(id)
    
    if session['uid'] != recipe.owner_id:
        return redirect('/dashboard')
    
    return render_template('modify.html',recipe=recipe)

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    
    if session['uid'] != recipe_model.Recipe.get_one_recipe_with_user(id).owner_id:
        return redirect('/dashboard')
    
    recipe_model.Recipe.remove_recipe(data = {'id':id})
    return redirect('/dashboard')