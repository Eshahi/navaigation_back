from django.urls import path, include
from admin_panel import views
from rest_framework.routers import DefaultRouter

from admin_panel.views import FloorViewSet, RoomViewSet,get_path

router = DefaultRouter()
router.register(r'floors', FloorViewSet, basename='floor')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
    path('rooms/path/<int:from_room_id>/<int:to_room_id>/', views.get_path, name='get_path'),
]