from django.test import TestCase, Client
from django.urls import reverse
from classroom.models import RoomData, Reservation
from django.contrib.auth.models import User

class RoomTestCase(TestCase):
  def setUp(cls):
    cls.user = User.objects.create_user(username="tester", password="1234")
    cls.room = RoomData.objects.create(room_code="R001",room_name="Room_01", room_capacity=3, room_hour=2, room_available=True)

#login
  def test_login_success(self):
    response = self.client.post(reverse("login_user"), {"username":"tester", "password":"1234"})
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse("index"))
  
  def test_login_fail(self):
    response = self.client.post(reverse("login_user"), {"username":"testttt", "password":"12"})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Invalid username or password.")

#reserve_room
  def test_reserve_room_success(self):
    self.client.login(username="tester",password="1234")
    response = self.client.post(reverse("reserve", args=[self.room.id]))
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Reservation.objects.count(), 1)
  
  def test_reserve_room_unavailable(self):
    self.client.login(username="tester",password="1234")
    self.room.room_available = False
    self.room.save()
    # สร้าง Reservation ก่อน เพื่อเช็ค count ถูกต้อง
    Reservation.objects.create(user=self.user, room=self.room)
    response = self.client.post(reverse("reserve", args=[self.room.id]))
    self.assertRedirects(response, reverse("index"))
    self.assertEqual(Reservation.objects.count(), 1)

  def test_reserve_room_notlogin(self):
    response = self.client.post(reverse("reserve", args=[self.room.id]))
    self.assertRedirects(response, reverse("login_user"))

#cancel_room
  def test_cancel_reservation_success(self):
    self.client.login(username="tester",password="1234")
    response = self.client.get(reverse("cancel"))
    self.assertRedirects(response, reverse("index"))
    self.assertEqual(Reservation.objects.count(), 0)

  def test_cancal_reservation_witout_existing(self):
    self.client.logout()
    response = self.client.get(reverse("cancel"))
    self.assertRedirects(response, '/login/?next=/cancel/')
  
#logout
  def test_logout_success(self):
    self.client.login(username="tester",password="1234")
    response = self.client.get(reverse("logout_user"))
    self.assertRedirects(response, reverse("index"))

#page_test
  def test_page(self):
    response = self.client.get(reverse("index"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Room_01")
  
