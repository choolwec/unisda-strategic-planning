from django.contrib import admin
from .models import Designation, StrategicTheme, StrategicObjective, KPI, Activity, User, Role, Report

# Register each model with the admin site
admin.site.register(StrategicTheme)
admin.site.register(StrategicObjective)
admin.site.register(Designation)
admin.site.register(KPI)
admin.site.register(Activity)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Report)