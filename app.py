from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

db.drop_all()

db.create_all()

@app.route("/")
def home_page():
    '''Home Page with user list'''

    return render_template('home.html')


@app.route("/users")
def users():
    '''Show all users'''
    all_users = User.query.all()

    return render_template('users.html', users=all_users)


@app.route("/create", methods=["GET"])
def create():
    '''Create new user form'''
    return render_template('/create_user.html')


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    '''Create a new user.'''

    form_req = request.form['submit']

    if form_req == "cancel":
        return redirect("/users")

    elif form_req == "create":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"] or None
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/users")


@app.route("/edit/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    '''Generate update user form.'''

    user = User.get_by_id(user_id)
    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template("/edit_user.html", user_id=user_id, first_name=first_name, last_name=last_name, image_url=image_url)

@app.route("/users/<user_id>/edit", methods=["GET", "POST"])
def submit_updates(user_id):
    '''Collect user updates and update database.'''
    if request.form['submit'] == "cancel":
        return redirect("/users")

    elif request.form['submit'] == "save":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"]
        user = User.get_by_id(user_id)

        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url

        db.session.commit()

        return redirect("/users")

@app.route("/users/<user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):
    '''Delete user form'''

    user = User.get_by_id(user_id)
    first_name = user.first_name
    last_name = user.last_name
    image_url = user.image_url

    return render_template("/delete_user.html", user_id=user_id, first_name=first_name, last_name=last_name, image_url=image_url)


@app.route("/users/<user_id>/delete_user", methods=["GET", "POST"])
def delete(user_id):
    '''Delete user from users'''

    if request.form['submit'] == "cancel":
        return redirect("/users")

    elif request.form['submit'] == "delete":
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return redirect("/users")


@app.route("/users/<user_id>/post", methods=["GET", "POST"])
def post_new(user_id):
    '''Create post form.'''

    user = User.query.get_or_404(user_id)
    first_name = user.first_name
    last_name = user.last_name

    return render_template("/post_form.html", user_id=user_id, first_name=first_name, last_name=last_name)


@app.route("/post/<user_id>/new", methods=["POST"])
def post(user_id):
    '''Get post and save post to database'''

    if request.form['submit'] == "cancel":
        return redirect("/users")

    elif request.form['submit'] == "create":
        title = request.form["title"]
        content = request.form["content"]
        user_id = user_id
        user = User.query.get_or_404(user_id)
        new_post = Post(title=title, content=content, user=user)

        db.session.add(new_post)
        db.session.commit()

        return render_template('/post_details.html', post=new_post, user=user)

@app.route("/post/<user_id>/detail", methods=['GET', 'POST'])
def post_details(user_id):
    '''Show post details'''

    user = User.query.get_or_404(user_id)
    title = post.title
    content = post.content



    # ************* can't get post_id' ***************



    return render_template('/post_details.html', title=title, content=content, user=user)

    # ***** need to add post_id ******

# # @app.route("/post/<post_id>/options", methods=['GET', 'POST'])
# @app.route("/post/options", methods=['GET', 'POST'])
# def post_options():
#     '''Post options'''
#
#     print('post_id')
#     print('post.id')
#
#
#     # if request.form['submit'] == "edit":
#     #     return redirect("/post/edit")
#
#     elif request.form['submit'] == "delete":
#         return redirect("/post/delete")


@app.route('/post/<post_id>/edit', methods=['GET', 'POST'])
def posts_edit():
    """Show a form to edit an existing post"""

    # post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)

# @app.route('/posts/<post_id>/save', methods=['GET', 'POST'])
# def post_save(post_id):
#
#     if request.form['submit'] == "cancel":
#         return redirect("/users")
#
#     elif request.form['submit'] == "create":
#         post = Post.query.get_or_404(post_id)
#         post.title = request.form['title']
#         post.content = request.form['content']
#
#         db.session.add(post)
#         db.session.commit()
#
#         return redirect('/users')
#
@app.route("/post/<post_id>/delete", methods=['GET', 'POST'])
def post_delete(post_id):

    if request.form['submit'] == "cancel":
        return redirect("/users")

    elif request.form['submit'] == "delete":

        post = Post.query.get_or_404(post_id)

        db.session.delete(post)
        db.session.commit()

        return redirect('/users')
