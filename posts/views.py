from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
from .models import Post



class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs): #this means keyword arguments, the double asterisk is python's take on pointers and is pretty standard. kwargs are key-value pairs
        context = super().get_context_data(**kwargs) #the super function is calling the original get_context_data method that lives in ListView
        context["post_list"] = Post.objects.filter(
            active=True
            ).order_by("created_on").reverse() #default behavior is ascending order, so using reverse() will go in descending
        context["current_datetime"] = datetime.now().strftime("%F %H:%M:%S") #the capital F represents the date
        return context

class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = Post.objects.filter(
            active=False
        ).filter(
            author=self.request.user
            ).order_by('created_on').reverse()
        context["current_datetime"] = datetime.now().strftime("%F %H:%M:%S")
        return context

class PostDetailView(DetailView): #the way to read this is PostDetailView is extending the DetailView class
    template_name = "posts/detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["post"].active == True:
            return context
        else:
            self.template_name = "Errors/404.html"
            return context

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user #this line of code is populating the author line with the user that is currently logged in.
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ['title', 'subtitle', 'body', 'active']

    #this test_func will define whether or not you have access to the specific view you're on, it returns true or false
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user