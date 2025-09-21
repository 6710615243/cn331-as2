from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RoomData(models.Model):
    room_code = models.CharField(max_length=6)
    room_name = models.CharField(max_length=10)
    room_capacity = models.IntegerField()
    room_hour = models.IntegerField(default=2)
    room_available = models.BooleanField(default=True)

    #String repretentation of the tour
    def __str__(self):
        return (f"ID:{self.id} Room name : {self.room_name} code : {self.room_code} Capacity : {self.room_capacity} hours : {self.room_hour} Available : {self.room_available}" )


# Reservation
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomData, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.room.room_name}"