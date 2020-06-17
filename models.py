import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    '''Connect to database.'''
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User model.'''
    __tablename__ = 'Users'

    default_image_url = "https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.String(200),
                          nullable=False,
                          default=default_image_url)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


    @classmethod
    def get_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        return user


class Post(db.Model):
    '''Post model.'''
    __tablename__ = "Posts"

    id = db.Column(db.Integer,
                   primary_key=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags",
    )