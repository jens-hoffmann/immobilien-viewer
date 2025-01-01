from django.db.models.query import EmptyQuerySet
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets

from django.contrib import messages
from ImmobilienViewer import serializers
from ImmobilienViewer.forms import AddRegionForm, ImmobilieForm, AddTagForm, AttachmentForm
from core.models import Immobilie, Region, Tag, FileAttachment


class ImmobilienDetailView(DetailView):

    model = Immobilie
    template_name = 'immo_detail.html'
    context_object_name = 'immobilie'

    def get_object(self, *args, **kwargs):
        immo = Immobilie.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        return immo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        immo = Immobilie.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        context['attachments'] = immo.attachments.all()
        return context

class ImmobilienListView(ListView):

    model = Immobilie
    template_name = "immo_list.html"
    context_object_name = 'immobilien'
    paginate_by = 9
    queryset = Immobilie.objects.order_by('-location')
    extra_context = {'active': 'list'}

class RegionListView(ListView):

    model = Immobilie
    template_name = "immo_list.html"
    context_object_name = 'immobilien'
    paginate_by = 1
    extra_context = {'active': 'list-by-region'}

    def get_queryset(self, *args, **kwargs):
        region_result = Region.objects.filter(uuid=self.kwargs.get('uuid'))
        if len(region_result) > 0:
            return Immobilie.objects.filter(region=region_result[0])
        else:
            return EmptyQuerySet()

class CreateRegionView(CreateView):

    model = Region
    form_class = AddRegionForm
    template_name = 'immobilie_form.html'
    extra_context = {'title': 'Create a new region', 'active': 'create'}

    def get_success_url(self):
        return reverse('immoviewer:immo-list')

class CreateImmobilieView(CreateView):

    model = Immobilie
    form_class = ImmobilieForm
    template_name = 'immobilie_form.html'
    extra_context = {'title': 'Create a new Immobilie', 'active': 'create'}

    def get_success_url(self):
        return reverse('immoviewer:immo-list')

class UpdateImmobilieView(UpdateView):

    model = Immobilie
    form_class = ImmobilieForm
    template_name = 'immobilie_form.html'
    extra_context = {'title': 'Update existing Immobilie', 'active': 'edit'}

    def get_success_url(self):
        url = reverse('immoviewer:immo-detail', kwargs={'uuid': self.kwargs['uuid']})
        return url

    def get_object(self, *args, **kwargs):
        return Immobilie.objects.filter(uuid=self.kwargs.get('uuid'))[0]

    def form_valid(self, form):
        messages.success(self.request, "The immobilie was updated successfully.")
        return super(UpdateImmobilieView,self).form_valid(form)

class CreateTagView(CreateView):

    model = Tag
    form_class = AddTagForm
    template_name = 'immobilie_form.html'
    success_url = '/immoviewer/list/'
    extra_context = {'title': 'Create a new tag', 'active': 'create'}

class ImmobilienAPIView(viewsets.ModelViewSet):

    serializer_class = serializers.ImmobilienSerializer
    queryset = Immobilie.objects.all()


class UploadAttachmentView(CreateView):

    model = FileAttachment
    form_class = AttachmentForm
    template_name = 'upload_form.html'

    def get_success_url(self):
        url = reverse('immoviewer:immo-list-attachments', kwargs={'uuid': self.kwargs['uuid']})
        return url

    def form_valid(self, form):
        immobilie = Immobilie.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        form.instance.immobilie = immobilie
        return super().form_valid(form)

class AttachmentListView(ListView):

    model = FileAttachment
    template_name = 'attachment_list.html'
    context_object_name = 'attachments'

    def get_queryset(self):
        attachments =  FileAttachment.objects.filter(immobilie__uuid=self.kwargs.get('uuid'))
        return attachments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        immobilie =  Immobilie.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        context['immobilie'] = immobilie
        return context

class DeleteAttachmentView(DeleteView):

    model = FileAttachment
    template_name = 'attachment_confirm_delete.html'
    context_object_name = 'attachment'

    def get_queryset(self):
        attachments = FileAttachment.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        return attachments

    def form_valid(self, form):
        messages.success(self.request, "The attachment was deleted successfully.")
        return super(DeleteAttachmentView,self).form_valid(form)

    def get_object(self, *args, **kwargs):
        attachments = FileAttachment.objects.filter(uuid=self.kwargs.get('uuid'))
        return attachments

    def get_success_url(self):
        attachment = FileAttachment.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        url = reverse('immoviewer:immo-list-attachments', kwargs={'uuid': attachment.immobilie.uuid})
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attachment = FileAttachment.objects.filter(uuid=self.kwargs.get('uuid'))[0]
        context['immobilie'] = attachment.immobilie
        return context
