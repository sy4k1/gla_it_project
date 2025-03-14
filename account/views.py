import hashlib
import json
import random
import uuid

from django.core.mail import send_mail
from django.utils import timezone

from account.models import AccountAccessToken, Account, AccountPasscode, Follower
from post.models import LikedPost, Comment
from server.request_helper import validate_request_data
from server.response_helper import generate_failed_response, generate_successful_response, \
    generate_missing_fields_response, \
    generate_account_response, format_comments, format_likes, format_followers


# Create your views here.
def query(request):
    try:
        req = json.loads(request.body)
        access_token = req.get('access_token', None)
        account_id = req.get('id', None)

        if access_token is None and account_id is None:
            return generate_failed_response('Access token and ID are missing!')

        if access_token is None:
            # query other's profile
            account = Account.objects.get(id=account_id)
            followers = Follower.objects.filter(followed_email=account.email).count()
            likes = LikedPost.objects.filter(poster_email=account.email).count()

            return generate_account_response(account, followers, 0, likes)

        # query account
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account = Account.objects.get(email=account_access_token.account_email)

        followers = Follower.objects.filter(followed_email=account.email).count()
        likes = LikedPost.objects.filter(poster_email=account.email).count()

        return generate_account_response(account, followers, 0, likes)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except Account.DoesNotExist:
        return generate_failed_response('Account does not exist!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def logout(request):
    try:
        req = json.loads(request.body)
        access_token = req.get('access_token', None)

        if access_token is None:
            return generate_failed_response('Access token is missing!')

        # delete access token
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account_access_token.delete()

        return generate_successful_response(None)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


max_diff_seconds = 10 * 60  # 10 min


def signup(request):
    try:
        req = json.loads(request.body)

        # validate request body
        missing_fields = validate_request_data(req, ['name', 'email', 'password', 'passcode'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        email = req.get('email', None)
        passcode = req.get('passcode', None)

        # validate passcode
        account_passcode = AccountPasscode.objects.get(account_email=email, passcode=passcode)
        diff = timezone.now() - account_passcode.create_datetime
        if diff.total_seconds() > max_diff_seconds:
            account_passcode.delete()
            return generate_failed_response('Expired passcode!')

        name = req.get('name', None)
        password = req.get('password', None)
        password_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

        # generate a new account
        account = Account(name=name, email=email, password=password_hash)

        # generate a new token
        access_token = uuid.uuid4().hex
        account_access_token = AccountAccessToken(account_email=email, access_token=access_token)

        account.save()
        account_access_token.save()
        account_passcode.delete()

        return generate_account_response(account, 0, 0, 0, access_token)
    except AccountPasscode.DoesNotExist:
        return generate_failed_response('Invalid passcode!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def login(request):
    try:
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['email', 'password'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        email = req.get('email', None)
        password = req.get('password', None)
        password_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

        account = Account.objects.get(email=email, password=password_hash)

        # delete existing tokens
        try:
            AccountAccessToken.objects.get(account_email=account.email).delete()
        except Exception as e:
            # do nothing
            print(e)

        # generate a new token
        access_token = uuid.uuid4().hex
        account_access_token = AccountAccessToken(account_email=account.email, access_token=access_token)
        account_access_token.save()

        followers = Follower.objects.filter(followed_email=account.email).count()
        likes = LikedPost.objects.filter(poster_email=account.email).count()

        return generate_account_response(account, followers, 0, likes, access_token)
    except Account.DoesNotExist:
        return generate_failed_response('Account does not exist!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def send_passcode(request):
    try:
        req = json.loads(request.body)
        email = req.get('email', None)

        if email is None:
            return generate_failed_response('Email address is missing!')

        # generate a new passcode
        passcode = ""
        for _ in range(6):
            passcode += str(random.randint(0, 9))

        # delete expired passcode
        try:
            AccountPasscode.objects.get(account_email=email).delete()
        except Exception as e:
            # do nothing
            print(e)

        # save the new passcode
        account_passcode = AccountPasscode(account_email=email, passcode=passcode)
        account_passcode.save()
        return generate_successful_response(passcode)
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def query_follow_status(request):
    try:
        req = json.loads(request.body)
        access_token = req.get('access_token', None)
        poster_email = req.get('email', None)

        if access_token is None or poster_email is None:
            return generate_failed_response('Access token or email address is missing!')

        # query account
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)

        # query follow status
        follow_status = Follower.objects.filter(follower_email=account_access_token.account_email,
                                                followed_email=poster_email).count() > 0

        return generate_successful_response(follow_status)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except Account.DoesNotExist:
        return generate_failed_response('Account does not exist!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def follow(request):
    try:
        req = json.loads(request.body)
        access_token = req.get('access_token', None)
        target_email = req.get('email', None)

        if access_token is None or target_email is None:
            return generate_failed_response('Access token or ID is missing!')

        # query account
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account = Account.objects.get(email=account_access_token.account_email)

        # query target account
        target_account = Account.objects.get(email=target_email)

        # query follow record
        follow_status = Follower.objects.filter(follower_email=account.email,
                                                followed_email=target_account.email).count() > 0

        # update follow status
        if follow_status:
            Follower.objects.filter(follower_email=account.email, followed_email=target_account.email).delete()
            follow_status = False
        else:
            follower = Follower(follower_email=account.email, follower_name=account.name, follower_id=account.id,
                                followed_email=target_account.email)
            follower.save()
            follow_status = True

        return generate_successful_response(follow_status)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except Account.DoesNotExist:
        return generate_failed_response('Account does not exist!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def query_notification(request):
    try:
        req = json.loads(request.body)
        access_token = req.get('access_token', None)

        if access_token is None:
            return generate_failed_response('Access token is missing!')

        # query account
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account = Account.objects.get(email=account_access_token.account_email)
        account_email = account.email

        # query comments which not read
        comments = Comment.objects.filter(poster_email=account_email, read=False).exclude(
            commentator_email=account_email).order_by('-id')

        # query likes which not read
        likes = LikedPost.objects.filter(poster_email=account_email, read=False).exclude(
            liked_account_email=account_email).order_by('-id')

        # query follower records which not read
        followers = Follower.objects.filter(followed_email=account_email, read=False).order_by('-id')

        data = {
            'comments': format_comments(comments),
            'likes': format_likes(likes),
            'followers': format_followers(followers),
        }

        return generate_successful_response(data)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except Account.DoesNotExist:
        return generate_failed_response('Account does not exist!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def read_notification(request):
    try:
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['access_token', 'id', 'type'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        # validate account access token
        access_token = req.get('access_token', None)
        AccountAccessToken.objects.get(access_token=access_token)

        target_id = req.get('id')
        read_type = req.get('type')

        # update read field
        if read_type == 'comments':
            comment = Comment.objects.get(id=target_id)
            comment.read = True
            comment.save()
        elif read_type == 'likes':
            liked_post = LikedPost.objects.get(id=target_id)
            liked_post.read = True
            liked_post.save()
        elif read_type == 'followers':
            follower = Follower.objects.get(id=target_id)
            follower.read = True
            follower.save()
        else:
            return generate_failed_response('Invalid type!')

        return generate_successful_response(True)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except Account.DoesNotExist:
        return generate_failed_response('Account does not exist!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))
