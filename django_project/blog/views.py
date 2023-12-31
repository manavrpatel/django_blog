from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import post


def home(request):
    context={
        'posts': post.objects.all()
    }
    return render(request,'blog/home.html', context)

class PostListView(ListView):
    model=post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model=post

class PostCreateView(LoginRequiredMixin, CreateView):
    model=post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model=post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user==post.author:
            return True
        else: 
            return False
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin , DeleteView):
    model=post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user==post.author:
            return True
        else: 
            return False
             

def about(request):
    return render(request,'blog/about.html', {'title':'About'})  