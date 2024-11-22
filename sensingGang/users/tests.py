from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class LoginTestCases(TestCase):
    
    # User setup
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
    # Test for login 
    def test_valid_login(self):
        response = self.client.post(reverse('signin'), {'username': self.username, 'password': self.password}, follow = True)
        # Check response status code is 200 (This means OK)
        self.assertEqual(response.status_code, 200)
        # Check if user is then logged in
        self.assertIn('_auth_user_id', self.client.session)
    
    # Test for invalid login and correct error message
    def test_invalid_login(self):
        response = self.client.post(reverse('signin'), {'username': self.username, 'password': 'wrongPassword'}, follow = True)
        # Checking invalid message and OK status code
        self.assertRedirects(response, reverse('signin'))
        # Checking if not in logged in users (no valid session key)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or password is incorrect")
        self.assertNotIn('_auth_user_id', self.client.session)
        
class AccountCreationTestCases(TestCase):
    
    # User setup
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.firstname = 'firstname'
        self.lastname = 'lastname'
        self.email = 'email@gmail.com'
        self.password = 'password'
        self.create_account_url = reverse('signup')
        
    def test_valid_account_creation(self):
        response = self.client.post(self.create_account_url, {'username': self.username , 'firstname': self.firstname ,'lastname': self.lastname ,'email': self.email ,'password': self.password, 'confirmPassword': self.password}, follow=True)
        # Checks for valid redirect to main page
        self.assertRedirects(response, reverse('signin'), status_code=302, target_status_code=200)
        # Verify that the user was created and can log in.
        self.assertEqual(User.objects.count(), 1)
        self.assertIsNotNone(User.objects.get(username=self.username).pk)
        
    def test_duplicate_username(self):
        response = self.client.post(self.create_account_url, {'username': self.username , 'firstname': self.firstname ,'lastname': self.lastname ,'email': self.email ,'password': self.password, 'confirmPassword': self.password}, follow=True)
        response = self.client.post(self.create_account_url, {'username': self.username , 'firstname': self.firstname ,'lastname': self.lastname ,'email': 'difemail@gmail.com' ,'password': self.password, 'confirmPassword': self.password}, follow=True)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username already in use")
        # Check if not user object was created
        self.assertEqual(User.objects.count(), 1)
        
    def test_duplicate_email(self):
        response = self.client.post(self.create_account_url, {'username': self.username , 'firstname': self.firstname ,'lastname': self.lastname ,'email': self.email ,'password': self.password, 'confirmPassword': self.password}, follow=True)
        response = self.client.post(self.create_account_url, {'username': 'difusername' , 'firstname': self.firstname ,'lastname': self.lastname ,'email': self.email ,'password': self.password, 'confirmPassword': self.password}, follow=True)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email already in use")
        # Check if not user object was created
        self.assertEqual(User.objects.count(), 1)   
    
    def test_matching_passwords(self):
        response = self.client.post(self.create_account_url, {'username': self.username , 'firstname': self.firstname ,'lastname': self.lastname ,'email': self.email ,'password': self.password, 'confirmPassword': 'difPassword'}, follow=True)
        # Check for correct message for unmatching passwords
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Passwords do not match")
        # Check if not user object was created
        self.assertEqual(User.objects.count(), 0)
        
    def test_empty_fields(self):
        response = self.client.post(self.create_account_url, {'username': '',  'firstname': '', 'lastname': '', 'email': '', 'password': '', 'confirmPassword': ''}, follow=True)
        # Check for correct message for empty fields
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Fields cannot be empty")
        # Check if not user object was created
        self.assertEqual(User.objects.count(), 0)
        
    def test_alpha_numeric_username(self):
        response = self.client.post(self.create_account_url, {'username': '#%*@!' , 'firstname': self.firstname ,'lastname': self.lastname ,'email': self.email ,'password': self.password, 'confirmPassword': self.password}, follow = True)
        # Check for correct message for unmatching passwords
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username must be Alpha-Numeric")
        # Check if not user object was created
        self.assertEqual(User.objects.count(), 0)
        
