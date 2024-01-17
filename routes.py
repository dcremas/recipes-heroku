from flask import render_template, redirect, url_for, flash
from app import app, db, login_manager
from models import Authors, Recipes
from forms import SignupForm, RecipeForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required


@login_manager.user_loader
def load_user(id):
    return Authors.query.get(int(id))


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        author = Authors.query.filter_by(email=form.email.data).first()
        if author is None or not author.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(author, form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        author = Authors(username=form.username.data,
                    email=form.email.data)
        author.set_password(form.password.data)
        db.session.add(author)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('create_account.html', form=form)


@app.route('/create_recipe', methods=["GET", "POST"])
@login_required
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipes(category=form.category.data,
                         title=form.title.data,
                         prep_time=form.prep_time.data,
                         cooking_time=form.cooking_time.data,
                         yield_amount=form.yield_amount.data,
                         ingredients=form.ingredients.data,
                         instructions=form.instructions.data,
                         tips=form.tips.data,
                         author=current_user,
                         )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipes'))
    return render_template('create_recipe.html', form=form)


@app.route('/recipes')
def recipes():
    current_recipes = db.session.scalars(db.select(Recipes)).all()
    return render_template('recipes.html', recipes=current_recipes)


@app.route('/recipes_table')
def recipes_table():
    current_recipes = db.session.scalars(db.select(Recipes)).all()
    return render_template('recipes_table.html', recipe_data=current_recipes)


@app.route('/<int:recipe_id>/')
def recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)
    image_name = recipe.title.lower().replace(" ", "")
    image_file = url_for('static', filename=image_name + '.jpg')
    return render_template('recipe.html',
                           recipe=recipe,
                           image=image_file,
                           ingredients=recipe.ingredients.split("\r\n"),
                           instructions=recipe.instructions.split("\r\n"),
                           tips=recipe.tips.split("\r\n"))
