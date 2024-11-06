from django.db.models.query import EmptyQuerySet
from django.views.generic import DetailView, ListView

from core.models import Immobilie, Region


class ImmobilienDetailView(DetailView):

    model = Immobilie
    template_name = 'immo_detail.html'
    context_object_name = 'immobilie'

    def get_queryset(self, *args, **kwargs):
        return Immobilie.objects.filter(pk=self.kwargs.get('pk'))

class ImmobilienListView(ListView):

    model = Immobilie
    template_name = "immo_list.html"
    context_object_name = 'immobilien'
    paginate_by = 1
    queryset = Immobilie.objects.all()

class RegionListView(ListView):

    model = Immobilie
    template_name = "immo_list.html"
    context_object_name = 'immobilien'
    paginate_by = 1

    def get_queryset(self, *args, **kwargs):
        region_result = Region.objects.filter(pk=self.kwargs.get('pk'))
        if len(region_result) > 0:
            return Immobilie.objects.filter(region=region_result[0])
        else:
            return EmptyQuerySet()
