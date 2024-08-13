from django.contrib import admin
from . import models
# Register your models here.

class TagAdmin(admin.ModelAdmin):
  search_fields=['label']


admin.site.register(models.Tag, TagAdmin)
