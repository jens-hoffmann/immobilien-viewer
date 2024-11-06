from core.models import Region

def regions_to_base(request):
    regions = Region.objects.all()
    return {'regionen': regions}
