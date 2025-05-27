
import pytest
from rest_framework.test import APIClient
from user.models import User
from ..models import Post, Like, Comment
from django.urls import reverse
from rest_framework import status





@pytest.mark.django_db
def test_post_model():

    user = User.objects.create_user(username="mahdi", phone_number="989121234567", password="12345678")
    post = Post.objects.create(user=user, title="Post 1", caption="Test 1", is_public=True, is_active=True )

    assert post.title == 'Post 1'
    assert post.caption == 'Test 1'
    assert post.user == user
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_comment_create():
    client = APIClient()
    user = User.objects.create_user(username="mahdi", phone_number="989121234567", password="12345678")
    client.force_authenticate(user)
    post = Post.objects.create(user=user, title="Post 1", caption="Test 1", is_public=True, is_active=True )
    user2 = User.objects.create_user(username="mahdi", phone_number="989121234567", password="12345678")
    client2 = APIClient()
    client2.force_authenticate(user2)

    data = {
        'title':'test_comment',
        'caption':'test_caption_comment'
    }
    url = reverse('comments',args=[post.id])
    response = client2.post(url,data)
    assert response.status_code == 201
    assert response.data['detail'] == 'Your comment was submitted!'


@pytest.mark.django_db
def test_like():
    client = APIClient()
    user = User.objects.create_user(username="mahdi", phone_number="989121234567", password="12345678")
    client.force_authenticate(user)
    post = Post.objects.create(user=user, title="Post 1", caption="Test 1", is_public=True, is_active=True )
    user2 = User.objects.create_user(username="mahdi2", phone_number="989121234569", password="12345678")
    client2 = APIClient()
    client2.force_authenticate(user2)

    data = {
        'is_liked': True
    }
    url = reverse('likes',args=[post.id])
    response = client2.post(url,data)
    assert response.status_code == 200
    assert response.data['detail'] == 'is liked'

@pytest.mark.django_db
def test_get_like():
    client = APIClient()
    user = User.objects.create_user(username="mahdi", phone_number="989121234567", password="12345678")
    client.force_authenticate(user)
    post = Post.objects.create(user=user, title="Post 1", caption="Test 1", is_public=True, is_active=True )
    user2 = User.objects.create_user(username="mahdi2", phone_number="989121234569", password="12345678")
    Like.objects.create(user=user2, post=post, is_liked=True)
    user3 = User.objects.create_user(username="mahdi3", phone_number="989121234566", password="12345678")
    Like.objects.create(user=user3, post=post, is_liked=True)

    url = reverse('likes',args=[post.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['likes'] == 2


@pytest.mark.django_db
def test_get_comment():
    client = APIClient()
    user = User.objects.create_user(username="mahdi", phone_number="989121234567", password="12345678")
    client.force_authenticate(user)
    post = Post.objects.create(user=user, title="Post 1", caption="Test 1", is_public=True, is_active=True)
    user2 = User.objects.create_user(username="mahdi2", phone_number="989121234569", password="12345678")
    Comment.objects.create(user=user2, post=post, caption='testt', is_approved=True)
    user3 = User.objects.create_user(username="mahdi3", phone_number="989121234566", password="12345678")
    Comment.objects.create(user=user3, post=post, caption='testewe', is_approved=True)

    url = reverse('comments', args=[post.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
