from django import forms

class Imagem(forms.Form):
    imagem = forms.ImageField()