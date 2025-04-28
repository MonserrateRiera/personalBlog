# import unittest
# from flask import Flask, session
# from services.auth_service import AuthService

# class TestAuthService(unittest.TestCase):
#     def setUp(self):
#         # Set up a Flask app context for testing
#         self.app = Flask(__name__)
#         self.app.secret_key = "test_secret_key"
#         self.client = self.app.test_client()  # Create a test client
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#     def tearDown(self):
#         # Tear down the Flask app context
#         self.app_context.pop()

#     def test_try_login_success(self):
#         with self.client:  # Use the test client to create a request context
#             result = AuthService.try_login("admin", "admin")
#             self.assertTrue(result)
#             #self.assertIn("username", session)
#             #self.assertEqual(session["username"], "admin")

#     def test_try_login_failure(self):
#         with self.client:  # Use the test client to create a request context
#             result = AuthService.try_login("user", "wrong_password")
#             self.assertFalse(result)
#             #self.assertNotIn("username", session)

#     # def test_try_logout(self):
#     #     with self.client:  # Use the test client to create a request context
#     #         session["username"] = "admin"
#     #         result = AuthService.try_logout()
#     #         self.assertTrue(result)

# if __name__ == "__main__":
#     unittest.main()