from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Article, Comments
from .filters import ArticleFilter, ArticleCommentsFilter
from .forms import ArticleForm, CommentForm


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


class ArticleDetail(FormMixin, DetailView):
    model = Article
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article')

class CommentsList(ListView):
    model = Comments
    # ordering = '-id'
    template_name = 'comments_page.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comments.objects.filter(author=self.request.user).all()
        return queryset

class UserPostCommentList(generic.ListView):
    model = Comments
    template_name = 'user_posts_comments.html'
    context_object_name = 'user_posts_comments'

    def get_queryset(self):
        queryset = Comments.objects.filter(article__author=self.request.user).all()
        return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = ArticleCommentsFilter(self.request.GET, queryset)
    #     return self.filterset.qs

    def get_queryset(self):
        queryset = Comments.objects.filter(article__author=self.request.user).order_by('-time_in').all()
        self.filterset = ArticleCommentsFilter(self.request.GET, queryset)
        self.filterset.form.fields['article'].queryset = Article.objects.filter(author=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

@login_required
def comments_accept(request, **kwargs):
    response = Comments.objects.get(id=kwargs.get('pk'))
    response.status = True
    response.save()
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('article/')

@login_required
def comments_delete(request, **kwargs):
    response = Comments.objects.get(id=kwargs.get('pk'))
    response.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('article/')
