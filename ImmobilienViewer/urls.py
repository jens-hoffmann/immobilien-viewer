from django.urls import path, include
from django.views.generic import TemplateView

from .views import ImmobilienDetailView, ImmobilienListView, RegionListView

app_name = 'immoviewer'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="homepage"),
    path('<int:pk>/', ImmobilienDetailView.as_view(), name="immo-detail"),
    path('list/', ImmobilienListView.as_view(), name='immo-list'),
    path('list-by-region/<int:pk>/', RegionListView.as_view(), name='immo-list-by-region')

]