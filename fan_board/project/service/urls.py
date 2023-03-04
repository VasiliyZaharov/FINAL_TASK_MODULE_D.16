from django.urls import path

from .views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, CommentsList, \
    UserPostCommentList, comments_accept, comments_delete

urlpatterns = [
    path('', ArticleList.as_view(), name='article'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('comments_page/', CommentsList.as_view(), name='comments'),
    path('user_posts_comments/', UserPostCommentList.as_view(), name='user_posts_comments'),
    path('user_posts_comments/accept/<int:pk>', comments_accept, name='comments_accept'),
    path('user_posts_comments/delete/<int:pk>', comments_delete, name='comments_delete'),
]
