from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import BlogPost
from blog.forms import BlogPostForm
from mailing_creation.models import Newsletter, NewsletterMessage
import random
from django.db.models import Count


class MainPageView(TemplateView):
    template_name = 'blog/main_page.html'

    def get_context_data(self, **kwargs):
        context = {}
        posts = BlogPost.objects.all()
        if posts:
            random_numbers = random.sample(range(len(posts)), min(3, len(posts)))
            random_posts = [posts[i] for i in random_numbers]
            context['posts'] = random_posts
        context['newsletter_count'] = Newsletter.objects.count()
        context['newsletter_active'] = Newsletter.objects.filter(status__in=['created', 'running']).count()
        recipients_count = []
        for i in Newsletter.objects.all():
            recipients_count.extend(i.recipients)
        context['unique_recipients'] = len(set(recipients_count))
        return context


class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_date')


class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    queryset = BlogPost.objects.filter(is_published=True)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.add_view()
        return self.object


class PostEditView(View):
    template_name = 'blog/edit_form.html'

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        form = BlogPostForm(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', slug=post.slug)


class PostCreateView(CreateView):
    template_name = 'blog/create_form.html'

    def get(self, request):
        form = BlogPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', slug=post.slug)


class PostDeleteView(View):

    def get(self, request, slug):
        posts = BlogPost.objects.filter(is_published=True).order_by('-created_date')
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        post.delete()
        return render(request, 'blog/post_list.html', {'posts': posts})
