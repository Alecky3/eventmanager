from django.contrib import admin

from eventmanager.views import login
from .models import *

admin.site.register(Event)
admin.site.register(User)
admin.site.register(Login)
admin.site.register(EventCategories)
admin.site.register(EventSubcategories)
admin.site.register(UserEvents)
admin.site.register(Advertisements)
admin.site.register(Messages)


