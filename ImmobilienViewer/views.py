from django.db.models.query import EmptyQuerySet
from django.views.generic import DetailView, ListView, CreateView
from rest_framework import viewsets, status
from rest_framework.response import Response

from ImmobilienViewer import serializers
from ImmobilienViewer.exceptions import ImmoblilieExistsException
from ImmobilienViewer.forms import AddRegionForm, AddImmobilieForm, AddTagForm
from ImmobilienViewer.serializers import ImmobilienResourceSerializer
from core.models import Immobilie, Region, Tag, ImmobilienResource


class ImmobilienDetailView(DetailView):

    model = Immobilie
    template_name = 'immo_detail.html'
    context_object_name = 'immobilie'

    def get_object(self, *args, **kwargs):
        return Immobilie.objects.filter(uuid=self.kwargs.get('uuid'))[0]

class ImmobilienListView(ListView):

    model = Immobilie
    template_name = "immo_list.html"
    context_object_name = 'immobilien'
    paginate_by = 9
    queryset = Immobilie.objects.all()
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
    template_name = 'create.html'
    success_url = '/immoviewer/list/'
    extra_context = {'title': 'Create a new region', 'active': 'create'}


class CreateImmobilieView(CreateView):

    model = Immobilie
    form_class = AddImmobilieForm
    template_name = 'create.html'
    success_url = '/immoviewer/list/'
    extra_context = {'title': 'Create a new Immobilie', 'active': 'create'}

class CreateTagView(CreateView):

    model = Tag
    form_class = AddTagForm
    template_name = 'create.html'
    success_url = '/immoviewer/list/'
    extra_context = {'title': 'Create a new tag', 'active': 'create'}

class ImmobilienAPIView(viewsets.ModelViewSet):

    serializer_class = serializers.ImmobilienSerializer
    queryset = Immobilie.objects.all()

