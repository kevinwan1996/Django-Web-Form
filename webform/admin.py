from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import *
# Register your models here.

class RulesAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'max_length':400})}
	}
class IVVAdmin(admin.ModelAdmin):
	list_display = ['ivv_id']
admin.site.register(IVV, IVVAdmin)

class StateAdmin(admin.ModelAdmin):
	list_display = ['state_id', 'state_name', 'POC_name', 'POC_email', 'update_date']

admin.site.register(State, StateAdmin)
admin.site.register(Submitter)
admin.site.register(LifeCycle)
admin.site.register(Recommendations)
admin.site.register(Risk)
admin.site.register(Entire)
admin.site.register(PDF)
admin.site.register(Email)