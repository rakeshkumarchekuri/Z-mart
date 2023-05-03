import pytest
import unittest 

from django.test import RequestFactory 
from django.test import TestCase, Client

from eShopping.views import login_check
from eShopping.views import login_request
from eShopping.views import Homepage 

class TestHomepage(unittest.TestCase): 
    def setUp(self): 
        # Create a request object 
        self.factory = RequestFactory() 
        self.request = self.factory.get('/') 
    def test_homepage(self): 
        response = Homepage(self.request) 
        # Check that the response status code is 200 
        self.assertEqual(response.status_code, 200) 
class Testlogin_request(unittest.TestCase):
    def login(username, password):
    # Perform authentication logic
    # Return True if authentication succeeds, False otherwise
        return username == "sai" and password == "sai"

    def test_login_successful():
        # Arrange
        username = "sai"
        password = "sai"

        # Act
        result = login(username, password)

        # Assert
        assert result == True

    def test_login_unsuccessful():
        # Arrange
        username = "sai"
        password = "incorrect"

        # Act
        result = login(username, password)

        # Assert
        assert result == False
    

if(0):
    def setUp(self): 
        # Create a request object 
        self.factory = RequestFactory() 
        self.request = self.factory.get('/')
        #self.request.META = {'REMOTE_ADDR': '127.0.0.1'}
    def test_login_request(self):
        # Perform the login request with a valid username, password, and OTP
        #request = {'POST': {'login_username': 'sai', 'login_password': 'sai', 'login_otp': '556776'}}
        #response = login_request(request)
        c = Client()
        response = c.post('/login_request/', {'login_username': 'sai', 'login_password': 'sai', 'login_otp': '556776'})
        # Verify that the response is a dictionary
        dict={'login_username': 'sai', 'login_password': 'sai', 'login_otp': '556776'}
        assert isinstance(response, dict)

        # Verify that the dictionary contains the expected keys
        expected_keys = {'product_no_1', 'price_1', 'product_no_2', 'price_2', 'product_no_3', 'price_3'}
        #assert set(response.keys()) == expected_keys

        # Verify that the dictionary values are of the expected type
        #assert all(isinstance(value, str) for value in response.values())

        # Verify that the dictionary values are not empty
        #assert all(len(value) > 0 for value in response.values())

        # Verify that the dictionary values are not equal to the placeholder text
        assert all(value != 'Enter The Item Name' for key, value in response.items() if 'product_no' in key)
        assert all(value != 'Enter The Price' for key, value in response.items() if 'price' in key)