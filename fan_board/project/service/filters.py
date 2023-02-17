from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Article
from django.contrib.auth.models import User
from django.forms import DateInput

class ArticleFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label=('Автор'),
        empty_label='all'
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Объявление содержит',
    )

    text = CharFilter(
        lookup_expr='icontains',
        label='В содержании объявления',
    )

    time_in = DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано с',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Article
        fields = {
            'category': ['exact']
        }