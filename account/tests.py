from django.test import TestCase

from account.models import Account, AccountAccessToken, AccountPasscode, Follower
from django.urls import reverse


# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(email='xi4f3i@gmail.com', name='xi4f3i',
                               password='7fcf4ba391c48784edde599889d6e3f1e47a27db36ecc050cc92f259bfac38afad2c68a1ae804d77075e8fb722503f3eca2b2c1006ee6f6c7b7628cb45fffd1d')
        AccountAccessToken.objects.create(account_email='xi4f3i@gmail.com', access_token='123456')
        AccountPasscode.objects.create(account_email='xi4f3i@gmail.com', passcode='123456')
        Follower.objects.create(follower_email='xi4f3i@gmail.com', follower_name='xi4f3i', follower_id=1,
                                followed_email='<EMAIL>')

    def test_account_creation(self):
        obj = Account.objects.get(email='xi4f3i@gmail.com')
        self.assertEqual(obj.name, 'xi4f3i')

    def test_account_access_token(self):
        obj = AccountAccessToken.objects.get(account_email='xi4f3i@gmail.com')
        self.assertEqual(obj.access_token, '123456')

    def test_account_passcode(self):
        obj = AccountPasscode.objects.get(account_email='xi4f3i@gmail.com')
        self.assertEqual(obj.passcode, '123456')

    def test_follower(self):
        obj = Follower.objects.get(follower_email='xi4f3i@gmail.com')
        self.assertEqual(obj.read, False)


class AccountViewTestCase(TestCase):
    def setUp(self):
        Account.objects.create(email='xi4f3i@gmail.com', name='xi4f3i',
                               password='7fcf4ba391c48784edde599889d6e3f1e47a27db36ecc050cc92f259bfac38afad2c68a1ae804d77075e8fb722503f3eca2b2c1006ee6f6c7b7628cb45fffd1d')
        Account.objects.create(email='aaaa@gmail.com', name='aaaa',
                               password='7fcf4ba391c48784edde599889d6e3f1e47a27db36ecc050cc92f259bfac38afad2c68a1ae804d77075e8fb722503f3eca2b2c1006ee6f6c7b7628cb45fffd1d')
        AccountAccessToken.objects.create(account_email='xi4f3i@gmail.com', access_token='123456')
        AccountPasscode.objects.create(account_email='xi4f3i@gmail.com', passcode='123456')
        Follower.objects.create(follower_email='xi4f3i@gmail.com', follower_name='xi4f3i', follower_id=1,
                                followed_email='<EMAIL>')

    def test_query(self):
        response = self.client.post('/api/account/query', {'id': 1},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        # self.assertEqual(response_data["code"], 1)
        self.assertEqual(response_data["data"]["id"], 1)

    def test_logout(self):
        response = self.client.post('/api/account/logout', {'access_token': '123456'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)

    def test_login(self):
        response = self.client.post('/api/account/login', {'email': 'xi4f3i@gmail.com', 'password': 'admin123'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(response_data["data"]["id"], 1)

    def test_read_notification(self):
        response = self.client.post('/api/account/read_notification',
                                    {'access_token': '123456', 'type': 'followers', 'id': 1},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(response_data["data"], True)

    def test_query_follow_status(self):
        response = self.client.post('/api/account/query_follow_status',
                                    {'access_token': '123456', 'email': 'aaaa@gmail.com'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(response_data["data"], False)