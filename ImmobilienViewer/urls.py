from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('immobilie', ImmobilienAPIView)

app_name = 'immoviewer'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html", extra_context = {'active': 'home'}), name="homepage"),
    path('immobilie/detail/<uuid:uuid>/', ImmobilienDetailView.as_view(), name="immo-detail"),
    path('immobilie/list/', ImmobilienListView.as_view(), name='immo-list'),
    path('immobilie/list/<slug:tag_slug>/', TaggedImmobilienListView.as_view(), name='immo-tagged-list'),
    path('region/create/', CreateRegionView.as_view(), name='immo-create-region'),
    path('immobilie/create', CreateImmobilieView.as_view(), name='immo-create-immobilie'),
    path('immobilie/update/<uuid:uuid>/', UpdateImmobilieView.as_view(), name='immo-update-immobilie'),
    path('immobilie/attachments/list/<uuid:uuid>/', AttachmentListView.as_view(), name='immo-list-attachments'),
    path('immobilie/attachment/upload/<uuid:uuid>/', UploadAttachmentView.as_view(), name='immo-upload-attachment'),
    path('immobilie/attachment/delete/<uuid:uuid>/', DeleteAttachmentView.as_view(), name='immo-delete-attachment'),
    path('list-by-region/<uuid:uuid>/', RegionListView.as_view(), name='immo-list-by-region'),
    path('map/', MapView.as_view(), name='immo-map'),
    path('immobilie/tag/', tag_immobilie, name='tag-immo'),
    path('api/', include(router.urls)),
    path('api/geojson/list/', GeoJSONAPIView.as_view(), name='api-geojson-list')
]