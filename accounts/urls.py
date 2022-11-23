from django.urls import path

from accounts.views import upgrade_me

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
]
