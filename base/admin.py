from django.contrib import admin
from . import models


MyModels = [models.Depart, models.Student, models.Company,
            models.Apps, models.Position]


admin.site.register(MyModels)
