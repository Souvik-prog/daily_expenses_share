from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

class ExpenseSharingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('create_user')
        self.add_expense_url = reverse('add_expense')
        
        # Create users
        self.user_data_1 = {
            'email': 'john.doe@example.com',
            'name': 'John Doe',
            'mobile': '1234567890',
            'password': 'password123'
        }
        self.user_data_2 = {
            'email': 'friend1@example.com',
            'name': 'Friend 1',
            'mobile': '1234567891',
            'password': 'password123'
        }
        self.user_data_3 = {
            'email': 'friend2@example.com',
            'name': 'Friend 2',
            'mobile': '1234567892',
            'password': 'password123'
        }

    def test_create_user(self):
        """Test user creation"""
        response = self.client.post(self.create_user_url, self.user_data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

    def test_add_expense_percentage_split(self):
        """Test adding an expense with percentage split"""

        # Create users
        self.client.post(self.create_user_url, self.user_data_1, format='json')
        self.client.post(self.create_user_url, self.user_data_2, format='json')
        self.client.post(self.create_user_url, self.user_data_3, format='json')

        # Define participants with percentage split
        participant_data = [
            {"email": "john.doe@example.com", "percentage": 50},
            {"email": "friend1@example.com", "percentage": 25},
            {"email": "friend2@example.com", "percentage": 25}
        ]
        
        expense_data = {
            "description": "Party",
            "amount": "4000",
            "payer_email": "john.doe@example.com",
            "split_method": "percentage",
            "participants": participant_data
        }
        
        response = self.client.post(self.add_expense_url, expense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Expense added successfully')

    def test_add_expense_exact_split(self):
        """Test adding an expense with exact split"""

        # Create users
        self.client.post(self.create_user_url, self.user_data_1, format='json')
        self.client.post(self.create_user_url, self.user_data_2, format='json')
        self.client.post(self.create_user_url, self.user_data_3, format='json')

        # Define participants with exact amounts
        participant_data = [
            {"email": "john.doe@example.com", "amount": "1000"},
            {"email": "friend1@example.com", "amount": "2000"},
            {"email": "friend2@example.com", "amount": "1000"}
        ]
        
        expense_data = {
            "description": "Shopping",
            "amount": "4000",
            "payer_email": "john.doe@example.com",
            "split_method": "exact",
            "participants": participant_data
        }
        
        response = self.client.post(self.add_expense_url, expense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Expense added successfully')