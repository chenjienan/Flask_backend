import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])


    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            # call post with data: username, email
            response = self.client.post(
                '/users',                           # route
                data=json.dumps({                   # data
                    'username': 'michael',
                    'email': 'michael@mherman.org'
                }),
                content_type='application/json',    # content type
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('michael@mherman.org was added!', data['message'])
            self.assertIn('success', data['status'])


    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),                # empty data
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])


    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org'
                }),
                content_type='application/json',
            )
            response = self.client.post(            # post twice with the same email
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email already exists.', data['message'])
            self.assertIn('fail', data['status'])


    def test_single_user(self):
        user = add_user('Terence', 'terencechen@gmail.com')

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Terence', data['data']['username'])
            self.assertIn('terencechen@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])


    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])


    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])


    def test_all_users(self):
        add_user('tester1', 'tester1@test.com')
        add_user('tester2', 'tester2@test.com')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('tester1', data['data']['users'][0]['username'])
            self.assertIn('tester1@test.com', data['data']['users'][0]['email'])
            self.assertIn('tester2', data['data']['users'][1]['username'])
            self.assertIn('tester2@test.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

if __name__ == '__main__':
    unittest.main()