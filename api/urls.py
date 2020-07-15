from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views import SlackEventsSubscriptionViewSet, SlackInteractionsSubscriptionViewSet, \
    StartViewSet, StopViewSet

router = DefaultRouter()
router.register('events', SlackEventsSubscriptionViewSet, basename='events_subscription')
router.register('interactions', SlackInteractionsSubscriptionViewSet, basename='interactions_subscription')
router.register('start', StartViewSet, basename='start')
router.register('stop', StopViewSet, basename='stop')

urlpatterns = [
    path('', include(router.urls)),
]
