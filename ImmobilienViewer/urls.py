from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import ImmobilienDetailView, ImmobilienListView, RegionListView, CreateRegionView, CreateImmobilieView, \
    CreateTagView, ImmobilienAPIView, UpdateImmobilieView, UploadAttachmentView

router = DefaultRouter()
router.register('immobilie', ImmobilienAPIView)

app_name = 'immoviewer'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html", extra_context = {'active': 'home'}), name="homepage"),
    path('<uuid:uuid>/', ImmobilienDetailView.as_view(), name="immo-detail"),
    path('list/', ImmobilienListView.as_view(), name='immo-list'),
    path('createregion/', CreateRegionView.as_view(), name='immo-create-region'),
    path('createimmobilie/', CreateImmobilieView.as_view(), name='immo-create-immobilie'),
    path('updateimmobilie/<uuid:uuid>/', UpdateImmobilieView.as_view(), name='immo-update-immobilie'),
    path('updateimmobilie/<uuid:uuid>/uploadattachment', UploadAttachmentView.as_view(), name='immo-upload-attachment'),
    path('createtag/', CreateTagView.as_view(), name='immo-create-tag'),
    path('list-by-region/<uuid:uuid>/', RegionListView.as_view(), name='immo-list-by-region'),
    path('map/', TemplateView.as_view(template_name="map.html"), name='immo-map'),
    path('api/', include(router.urls))
]