from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from .models import Post 

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'all_post_list'
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields =('flight_number','travel_date','origin','destination','message')
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.traveler = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post 
    template_name = 'post_edit.html'
    fields = ['flight_number','origin','destination','travel_date', 'message']
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if (obj.traveler != self.request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if (obj.traveler != self.request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
