from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Category, Post


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

