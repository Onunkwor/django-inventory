from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f'{title} already exists')
        return data


# class ArticleFormOld(forms.Form):
#     title = forms.CharField()
#     content = forms.CharField()

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         title = cleaned_data.get('title')
#         content = cleaned_data.get('content')
#         if title.lower().strip() == 'cake':
#             self.add_error('title', "this title is taken")
#         if "cake" in content or "cake" in title:
#             self.add_error('content', "this content is taken")
#             raise forms.ValidationError("Cake is not allowed")
#         return cleaned_data
