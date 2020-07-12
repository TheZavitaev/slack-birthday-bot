from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views import SlackEventsSubscriptionViewSet

router = DefaultRouter()
router.register('events', SlackEventsSubscriptionViewSet, basename='events_subscription')

urlpatterns = [
    path('', include(router.urls)),
]