from rest_framework import serializers
from .models import Participant
from .models import Room


class ParticipantSerializer(serializers.Serializer):
    p_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=20)
    middle_name = serializers.CharField(max_length=20)
    family_name = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=15)
    group_name = serializers.CharField(max_length=10, required=False, allow_blank=True)
    telegram_id = serializers.CharField(max_length=50)
    vk_url = serializers.CharField(max_length=50)
    birth_date = serializers.DateField(required=False)
    check_in = serializers.DateTimeField(required=False)
    arrive_status = serializers.IntegerField(default=0)
    r_id = serializers.IntegerField(required=False)
    room_num = serializers.IntegerField(required=False)
    bed_num = serializers.IntegerField(required=False)
    t_id = serializers.IntegerField(required=False)
    team_name = serializers.CharField(required=False)


class TeamSerializer(serializers.Serializer):
    t_id = serializers.IntegerField(read_only=True)
    team_name = serializers.CharField()


class RoomSerializer(serializers.Serializer):
    r_id = serializers.IntegerField(read_only=True)
    room_num = serializers.IntegerField()

    # room_floor = serializers.IntegerField(required=False)
    # room_building = serializers.CharField(max_length=5, required=False)
    # bed_num = serializers.IntegerField()
    # features = serializers.CharField(max_length=4000, required=False)


class TimetableSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    event_start_time = serializers.DateTimeField()
    event_end_time = serializers.DateTimeField()
    first_name = serializers.CharField(max_length=20)
    middle_name = serializers.CharField(max_length=20)
    family_name = serializers.CharField(max_length=20)
    post_name = serializers.CharField(max_length=20)
    post_id = serializers.IntegerField(read_only=True)
    place_name = serializers.CharField(max_length=20)
    place_id = serializers.IntegerField(read_only=True)
    ev_id = serializers.IntegerField(read_only=True)
    ev_name = serializers.CharField(max_length=20)
    t_id = serializers.IntegerField(read_only=True)
    team_name = serializers.CharField(max_length=20)

