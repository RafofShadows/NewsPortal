from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import Post


@receiver(post_save, sender=Post)
def post_notify(sender, instance, created, **kwargs):
    if created:
        send_subscription(instance)


def send_subscription(post):
    html_content = render_to_string(
        'subscription.html',
        {
            'post': post,
        }
    )
    for category in post.categories.all():
        for user in category.subscribers.all():
            # mail_list = list([u.email for u in category.subscribers.all()])
            msg = EmailMultiAlternatives(
                subject=post.header,
                body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
                from_email='pickers97@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
