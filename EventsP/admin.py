from django.contrib import admin
from django.contrib import messages
from . import models
from abc import ABC


# Register your models here.
class RemoveAdminDefaultMessageMixin:

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def response_change(self, request, obj):
        """override"""
        response = super().response_change(request, obj)
        self.remove_default_message(request)
        return response

    def response_delete(self, request, obj_display, obj_id):
        """override"""
        response = super().response_delete(request, obj_display, obj_id)
        self.remove_default_message(request)
        return response


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter, ABC):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


admin.site.register(models.Event)
admin.site.register(models.Post)
admin.site.register(models.Team)


class PersonAdmin(admin.ModelAdmin, RemoveAdminDefaultMessageMixin):
    list_display = [models.Person.i_name,
                    'phone',
                    'group_name',
                    'telegram_id',
                    'vk_url',
                    'birth_date',
                    'check_in',
                    'arrive_status',
                    'room',
                    'team',
                    ]
    exclude = ['status']
    list_filter = [('group_name', custom_titled_filter('Номер группы')),
                   ('arrive_status', custom_titled_filter('Статус прибытия')),
                   ('room', custom_titled_filter('Номер комнаты')),
                   ('team', custom_titled_filter('Команда'))]
    search_fields = [field.name for field in models.Person._meta.fields]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['status']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        tmp = models.Participant.objects.filter(room=obj.room)
        rooms = models.Room.objects.filter(r_id=obj.room.r_id)
        if tmp.exists():
            for room in rooms:
                if len(tmp) < room.bed_num:
                    super().save_model(request, obj, form, change)
                else:
                    messages.error(request, 'В комнате заняты все места')
        else:
            super().save_model(request, obj, form, change)

    class Meta:
        model = models.Participant


admin.site.register(models.Participant, PersonAdmin)


class OrgAdmin(admin.ModelAdmin):
    list_display = [models.Person.i_name,
                    'first_name',
                    'middle_name',
                    'family_name',
                    'phone',
                    'group_name',
                    'telegram_id',
                    'vk_url'
                    ]
    exclude = ['status']
    list_filter = [('group_name', custom_titled_filter('Номер группы'))]
    search_fields = [field.name for field in models.Participant._meta.fields]

    class Meta:
        model = models.Org


admin.site.register(models.Org, OrgAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_num',
                    'room_floor',
                    'room_building',
                    'bed_num',
                    'features']

    class Meta:
        model = models.Room


admin.site.register(models.Room, RoomAdmin)


class TimetableAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):
    list_display = ['id_person_post',
                    'id_event',
                    'team',
                    'place',
                    models.Timetable.b_time]

    def save_model(self, request, obj, form, change):
        tmp = models.Timetable.objects.filter(id_person_post=obj.id_person_post)
        if tmp.exists():
            fl = True
            for timetable in tmp:
                if timetable.event_start_time < obj.event_end_time and \
                        timetable.event_end_time > obj.event_start_time:
                    fl = False
            if fl:
                super().save_model(request, obj, form, change)
            else:
                messages.error(request, 'Временной интервал некорректен')
        else:
            super().save_model(request, obj, form, change)


class Meta:
    model = models.Timetable


admin.site.register(models.Timetable, TimetableAdmin)


class BusynessInline(admin.TabularInline):
    model = models.Timetable
    extra = 0


class PPostAdmin(admin.ModelAdmin):
    list_display = ['id_person',
                    'id_post']
    inlines = [BusynessInline]

    class Meta:
        model = models.PersonWithPost


admin.site.register(models.PersonWithPost, PPostAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['place_name',
                    'features']

    class Meta:
        model = models.Place


admin.site.register(models.Place, PlaceAdmin)


class ReqAdmin(admin.ModelAdmin):
    list_display = ['req_name',
                    'req_amount',
                    'req_description',
                    'req_owner', ]

    class Meta:
        model = models.Room


admin.site.register(models.Requisite, ReqAdmin)
# Register your models here.
