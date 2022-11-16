from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, NewsCreate, ArticlesCreate

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    # path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostList.as_view(), name='post_search'),
    # path('create/', PostCreate.as_view(), name='post_create'),
    # path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    # path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('articles/<int:pk>', PostDetail.as_view(), name='articles_detail'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]
