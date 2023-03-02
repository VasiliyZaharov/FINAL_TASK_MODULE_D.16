from django import forms
from django.core.exceptions import ValidationError

from .models import Article, Comments


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category',
                  'title',
                  'text',
                  ]
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'text': 'Содержание',
        }

    def clean(self):
        cleaned_data = super().clean()
        title, content = cleaned_data.get('title', ''), cleaned_data.get('text', '')
        if title is not None and title.lower() in content.lower():
            err_text = 'Избегайте повтора текста объявления в содержании.'
            raise ValidationError({'title': err_text})
        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and title[0].islower():
            raise ValidationError('Начните объявление с заглавной буквы.')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
