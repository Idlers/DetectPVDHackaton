from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViolationRecordViewSet

router = DefaultRouter()
router.register(r'violations', ViolationRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
