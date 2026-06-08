from django import forms
from django.core.validators import MinValueValidator
from .models import Category

class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Название'
    )
    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Цена'
    )
    image = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label='URL изображения'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Категория',
        empty_label=None
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Описание'
    )
    stock = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Остаток'
    )

class SearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию'
        }),
        label=''
    )
    