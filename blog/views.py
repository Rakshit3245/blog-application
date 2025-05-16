from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Comment, PostImage
from django.views.generic import (
                ListView,
                DetailView,
                CreateView,
                UpdateView,
                DeleteView
)
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostImageForm
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.views.generic import TemplateView

class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')  # Assuming created_at is the timestamp
        context['images'] = PostImage.objects.filter(post=self.object)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog-list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        image = self.request.FILES.getlist('post_images')
        for image_file in image:
            PostImage.objects.create(post=post, post_images=image_file)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return True

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return True

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('pk'))
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('blog-list')

def post_images(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    images = PostImage.objects.filter(post=post)
    return render(request, 'blog/post_images.html', {'post': post, 'images': images})

class PostImageView(LoginRequiredMixin, View):
    model = PostImage
    template_name = 'blog/post_image.html'
    success_url = reverse_lazy('blog-list')

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('pk'))
        image_form = PostImageForm(request.POST, request.FILES, instance=post)
        if image_form.is_valid():
            image_form.save()
            return redirect('blog-list')
        else:
            return render(request, 'blog/post_image.html', {'post': post,'image_form': image_form})

@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_content = request.POST.get('comments')
        if comment_content:
            # Create the comment
            comment = Comment.objects.create(post=post, user=request.user, comments=comment_content)
            messages.success(request, 'Comment successfully posted')
    return redirect('post-detail', pk=post.id)


@login_required
def comment_replay(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post_id = request.POST.get('post_id')
    if not post_id:
        messages.error(request, "Post not found.")
        return redirect('blog-list')

    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        reply_content = request.POST.get('replay')
        new_reply = Comment(
            post=parent_comment.post,
            user=request.user,
            comments=reply_content,
            parent_comment=parent_comment
        )
        new_reply.save()
        messages.success(request, 'Replied successfully!')
        return redirect('post-detail', pk=parent_comment.post.id)
    return redirect('post-detail', pk=post.id)


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(PostImage, id=image_id)
    post_id = image.post.id
    image.delete()
    return redirect('post-detail', pk=post_id)

def search_blog(request):
    query = request.GET.get('search', '')
    if not query.strip():
        messages.warning(request, 'Please enter a Valid Input')
        return redirect('blog-list')
    if query:
        posts = Post.objects.filter(
            title__icontains=query) | Post.objects.filter(
            content__icontains=query)
        return render(request, 'blog/blog_search.html', {'posts': posts, 'q': query})
    else:
        return render(request, 'blog/home.html')

class PostImageCreateView(LoginRequiredMixin, CreateView):
    model = PostImage
    form_class = PostImageForm
    template_name = 'blog/add_images.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

class AboutView(TemplateView):
    template_name = 'blog/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About'
        return context
