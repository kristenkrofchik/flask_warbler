"""Message model tests."""

#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

"""Set environment variable to use a different database for testing"""
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app


db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 4949
        user = User.signup('msgtestuser', 'testemail@email.com', 'testpassword', None)
        user.id = self.uid
        db.session.commit()
    
        self.user = User.query.get(self.uid)
        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        """Does basic model work?"""

        m = Message(
            text="This is a test.",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "This is a test.")

    def test_message_likes(self):
        msg_1 = Message(
            text="I love pizza!",
            user_id=self.uid
        )

        msg_2 = Message(
            text='I love candy!',
            user_id=self.uid
        )

        new_user = User.signup("sohungry", "food@food.com", "foodpassword", None)
        uid = 888
        new_user.id = uid

        db.session.add(msg_1)
        db.session.add(msg_2)
        db.session.add(new_user)
        db.session.commit()

        new_user.likes.append(msg_1)
        db.session.commit()

        like_list = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(like_list), 1)



      