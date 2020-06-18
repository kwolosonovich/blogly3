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
        '''Test valid route and create user.'''
        with self.client as client:


            self.assertEqual(first_name: request.form["TestFirstName"])
            self.assertEqual(last_name: request.form["TestLastName"])
            self.assertEqual(image_url == request.form["None"])

            # new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
            #
            # user = User(first_name='TestFirstName', last_name="TestLastName",
            #             image_url='https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y')

            response = client.get('/users')
            self.first_name = request.form['first_name']

            self.assertTrue(response.status_code == 200)
            self.assertTrue()


    # def test_create_user(self):
    #     '''Test create form request and relationship to database'''
    #
    #
    #         # ******* does not work ********
    #
    # def edit_user(self):
    #     '''Test if update user form is generated.'''
    #     with self.client as client:
    #
    #     user = User(first_name='TestFirstName', last_name="TestLastName", image_url='https://i.picsum.photos/id/1025/4951/3301.jpg?hmac=_aGh5AtoOChip_iaMo8ZvvytfEojcgqbCH7dzaz-H8Y')
    #
    #     response = client.get('/edit_user.html')
    #     html = response.get_data(as_text=True)
    #     self.assertTrue(response.status_code == 200)
    #     self.assertIn("<h1>Edit {{ first_name }} Profile</h1>", html)
    #

