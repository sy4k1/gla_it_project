from django.test import TestCase

from account.models import Account, AccountAccessToken, AccountPasscode, Follower
from post.models import Post, Comment


# Create your tests here.
class PostViewTestCase(TestCase):
    def setUp(self):
        Account.objects.create(email='xi4f3i@gmail.com', name='xi4f3i',
                               password='7fcf4ba391c48784edde599889d6e3f1e47a27db36ecc050cc92f259bfac38afad2c68a1ae804d77075e8fb722503f3eca2b2c1006ee6f6c7b7628cb45fffd1d')
        Account.objects.create(email='aaaa@gmail.com', name='aaaa',
                               password='7fcf4ba391c48784edde599889d6e3f1e47a27db36ecc050cc92f259bfac38afad2c68a1ae804d77075e8fb722503f3eca2b2c1006ee6f6c7b7628cb45fffd1d')
        AccountAccessToken.objects.create(account_email='xi4f3i@gmail.com', access_token='123456')
        AccountPasscode.objects.create(account_email='xi4f3i@gmail.com', passcode='123456')
        Follower.objects.create(follower_email='xi4f3i@gmail.com', follower_name='xi4f3i', follower_id=1,
                                followed_email='<EMAIL>')
        Post.objects.create(title='Post Title', content='Post Content', poster_email='xi4f3i@gmail.com', poster_id=1,
                            poster_name='xi4f3i', likes=0, channel='Western_Cuisine')
        Post.objects.create(title='Post Title 2', content='Post Content 2', poster_email='xi4f3i@gmail.com',
                            poster_id=1, poster_name='xi4f3i', likes=0, channel='Western_Cuisine')
        Comment.objects.create(post=Post.objects.get(id=1), poster_email='xi4f3i@gmail.com',
                               commentator_email='aaaa@gmail.com', commentator_id=2, commentator_name='aaaa',
                               comment='aaaa comment 1')
        Comment.objects.create(post=Post.objects.get(id=1), poster_email='xi4f3i@gmail.com',
                               commentator_email='aaaa@gmail.com', commentator_id=2, commentator_name='aaaa',
                               comment='aaaa comment 2')
        Comment.objects.create(post=Post.objects.get(id=1), poster_email='xi4f3i@gmail.com',
                               commentator_email='aaaa@gmail.com', commentator_id=2, commentator_name='aaaa',
                               comment='aaaa comment 3')

    def test_query(self):
        response = self.client.post('/api/post/query', {'type': 'All'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(len(response_data["data"]), 2)

    def test_query_comments(self):
        response = self.client.post('/api/post/query_comments', {'id': 1},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(len(response_data["data"]), 3)

    def test_query_like_status(self):
        response = self.client.post('/api/post/query_like_status', {'id': 1, 'access_token': '123456'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(response_data["data"], False)

    def test_comment(self):
        response = self.client.post('/api/post/comment',
                                    {'id': 1, 'access_token': '123456', 'comment': 'test comment 1'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["code"], 1)
        self.assertEqual(len(response_data["data"]), 1)
