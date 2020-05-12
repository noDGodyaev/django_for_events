from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import UserCreateForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from .forms import UserCreateForm
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import PartForm
from django.views.generic import ListView
from django.http import JsonResponse
import io
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import ParticipantSerializer, RoomSerializer, TeamSerializer, TimetableSerializer
import json

'''Функция для установки сессионного ключа.
По нему django будет определять, выполнил ли вход пользователь.'''


class MainView(TemplateView):
    template_name = 'ajax.html'
    participant_form = PartForm

    def get(self, request):
        if request.user.is_authenticated:
            participants = models.Participant.objects.all()
            ctx = {}
            ctx['participants'] = participants
            ctx['participant_form'] = self.participant_form
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})


def JSONPartView(request):
    # json_data = serializers.serialize('json', models.Person.objects.all())
    # json_data = serializers.serialize('json', models.Participant.objects.select_related())
    # tmp = models.Participant.objects.all().values('first_name', 'birth_date')
    # json_data = serializers.serialize('json', tmp)
    # listt = [*models.Person.objects.filter(status=2), *models.Participant.objects.filter(person_ptr_id)]
    # listt = models.Participant.objects.select_related('person_ptr')
    if request.method == 'GET':
        if request.user.is_authenticated:
            query = "SELECT\
            p.p_id,\
            p.first_name,\
            p.middle_name,\
            p.family_name,\
            p.phone,\
            p.group_name,\
            p.vk_url,\
            part.birth_date,\
            part.check_in,\
            part.arrive_status, \
            r.r_id, \
            r.room_num, \
            r.bed_num, \
            t.t_id,\
            t.team_name\
            FROM\
            ev_people as p, \
            ev_Part as part \
                LEFT OUTER JOIN ev_rooms as r\
                ON part.room_id = r.r_id\
                LEFT OUTER JOIN ev_teams as t\
                ON part.team_id = t.t_id\
            WHERE\
            part.person_ptr_id = p.p_id;"
            participants = models.Person.objects.raw(query)
            serializer = ParticipantSerializer(participants, many=True)
            return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        if request.is_ajax():
            data = json.loads(request.body)
            person = models.Participant.objects.get(p_id=data['p_id'])
            person.first_name = data['first_name']
            person.middle_name = data['middle_name']
            person.family_name = data['family_name']

            person.phone = data['phone']
            person.group_name = data['group_name']
            person.vk_url = data['vk_url']
            person.birth_date = data['birth_date'].split('T')[0]
            # person.check_in = data['check_in']
            person.arrive_status = data['arrive_status']
            room = models.Room.objects.get(r_id=data['room'])
            person.room = room
            if data['team'] != '':
                team = models.Team.objects.get(t_id=data['team'])
                person.team = team
            person.save()
            print('correct form')
            return HttpResponse(status=201)
        else:
            print('incorrect form')
            return HttpResponse(status=400)


def JSONRoomView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            query = 'SELECT r_id, room_num, bed_num\
                     FROM ev_rooms\
                            LEFT OUTER JOIN (\
                                SELECT room_id, count(*) as c\
                                FROM ev_part\
                                WHERE room_id IS NOT NULL\
                                GROUP BY room_id) A ON ev_rooms.r_id = A.room_id\
                     WHERE bed_num > COALESCE(A.c, 0);'
            rooms = models.Room.objects.raw(query)
            serializer = RoomSerializer(rooms, many=True)
            return JsonResponse(serializer.data, safe=False)


def JSONTeamView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            rooms = models.Team.objects.all()
            serializer = TeamSerializer(rooms, many=True)
            return JsonResponse(serializer.data, safe=False)


def JSONTimetableView(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            query = "SELECT ev_timetable.event_start_time,\
            ev_timetable.event_end_time,\
            ev_timetable.id,\
            Ev_People.first_name,\
            Ev_People.middle_name,\
            Ev_People.family_name,\
            ev_posts.post_name,\
            Ev_Posts.post_id,\
            Ev_Places.place_id,\
            Ev_Places.place_name,\
            Ev_Events.ev_id,\
            Ev_Events.ev_name,\
            Ev_Teams.team_name,\
            Ev_Teams.t_id\
            FROM ev_timetable\
                LEFT JOIN ev_person_posts as pp ON ev_timetable.id_person_post = pp.id\
                LEFT JOIN ev_org ON pp.org_id = Ev_Org.org_id\
                LEFT JOIN ev_posts ON pp.id_post = Ev_Posts.post_id\
                LEFT JOIN ev_people ON Ev_Org.person_ptr_id = Ev_People.p_id\
                LEFT OUTER JOIN ev_places ON ev_timetable.id_place = Ev_Places.place_id\
                LEFT OUTER JOIN ev_teams ON ev_timetable.id_team = ev_teams.t_id\
                LEFT JOIN ev_events ON ev_timetable.id_event = Ev_Events.ev_id;"
            timetable = models.Timetable.objects.raw(query)
            serializer = TimetableSerializer(timetable, many=True)
            return JsonResponse(serializer.data, safe=False)


class RegisterFormView(FormView):
    form_class = UserCreateForm
    success_url = "/events/login"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"

    success_url = "/events/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/events/")
