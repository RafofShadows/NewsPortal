import time

from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import Post, PostCategory


#@receiver(m2m_changed, sender=Post.categories.through)
def post_notify(sender, instance, action, **kwargs):
    if action == "post_add":
        transaction.on_commit(lambda: send_subscription(instance))


m2m_changed.connect(post_notify, sender=Post.categories.through)


def send_subscription(post):
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
                from_email='pickers97@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
