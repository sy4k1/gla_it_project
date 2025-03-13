from django.http import JsonResponse


def generate_successful_response(data):
    return JsonResponse({
        'code': 1,
        'data': data,
    }, status=200)


def generate_failed_response(message: str, code=0, data=None):
    return JsonResponse({
        'code': code,
        'message': message,
        'data': data,
    }, status=200)


def generate_missing_fields_response(missing_fields):
    return generate_failed_response(f"Missing fields: {', '.join(missing_fields)}!")


def generate_account_response(account, followers=0, following=0, likes=0, access_token=None):
    return generate_successful_response({
        'id': account.id,
        'email': account.email,
        'name': account.name,
        'role': account.role,
        'bio': account.bio,
        'avatar': account.avatar,
        'wallpaper': account.wallpaper,
        'create_datetime': account.create_datetime,
        'access_token': access_token,
        'following': following,
        'followers': followers,
        'likes': likes,
    })


def generate_posts_response(posts):
    return generate_successful_response([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'images': post.images,
        'poster_email': post.poster_email,
        'poster_id': post.poster_id,
        'poster_name': post.poster_name,
        'likes': post.likes,
        'views': post.views,
        'channel': post.channel,
        'create_datetime': post.create_datetime,
    } for post in posts])


def generate_comments_response(comments):
    return generate_successful_response(format_comments(comments))


def format_comments(comments):
    return [{
        'id': comment.id,
        'post': comment.post.id,
        'post_title': comment.post.title,
        'poster_email': comment.poster_email,
        'commentator_email': comment.commentator_email,
        'commentator_id': comment.commentator_id,
        'commentator_name': comment.commentator_name,
        'comment': comment.comment,
        'read': comment.read,
        'create_datetime': comment.create_datetime,
    } for comment in comments]


def format_likes(likes):
    return [{
        'id': like.id,
        'liked_account_email': like.liked_account_email,
        'liked_account_name': like.liked_account_name,
        'post_id': like.post_id,
        'poster_email': like.poster_email,
        'read': like.read,
        'create_datetime': like.create_datetime,
    } for like in likes]


def format_followers(followers):
    return [{
        'id': follower.id,
        'follower_email': follower.follower_email,
        'follower_name': follower.follower_name,
        'follower_id': follower.follower_id,
        'followed_email': follower.followed_email,
        'read': follower.read,
        'create_datetime': follower.create_datetime,
    } for follower in followers]
