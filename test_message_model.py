"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase
from datetime import datetime

from models import db, User, Message, FollowersFollowee, Like

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


class MessageModelTestCase(TestCase):
    """Test models for messages."""

    def setUp(self):
        """Create test message, add sample data."""

        self.user1 = User(
            username="user1",
            email="user1@123.com",
            image_url="abc",
            header_image_url="abc",
            bio="i am awesome",
            location="nonesuch",
            password="123456")
        self.user2 = User(
            username="user2",
            email="user2@123.com",
            header_image_url="",
            bio="i am great",
            location="nowhere",
            password="abcdefg")

        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        self.message1 = Message(text="abc", user_id=self.user1.id)
        self.message2 = Message(text="testing", user_id=self.user1.id)

        # self.user2 = User(username="user2", email="user2@123.com", header_image_url="", bio="i am great", location="nowhere", password="abcdefg")
        # self.new_user = User.signup(username = "test", email="test@test.com", password="abcd123", image_url="")
        # self.follows2 = FollowersFollowee(self.user2.id, self.user1.id)
        db.session.add_all([self.message1, self.message2])
        # ^^needed to add add_all message2 as well
        db.session.commit()

        # import pdb; pdb.set_trace()

        self.client = app.test_client()

    def tearDown(self):
        """Rest after testing"""
        User.query.delete()
        Message.query.delete()
        Like.query.delete()
        db.session.commit()

    def test_message_model(self):
        """test the attributes of messages"""

        u = User(
            email="test1@test.com",
            username="testuser",
            password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        m = Message(text="texttest", user_id=u.id)

        db.session.add(m)
        db.session.commit()

        # Message should have no likes
        self.assertEqual(len(m.users_like), 0)
        self.assertEqual(len(u.liked_msgs), 0)

        # me should be instances of Message class
        self.assertIsInstance(self.message1, Message)

        # testing attributes of each Message instance
        self.assertEqual(self.message1.text, "abc")
        self.assertEqual(self.message1.user_id, self.user1.id)
        self.assertIsInstance(self.message1.timestamp, datetime)
        self.assertEqual(self.message2.text, "testing")
        self.assertEqual(self.message2.user_id, self.user1.id)
        self.assertIsInstance(self.message2.timestamp, datetime)
        

    def test_is_msg1_created_by_user1_true(self):
        """is msg1 created by user1"""

        self.assertIn(self.message1, self.user1.messages)

    def test_is_msg1_created_by_user1_false(self):
        """is msg1 created by user2"""

        self.assertNotIn(self.message1, self.user2.messages)

    def test_is_user1_creator_of_msg1(self):
        """is user1 the creator of msg1"""

        self.assertEqual(self.message1.user, self.user1)

    def test_is_user1_creator_of_msg2(self):
        """is user1 the creator of msg2"""

        self.assertEqual(self.message2.user, self.user1)

    def test_is_user2_creator_of_msg2_false(self):
        """is user2 the creator of msg2 - false"""
        self.assertNotEqual(self.message2.user, self.user2)
    
    def test_is_user2_creator_of_msg1_false(self):
        """is user2 the creator of msg1 - false"""
        self.assertNotEqual(self.message1.user, self.user2)

