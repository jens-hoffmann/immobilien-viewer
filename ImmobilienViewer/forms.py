from django import forms

from core.models import Region, Immobilie, Tag, FileAttachment, District


class AddRegionForm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = ['uuid', 'tags']

    name = forms.CharField(widget=forms.TextInput())
    districts = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'id': 'district-selection'}),
        queryset=District.objects.all()
        )


class ImmobilieForm(forms.ModelForm):

    class Meta:
        model = Immobilie
        fields = ('title', 'description', 'provider','provider_id', 'price', 'url', 'location')


class AddTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)


class AttachmentForm(forms.ModelForm):

    class Meta:
        model = FileAttachment
        fields = ('name', 'attachment')

