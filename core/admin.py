from django.contrib import admin

import core.models

myModels = [core.models.Immobilie, core.models.ImmobilienResource, core.models.Region]
admin.site.register(myModels)