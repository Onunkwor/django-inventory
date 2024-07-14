from django import forms


class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title.lower().strip() == 'cake':
            self.add_error('title', "this title is taken")
        if "cake" in content or "cake" in title:
            self.add_error('content', "this content is taken")
            raise forms.ValidationError("Cake is not allowed")
        return cleaned_data
