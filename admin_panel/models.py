from django.db import models


class Floor(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define an ID field
    floor_number = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'floor'


class Room(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define an ID field
    floor = models.ForeignKey(Floor, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    is_elevator = models.BooleanField(default=False)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    class Meta:
        db_table = 'room'


class Occupant(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_info = models.TextField()
    space = models.ForeignKey(Room, on_delete=models.CASCADE)
    additional_info = models.TextField()

    class Meta:
        db_table = 'occupant'


# Assuming your other models are defined above...

class Connection(models.Model):
    from_room = models.ForeignKey(Room, related_name='connections_from', on_delete=models.CASCADE)
    to_room = models.ForeignKey(Room, related_name='connections_to', on_delete=models.CASCADE)
    distance = models.FloatField()  # This can store the calculated distance between rooms

    class Meta:
        db_table = 'connection'
        unique_together = ('from_room', 'to_room')

    def __str__(self):
        return f"Connection from {self.from_room.name} to {self.to_room.name}"


# Add a function to rebuild connections for a room
def rebuild_connections_for_room(room):
    # This function will delete old connections and create new ones based on the updated room information.
    # It should contain the logic from your graph-building algorithm.
    pass

# Create your models here.
