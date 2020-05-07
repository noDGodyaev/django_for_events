from django.conf.urls import url, include
from . import views

app_name = 'EventsP'

urlpatterns = [
    # url(r'^sponsor/([0-9]{6})$', views.sponsor, name="Sponsor"),  # http://127.0.0.1:8000/sponsor/1234
    url(r'^register$', views.RegisterFormView.as_view()),
    url(r'^login$', views.LoginFormView.as_view()),
    url(r'^logout$', views.LogoutView.as_view()),
    url(r'^$', views.MainView.as_view(), name='Homepage'),  # http://127.0.0.1:8000/
    url(r'^json-upload$', views.JSONPartView),
    url(r'^json-upload-room$', views.JSONRoomView),
    url(r'^json-upload-team$', views.JSONTeamView),
    url(r'^json-upload-timetable$', views.JSONTimetableView),
]
