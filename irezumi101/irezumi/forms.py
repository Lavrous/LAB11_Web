from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.deconstruct import deconstructible
from .models import Motif, Category, Comment

@deconstructible
class NoNumbersValidator:
    def __init__(self, message=None):
        self.message = message if message else "В названии мотива не должно быть цифр!"

    def __call__(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError(self.message)


class AddMotifForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        label="Название мотива",
        validators=[NoNumbersValidator(), MinLengthValidator(2, message="Минимум 2 символа")],
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Motif
        fields = ['title', 'slug', 'content', 'image', 'is_published', 'cat', 'tags']

        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'cols': 60, 'rows': 10}),
            'cat': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина названия превышает 50 символов')
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Оставьте свой комментарий...'
            }),
        }
        labels = {'content': ''}