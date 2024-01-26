from rest_framework import serializers
from .models import Floor, Room


class RoomSerializer(serializers.ModelSerializer):
    floor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
         model = Room
         fields = '__all__'




class FloorSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = '__all__'
