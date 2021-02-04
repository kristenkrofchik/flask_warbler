"""Message model tests."""

#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes
#from sqlalchemy import exc


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
        db.session.add(user)
        db.session.commit()
    
        self.user = User.query.get(self.uid)
        self.client = app.test_client()
    
    def test_message_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        m = Message(
            text="This is a test.",
            user_id=u.user_id
        )

        db.session.add(u)
        db.session.add(m)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 1)
        self.assertEqual(u.messages[0].text, "This is a test.")

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

        nolikes_list = Likes.query.filter(Likes.user_id == self.uid).all()
        self.assertEqual(len(nolikes_list), 0)


      