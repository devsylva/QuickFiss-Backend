from django.contrib import admin
from .models import *

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UserInteraction)
admin.site.register(Post)
admin.site.register(Service, ServiceAdmin)