from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views import SlackEventsSubscriptionViewSet, SlackInteractionsSubscriptionViewSet

router = DefaultRouter()
router.register('events', SlackEventsSubscriptionViewSet, basename='events_subscription')
router.register('interactions', SlackInteractionsSubscriptionViewSet, basename='interactions_subscription')

urlpatterns = [
    path('', include(router.urls)),
]