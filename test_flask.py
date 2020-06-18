from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly3_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    '''Tests for User views'''
    def setUp(self):
        '''Sample user and post'''
        User.query.delete()
        Post.query.delete()
        user = User(first_name='TestFirstName', last_name="TestLastName", image_url='https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y')
        post = Post(title='Test title', content='Test content')
        db.session.add(post)
        db.session.add(user)
        db.session.commit()
        self.user = user
        self.user_id = user.id
        self.post = post
        self.post_id = post.id
        self.client = app.test_client()

    def tearDown(self):
        '''Reset database.'''
        db.session.rollback()

    # def test_home_page(self):
    #     with self.client as client:
    #         response = client.get('/')
    #         self.assertTrue(response.status_code == 200)
    #
    # def test_users(self):
    #     '''Test route and GET request for users.'''
    #     with self.client as client:
    #         response = client.get('/users')
    #         html = response.get_data(as_text=True)
    #         self.assertTrue(response.status_code == 200)
    #         self.assertIn('TestFirstName', html)

    # def test_users_show(self):
    #     '''Test valid route and GET request for user details'''
    #     with self.client as client:
    #         response = client.get(f'/users/{ self.user_id }')
    #         print(response.status_code)
    #         html = response.get_data(as_text=True)
    #         self.assertTrue(response.status_code == 200)
    #         self.assertIn('TestFirstName', html)

    # def test_create(self):
    #     '''Test valid route and GET method.'''
    #     with self.client as client:
    #         response = client.get('/create')
    #         self.assertTrue(response.status_code == 200)


# ********************* doesn't work  ************

    def test_create_user(self):
        '''Test valid route, create user, save to db, and POST request.'''
        # form data

        with self.client as client:
            # test with None image url
            form = {
                "first_name": "TestFirstName",
                "last_name": "TestLastName",
                "image_url": None,
            }

            # query the database for the user
            user = User.query.first()
            # assert that the info in the database matches the info in the form above
            self.assertTrue(user.first_name == form["first_name"])
            self.assertTrue(user.last_name == form["last_name"])

            # default_image_url = "https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png"
            # self.assertTrue(user.image_url == default_image_url)
            # self.assertTrue(user.image_url == 'https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png')


            # test with image url
            form = {
                "first_name": "Test",
                "last_name": "Test",
                "image_url": "https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png",
            }

            self.assertTrue(user.first_name == form["first_name"])
            self.assertTrue(user.last_name == form["last_name"])
            self.assertTrue(user.image_url == form['https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png'])

            response = client.post("/create_user", data=form)
            self.assertTrue(response.status_code == 302)


    def test_edit_user(self):
        '''Test valid route and GET method, edit form and query of db.'''
        with self.client as client:
            user = {"first_name": "TestFirstName", "last_name": "TestLastName", "image_url": "https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y"}
            # user = self.user
            response = client.get(f'/users/{self.user_id}/edit', user=user, follow_redirects=True)
            self.assertTrue(response.status_code == 200)

    def test_update_user(self):
        '''Test valid route, POST method, collect for data and save to db.'''
        with self.client as client:

            # test with None image url
            form = {
                "first_name": "TestFirstName",
                "last_name": "TestLastName",
                "image_url": None,
            }

            user = User.query.first()

            self.assertTrue(user.first_name == form["first_name"])
            self.assertTrue(user.last_name == form["last_name"])
            # default_image_url = "https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png"
            # self.assertTrue(user.image_url == default_image_url)
            # self.assertTrue(user.image_url == 'https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png')

            # test with image url
            form = {
                "first_name": "Test",
                "last_name": "Test",
                "image_url": "https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png",
            }

            self.assertTrue(user.first_name == form["first_name"])
            self.assertTrue(user.last_name == form["last_name"])
            self.assertTrue(user.image_url == form['https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16671574911586787867-512.png'])

            response = client.post(f"/users/{user_id}/edit", data=form)
            self.assertTrue(response.status_code == 200)

    def