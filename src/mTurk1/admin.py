from django.contrib import admin
from mTurk1.models import Key_sim_pair, GUI_report_1, Report_group, Sim_setup,\
    Agent_setup, View_setup, Simulation, Simulation_instance, Pass_key_group,\
    Experiment_group, Report_group2



#class ReportInline(admin.TabularInline):
#    model = GUI_report_1
#
#class ReportGroupInline(admin.TabularInline):
#    model=Report_group
#
#class Report_group_admin(admin.ModelAdmin):
#    readonly_fields=[]
#    inlines = [
#        ReportInline,    
#    ]
#
#class Key_sim_admin(admin.ModelAdmin):
#    inlines=[
#             ReportGroupInline,
#             ]

class GUI_admin(admin.ModelAdmin):
    readonly_fields = ['created']


class File_admin(admin.ModelAdmin):
    readonly_fields=['created_at','updated_at']

class Simulation_admin(admin.ModelAdmin):
    readonly_fields=['created_at','updated_at']
    
class ExperimentInline(admin.TabularInline):
    model = Pass_key_group
    extra=0
class Experiment_admin(admin.ModelAdmin):
    readonly_fields=['created_at','updated_at']
    inlines=[ExperimentInline]    
class ReportGroupInline(admin.TabularInline):
    model=GUI_report_1
    extra=0

class Report_Group_admin(admin.ModelAdmin):
    inlines=[ReportGroupInline]
#admin.site.register(GUI_report_1,GUI_admin)
#admin.site.register(Report_group,Report_group_admin)
#admin.site.register(Key_sim_pair, Key_sim_admin)
admin.site.register(Sim_setup, File_admin)
admin.site.register(Agent_setup, File_admin)
admin.site.register(View_setup, File_admin)
admin.site.register(Simulation,Simulation_admin)
admin.site.register(Simulation_instance,Simulation_admin)
admin.site.register(Pass_key_group)
admin.site.register(Experiment_group,Experiment_admin)
admin.site.register(GUI_report_1)
admin.site.register(Report_group2, Report_Group_admin)