from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime
from .mymodels.ReturningCitizen import ReturningCitizen
from .mymodels.Mentor import Mentor
from .mymodels.Event import Event
from .mymodels.ParoleAddress import ParoleAddress
from .mymodels.ParoleOfficer import ParoleOfficer
from .mymodels.DailyResponse import DailyResponse
from .mymodels.TempLogins import TempUserLogin, TempParoleOfficerLogin, TempMentorLogin
from .mymodels.ThreeDailyActions import ThreeDailyActions
from .mymodels.CommunityHealthOrg import CommunityHealthOrganization
from datetime import date
from django.db import models
from django import forms

class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    formfield_overrides = {
        models.DateTimeField: {'widget': AdminSplitDateTime},
    }

class ParoleAddressInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()

        filled_out_forms = sum(bool(form.cleaned_data) for form in self.forms)
        if filled_out_forms == 0:
            raise forms.ValidationError("At least one ParoleAddress must be provided.")

class ParoleAddressInline(admin.TabularInline):
    model = ParoleAddress
    extra = 1
    min_num = 1
    max_num = 1
    formset = ParoleAddressInlineFormset
    def has_delete_permission(self, request, obj=None):
        return False

class DailyResponseInline(admin.TabularInline):
    model = DailyResponse
    extra = 1
    
class ReturningCitizenAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Returning Citizen Information', {
            'fields': ('first_Name', 'last_Name', 'MDOC', 'active')
        }),
        ('Care Team', {
            'fields': ('myMentor', 'myParoleOfficer'),
        }),
    )

    list_display = ("__str__", "get_daily_response_avg", "get_mentor", "get_parole_offcer", "active", "get_pa", "upcoming_events", "past_events")
    actions = ['set_inactive']
    inlines = [DailyResponseInline, ParoleAddressInline, EventInline]
    #
    #
    #
    def get_daily_response_avg(self, obj):
        total = 0
        responses = obj.daily_responses.all()
        response_count = responses.count()

        if response_count > 0:
            for response in responses:
                total += response.rating

            return str(total / response_count)
        else:
            return "None Logged"
    get_daily_response_avg.short_description = 'Average Feeling ( x/10 )'
    #
    #
    #
    def get_pa(self, obj):
        try:
            parole_address = obj.paroleAddress.get()
            return str(parole_address)
        except ParoleAddress.DoesNotExist:
            return "No Parole Address" 
    get_pa.short_description = 'Parole Address'
    #
    #
    #
    def get_mentor(self, obj):
        if obj.myMentor:
            return f"{obj.myMentor}"
        else:
            return "No Mentor Assigned"
    get_mentor.short_description = 'Mentor'
    #
    #
    #
    def upcoming_events(self, obj):
        if obj.events.exists():
            return sum(1 for evnt in obj.events.all() if evnt.is_valid())
        else:
            return 0
    upcoming_events.short_description = '# of Upcoming Events'
    #
    #
    #
    def past_events(self, obj):
        if obj.events.exists():
            return sum(1 for evnt in obj.events.all() if not evnt.is_valid())
        else:
            return 0
    past_events.short_description = '# of Past Events'
    #
    #
    #
    def get_parole_offcer(self, obj):
        if obj.myParoleOfficer:
            return f"{obj.myParoleOfficer}"
        else:
            return "No Parole Officer Assigned"
    get_parole_offcer.short_description = 'Parole Officer'
    #
    #
    #
    def set_inactive(self, request, queryset):
        for user in queryset:
            user.active = False
            user.save()
            user.date_deactivated = date.today()
    set_inactive.short_description = "Set inactive"


# =======================================================================
    


# Mentor & Parole Officer Admin # --------------------------------------------------------

class ReturningCitizenInline(admin.StackedInline):
    model = ReturningCitizen
    extra = 0
    max_num = 0
    fields = ('first_Name', 'last_Name', 'MDOC','p_address' ,'myMentor', 'myParoleOfficer', 'upcoming_events', 'past_events', 'num_comp_da', 'num_uncomp_da')
    readonly_fields = fields

    def p_address(self, obj):
        return obj.paroleAddress
    p_address.short_description = 'Parole Address'
    def upcoming_events(self, obj):
        if obj.events.exists():
            return sum(1 for action in obj.events.all() if action.is_valid())
        else:
            return 0
    upcoming_events.short_description = '# Active Events'
    #
    #
    #
    def past_events(self, obj):
        if obj.events.exists():
            return sum(1 for action in obj.events.all() if not action.is_valid())
        else:
            return 0
    past_events.short_description = '# Past Events'

    def num_comp_da(self, obj):
        if obj.daily_actions.exists():
            return sum(1 for action in obj.daily_actions.all() if action.is_completed)
        else:
            return 0
    num_comp_da.short_description = "Completed DAS"

    def num_uncomp_da(self, obj):
        if obj.daily_actions.exists():
            return sum(1 for action in obj.daily_actions.all() if not action.is_completed)
        else:
            return 0
    num_uncomp_da.short_description = "Un-Completed DAS"

    

class MentorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "count")
    inlines = []

    def count(self, obj):
        return obj.returning_citizens.count()

    count.short_description = 'Amount of Assigned Returning Citizens'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        mentor = Mentor.objects.get(pk=object_id)
        self.inlines = [ReturningCitizenInline] if mentor.returning_citizens.exists() else []
        return super().change_view(request, object_id, form_url, extra_context)

class ParoleOfficerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "count")
    inlines = []

    def count(self, obj):
        return obj.returning_citizens.count()

    count.short_description = 'Amount of Assigned Returning Citizens'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        po = ParoleOfficer.objects.get(pk=object_id)
        self.inlines = [ReturningCitizenInline] if po.returning_citizens.exists() else []
        return super().change_view(request, object_id, form_url, extra_context)
    
# -----------------------------------------------------------------------

# Register Models =======================================================
admin.site.register(ReturningCitizen, ReturningCitizenAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(ParoleOfficer, ParoleOfficerAdmin)
admin.site.register(TempUserLogin)
admin.site.register(TempMentorLogin)
admin.site.register(TempParoleOfficerLogin)
admin.site.register(CommunityHealthOrganization)
admin.site.register(ThreeDailyActions)

admin.site.site_header = "Total Reentry Solutions"
admin.site.site_title = "TRS Admin Portal"
admin.site.index_title = "Total Reentry Solution Admin Portal"