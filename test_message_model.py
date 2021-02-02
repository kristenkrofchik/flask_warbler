"""Message model tests."""

#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app


db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

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
      