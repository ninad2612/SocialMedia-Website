from django.shortcuts import render , redirect , get_object_or_404

from django.contrib.auth.decorators import login_required
from accounts.models import * 
from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Post, Like, Comment
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Follow  # Import your Follow model

# @require_POST
# def follow_user(request, user_id):
#     if request.user.is_authenticated:
#         action = request.POST.get('action')

#         if action == 'follow':
#             Follow.objects.get_or_create(user=request.user, following_id=user_id)  # Create follow object
#             return JsonResponse({'success': True})
#         elif action == 'unfollow':
#             Follow.objects.filter(user=request.user, following_id=user_id).delete()  # Remove follow object
#             return JsonResponse({'success': True})

#     return JsonResponse({'success': False}, status=400)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Check if the follow relationship already exists
    follow, created = Follow.objects.get_or_create(user=request.user, following=user_to_follow)
    
    if created:
        # Successfully followed the user
        return redirect('/view_user/', user_id=user_id)
    else:
        # User already followed, unfollow them
        follow.delete()  # This will unfollow the user
        return redirect('view_user', user_id=user_id)


@login_required
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Fetch user by ID
    user_posts = Post.objects.filter(user=user)  # Get all posts by this user
    profile = get_object_or_404(Profile, user=user)
    is_following = Follow.objects.filter(user=request.user, following=user).exists()  # Check if current user follows this user

    context = {
        'user': user,
        'user_posts': user_posts,
        'profile': profile,
        'is_following': is_following,  # Pass follow status to the template
    }
    return render(request, 'view_user.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q')  # Get the query from the GET request
    results = User.objects.none()  # Initialize an empty queryset

    if query:  # If a query is provided
        results = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).select_related('profile')  # Use select_related to fetch related Profile objects

    return render(request, 'search_users.html', {'results': results})

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.get_or_create(post=post, user=request.user)  # Create a like if it doesn't exist
    messages.success(request, "You liked the post!")
    return redirect('view_posts')

@login_required
def comment_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        comment = request.POST.get('comment')
        Comment.objects.create(post=post, user=request.user, content=comment)  # Create a new comment
        messages.success(request, "Your comment has been added!")
    return redirect('view_posts')

@login_required
def view_posts(request):
    user_posts = Post.objects.filter(user=request.user)  # Fetch posts created by the logged-in user
    return render(request, 'view_posts.html', {'user_posts': user_posts})

@login_required  # Ensure the user is logged in to access this view
def upload_post(request):
    if request.method == 'POST':
        # Retrieve the uploaded files and other data
        content_image = request.FILES.get('content_image')
        content_video = request.FILES.get('content_video')
        caption = request.POST.get('caption')

        # Create a new post instance
        post = Post(user=request.user)  # Set the logged-in user as the post author

        # Assign content if uploaded
        if content_image:
            post.content_image = content_image
        if content_video:
            post.content_video = content_video
            
        post.caption = caption  # Set the caption for the post

        # Save the post to the database
        post.save()  # This also saves the created_at timestamp automatically

        return redirect('/your-posts/')  # Redirect to the view where posts are displayed

    return render(request, 'upload_post.html')

@login_required
def home_page(request):
    # Fetch the user's profile using the user's ID

    # Fetch posts from users that the logged-in user follows
    following_users = Follow.objects.filter(user=request.user).values_list('following', flat=True)
    user_posts = Post.objects.filter(user__id__in=following_users).order_by('-created_at')  # Sort by creation date

    try:
        profile = Profile.objects.get(user=request.user)  # Fetch the profile using the user ID
    except Profile.DoesNotExist:
        profile = None  # If no profile exists, handle it as needed

    return render(request, 'home.html', {
        'username': request.user.username,
        'profile': profile,
        'user_posts': user_posts,  # Handle case where profile is None
    })


