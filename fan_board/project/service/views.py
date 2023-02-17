from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article
from .filters import ArticleFilter
from .forms import ArticleForm

class ArticleList(ListView):
    model = Article
    ordering = '-id'
    template_name = 'article.html'
    context_object_name = 'article'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'post.html'
    context_object_name = 'post'


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'

class ArticleDelete(DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article')
