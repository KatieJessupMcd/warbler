"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test-again"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.user1 = User(username="user1", email="user1@123.com", image_url="abc", header_image_url="abc", bio="i am awesome", location="nonesuch", password="123456")
        self.user2 = User(username="user2", email="user2@123.com", header_image_url="", bio="i am great", location="nowhere", password="abcdefg")
        self.new_user = User.signup(username="test", email="test@test.com", password="abcd123", image_url="")
        # self.follows2 = FollowersFollowee(self.user2.id, self.user1.id)
        db.session.add_all([self.user1, self.user2])
        db.session.commit()
        
        # import pdb; pdb.set_trace()
        self.follows1 = FollowersFollowee(followee_id=self.user1.id, follower_id=self.user2.id)
        
        db.session.add(self.follows1)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test1@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        # user1 and user2 should be instances of User class
        self.assertIsInstance(self.user1, User)
        self.assertIsInstance(self.user2, User)

        # testing attributes of each user instance
        self.assertEqual(self.user1.username, "user1")
        self.assertEqual(self.user1.email, "user1@123.com")
        self.assertEqual(self.user1.image_url, "abc")
        self.assertEqual(self.user1.header_image_url, "abc")
        self.assertEqual(self.user1.bio, "i am awesome")
        self.assertEqual(self.user1.location, "nonesuch")
        self.assertEqual(self.user1.password, "123456")

        self.assertEqual(self.user2.username, "user2")
        self.assertEqual(self.user2.email, "user2@123.com")
        self.assertEqual(self.user2.image_url, "/static/images/default-pic.png")
        self.assertEqual(self.user2.header_image_url, "")
        self.assertEqual(self.user2.bio, "i am great")
        self.assertEqual(self.user2.location, "nowhere")
        self.assertEqual(self.user2.password, "abcdefg")

    def test_repr(self):
        """Does the repr method work as expected?"""
        self.assertEqual(repr(self.user1), f"<User #{self.user1.id}: {self.user1.username}, {self.user1.email}>")
        self.assertEqual(repr(self.user2), f"<User #{self.user2.id}: {self.user2.username}, {self.user2.email}>")

    def test_is_following_method_true(self):
        """does is_following successfully detect when user1 is following user2"""

        # import pdb; pdb.set_trace()
        self.assertIn(self.user1, self.user2.followers)

    def test_is_following_method_false(self):
        """does is_following successfully detect when user1 is not following user2"""
        self.assertNotIn(self.user2, self.user1.followers)

    def test_is_followed_by_true(self):
        """Does is_followed_by successfully detect when user1 is followed by user2"""

        self.assertIn(self.user2, self.user1.following)

    def test_is_followed_by_false(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2"""

        self.assertNotIn(self.user1, self.user2.following)
    

    def test_user_signup(self):
        """does User.signup successfully create a new user given valid credentials that it is added to DB"""

        self.assertEqual(self.new_user.username, "test")
        self.assertEqual(self.new_user.email, "test@test.com")
        self.assertNotEqual(self.new_user.password, "abcd123")
        self.assertEqual(self.new_user.image_url, "")

    def test_user_authenticate_success(self):
        """Does User.authenticate successfully return a user when given a valid username and password"""

        autheticate_new_user = User.authenticate(self.new_user.username, "abcd123")

        self.assertEqual(autheticate_new_user, self.new_user)

    def test_user_authenticate_username_fail(self):
        """Does User.authenticate fail to return a user when the username is invalid"""
        autheticate_new_user = User.authenticate("random", "abcd123")

        self.assertEqual(autheticate_new_user, False)

    def test_user_authenticate_password_fail(self):
        """Does User.authenticate fail to return a user when the password is invalid"""
        autheticate_new_user = User.authenticate(self.new_user.username, "abcd567")

        self.assertEqual(autheticate_new_user, False)
        

