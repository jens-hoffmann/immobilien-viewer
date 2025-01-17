from django import forms

from core.models import Region, Immobilie, FileAttachment, District


class AddRegionForm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = ['uuid']

    name = forms.CharField(widget=forms.TextInput())
    districts = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'id': 'district-selection'}),
        queryset=District.objects.all()
        )


class ImmobilieForm(forms.ModelForm):

    class Meta:
        model = Immobilie
        fields = ('title', 'description', 'provider','provider_id', 'price', 'url', 'location')


class AttachmentForm(forms.ModelForm):

    class Meta:
        model = FileAttachment
        fields = ('name', 'attachment')

