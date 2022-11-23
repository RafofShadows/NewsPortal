from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, News, Article, Category
from .filters import PostFilter
# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-timestamp'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)




class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = News
        post.rating = 0

        super().form_valid(form)

        #send_subscription(post)

        return redirect('/portal/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Article
        post.rating = 0

        super().form_valid(form)

        #send_subscription(post)

        return redirect('/portal/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


@login_required
def add_subscriber(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    category.subscribers.add(user)
    category.save()
    return redirect(category.get_absolute_url())


def send_subscription(post):
    html_content = render_to_string(
        'subscription.html',
        {
            'post': post,
        }
    )
    for category in post.categories.all():
        for user in category.subscribers.all():
            msg = EmailMultiAlternatives(
                subject=post.header,
                body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
                from_email='pickers97@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
