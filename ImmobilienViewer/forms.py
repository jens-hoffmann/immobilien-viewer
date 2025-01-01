from django import forms

from core.models import Region, Immobilie, Tag, FileAttachment


class AddRegionForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = ('name',)

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

