from django.urls import path, include
from django.views.generic import TemplateView

from .views import ImmobilienDetailView, ImmobilienListView, RegionListView, CreateRegionView, CreateImmobilieView, \
    CreateTagView

app_name = 'immoviewer'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html", extra_context = {'active': 'home'}), name="homepage"),
    path('<uuid:uuid>/', ImmobilienDetailView.as_view(), name="immo-detail"),
    path('list/', ImmobilienListView.as_view(), name='immo-list'),
    path('createregion/', CreateRegionView.as_view(), name='immo-create-region'),
    path('createimmobilie/', CreateImmobilieView.as_view(), name='immo-create-immobilie'),
    path('createtag/', CreateTagView.as_view(), name='immo-create-tag'),
    path('list-by-region/<uuid:uuid>/', RegionListView.as_view(), name='immo-list-by-region')

]