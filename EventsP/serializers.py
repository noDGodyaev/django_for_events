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

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Participant.objects.create(**validated_data)

    """
    def update(self, instance, validated_data):

        Update and return an existing `Snippet` instance, given the validated data.

        instance.p_id = validated_data.get('p_id', instance.p_id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.group_name = validated_data.get('group_name', instance.group_name)
        instance.vk_url = validated_data.get('vk_url', instance.vk_url)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.arrive_status = validated_data.get('arrive_status', instance.arrive_status)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.room = validated_data.get('room', instance.room)
        instance.team = validated_data.get('team', instance.team)
        instance.save()
        return instance
    """


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

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Room.objects.create(**validated_data)

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

