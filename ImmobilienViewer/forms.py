from django import forms

from core.models import Region, Immobilie, Tag


class AddRegionForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddImmobilieForm(forms.ModelForm):

    class Meta:
        model = Immobilie
        fields = ('title', 'description', 'price', 'url', 'location', 'region')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
        }

class AddTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
