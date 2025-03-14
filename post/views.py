import json

from account.models import AccountAccessToken, Account
from post.models import Post, LikedPost, Comment
from server.request_helper import validate_request_data
from server.response_helper import generate_failed_response, generate_successful_response, generate_posts_response, \
    generate_missing_fields_response, generate_comments_response

# valid query types
types = ['publish', 'like', 'explore', 'All', 'Vegetarian_Cuisine', 'Chinese_Cuisine', 'Western_Cuisine',
         'Japanese_Cuisine', 'Desserts', 'Soups']


# Create your views here.
def query(request):
    try:
        req = json.loads(request.body)
        query_type = req.get('type')

        # validate type
        if query_type not in types:
            return generate_failed_response('Invalid type!')

        email = req.get('email')
        if query_type == 'publish' or query_type == 'like':
            if email is None:
                return generate_failed_response('Invalid email address!')

        if query_type == 'publish':
            # query posts which account published
            posts = Post.objects.filter(poster_email=email).order_by('-id')
            return generate_posts_response(posts)
        elif query_type == 'like':
            # query posts which account liked
            liked_posts = LikedPost.objects.filter(liked_account_email=email)
            post_ids = [post.post_id for post in liked_posts]
            posts = Post.objects.filter(id__in=post_ids).order_by('-id')
            return generate_posts_response(posts)

        # query posts for explore
        if query_type == 'All':
            posts = Post.objects.all().order_by('-id')
        else:
            posts = Post.objects.filter(channel=query_type).order_by('-id')
        return generate_posts_response(posts)
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def publish(request):
    try:
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['access_token', 'title', 'content', 'channel'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        # query account
        access_token = req.get('access_token')
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account = Account.objects.get(email=account_access_token.account_email)

        title = req.get('title')
        content = req.get('content')
        channel = req.get('channel')
        # generate a new post
        post = Post(poster_id=account.id, poster_name=account.name, poster_email=account.email, title=title,
                    content=content, channel=channel)
        post.save()

        return generate_successful_response(None)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def query_comments(request):
    try:
        req = json.loads(request.body)
        post_id = req.get('id')
        if post_id is None:
            return generate_failed_response('Invalid ID!')

        comments = Comment.objects.filter(post_id=post_id)

        return generate_comments_response(comments)
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def query_like_status(request):
    try:
        # validate reuqest body
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['access_token', 'id'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        # query account
        access_token = req.get('access_token')
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)

        # check has liked post or not
        post_id = req.get('id')
        liked = LikedPost.objects.filter(post_id=post_id,
                                         liked_account_email=account_access_token.account_email).count() > 0

        return generate_successful_response(liked)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def like(request):
    try:
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['access_token', 'id'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        # query account
        access_token = req.get('access_token')
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)

        # firstly validate like status
        post_id = req.get('id')
        liked = LikedPost.objects.filter(post_id=post_id,
                                         liked_account_email=account_access_token.account_email).count() > 0

        if not liked:
            # record new like item
            post = Post.objects.get(id=post_id)
            account = Account.objects.get(email=account_access_token.account_email)
            like_post = LikedPost(liked_account_email=account.email, liked_account_name=account.name, post_id=post_id,
                                  poster_email=post.poster_email)
            post.likes += 1
            like_post.save()
            post.save()
            liked = True
        else:
            # remove like item
            LikedPost.objects.filter(post_id=post_id, liked_account_email=account_access_token.account_email).delete()
            post = Post.objects.get(id=post_id)
            post.likes -= 1
            post.save()
            liked = False

        return generate_successful_response(liked)
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))


def comment(request):
    try:
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['access_token', 'id', 'comment'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        # query account
        access_token = req.get('access_token')
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account = Account.objects.get(email=account_access_token.account_email)

        # query post
        post_id = req.get('id')
        post = Post.objects.get(id=post_id)

        # generate new comment
        comment_text = req.get('comment')
        new_comment = Comment(post_id=post.id, poster_email=post.poster_email, commentator_email=account.email,
                              commentator_id=account.id, commentator_name=account.name, comment=comment_text)

        new_comment.save()

        return generate_comments_response([new_comment])
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))

def delete(request):
    try:
        req = json.loads(request.body)
        missing_fields = validate_request_data(req, ['access_token', 'id'])
        if missing_fields:
            return generate_missing_fields_response(missing_fields)

        # validate account access token
        access_token = req.get('access_token')
        account_access_token = AccountAccessToken.objects.get(access_token=access_token)
        account_email = account_access_token.account_email

        # query post
        post_id = req.get('id')
        post = Post.objects.get(id=post_id, poster_email=account_email)

        # query post like records
        likes = LikedPost.objects.filter(post_id=post_id, poster_email=account_email)

        # query post comments
        comments = Comment.objects.filter(post_id=post_id, poster_email=account_email)

        comments.delete()
        likes.delete()
        post.delete()
        return generate_successful_response(True)
    except Post.DoesNotExist:
        return generate_failed_response('Invalid ID!')
    except AccountAccessToken.DoesNotExist:
        return generate_failed_response('Invalid access token!')
    except json.JSONDecodeError:
        return generate_failed_response('Invalid JSON!')
    except Exception as e:
        return generate_failed_response('An unexpected error occurred.', data=str(e))