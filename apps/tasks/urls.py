from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tasks.views.views import TaskViewset

router = DefaultRouter()
router.register(r'tasks', TaskViewset, basename='tasks')

urlpatterns = [
    path('', include(router.urls))
]
