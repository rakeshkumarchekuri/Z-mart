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
