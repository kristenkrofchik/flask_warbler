"""User View tests."""

#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app, CURR_USER_KEY


db.create_all()


app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id
        
        self.userb = User.signup("userb", "b@email.com", "bbb", None)
        self.userb_id = 9090
        self.userb.id = self.userb_id

        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        with self.client as c:
            resp = c.get("/users")

            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@userb", str(resp.data))

    def test_user_homepage(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))
            self.assertNotIn("@userb", str(resp.data))

    def setup_like_tests(self):
        m1 = Message(id=123, text="hey", user_id=self.testuser_id)
        m2 = Message(id=456, text="yo", user_id=self.userb_id)

        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()

        testuser_likes = Likes(user_id=self.testuser_id, message_id=456)
        
        db.session.add(testuser_likes)
        db.session.commit()

    def test_show_likes(self):
        self.setup_like_tests()

        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

    def test_add_like(self):
        msg = Message(id=11111, text="Gummy Bear", user_id=self.userb)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/messages/11111/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.message_id==11111).all()
            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.testuser_id)
