from django import forms
from django.forms.utils import ErrorList
from .models import Post, Category, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "status", "category")
    publish = forms.CharField(required=True)

    def add_error_msg(self, field, msg):
        errors = self._errors.setdefault(field, ErrorList())
        errors.append(msg)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("title",)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
