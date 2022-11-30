from datetime import date, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Category, Post


@shared_task
def weekly_mail():
    start_date = date.today() - timedelta(days=7)

    for category in Category.objects.all():
        posts = Post.objects.filter(categories=category, timestamp__gt=start_date).order_by('-timestamp')
        for user in category.subscribers.all():
            if user.email:
                html_content = render_to_string(
                    'weekly_news.html',
                    {
                        'posts': posts,
                        'username': user.username
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f"Новости за прошлую неделю. Категория {category.name}",
                    from_email='newsportaltest@yandex.ru',
                    to=[user.email]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()


@shared_task
def send_subscription(post_id):
    post = Post.objects.get(pk=post_id)
    for category in post.categories.all():
        for user in category.subscribers.all():
            html_content = render_to_string(
                'subscription.html',
                {
                    'post': post,
                    'username': user.username
                }
            )
            msg = EmailMultiAlternatives(
                subject=post.header,
                from_email='newsportaltest@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()