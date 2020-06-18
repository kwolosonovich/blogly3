from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route("/create", methods=["GET"])
def create():
    '''Create new user form'''
    return render_template('/create_user.html')


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    '''Create a new user.'''

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/edit_user.html', user=user)


@app.route("/users/<user_id>/edit", methods=["POST"])
def update_user(user_id):
    '''Collect user updates and update database.'''

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/delete")
def delete_user(user_id):
    '''Delete user form'''

    user = User.get_by_id(user_id)

    # return render_template("/delete_user.html", user_id=user_id, first_name=first_name, last_name=last_name, image_url=image_url)
    return render_template("/delete_user.html", user_id=user_id, user=user)


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete(user_id):
    '''Delete user from users'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/post/new")
def post_new(user_id):
    '''Create post form.'''

    user = User.query.get_or_404(user_id)
    return render_template("/post_form.html", user=user)


@app.route("/users/<user_id>/post/new", methods=["POST"])
def post(user_id):
    '''Get post and save post to database'''

    title = request.form["title"]
    content = request.form["content"]
    user_id = user_id
    user = User.query.get_or_404(user_id)
    new_post = Post(title=title, content=content, user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/post/<post_id>")
def post_details(post_id):
    '''Show post details'''

    post = Post.query.get_or_404(post_id)

    return render_template('posts/show.html', post=post)


@app.route('/post/<post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_edit.html', post=post)


@app.route('/post/<post_id>/edit', methods=['POST'])
def posts_update(post_id):
    '''Save updated post to database'''

    print("post_update")
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/post/<post_id>/delete", methods=['POST'])
def post_delete(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/tags')
def tags_index():
    '''Show all tags.'''

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def new_tag():
    '''Render create tag form'''

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def save_tag():
    '''Save tag to database.'''

    for num in request.form.getlist("posts"):
        print(num)

    print(num)

    post_ids = [int(num) for num in request.form.getlist("posts")]
    print(num)
    print(post_ids)
    post = [request.form.getlist("posts")]
    print(post)
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/new', methods=["POST"])
def save_tag():
    '''Save tag to database.'''
    print("******************************************")
    print(request.form.getlist("posts"))
    for num in request.form.getlist("posts"):
        print(num)
    print("******************************************")
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tag/<tag_id>')
def tags_show(tag_id):
    '''Show tag details.'''
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    '''Edit tag'''
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


