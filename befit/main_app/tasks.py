from celery import shared_task
from django.utils import timezone
from .models import Subscription

@shared_task
def deactivate_expired_subscriptions():
    today = timezone.now().date()
    subscriptions = Subscription.objects.filter(status='Active')
    
    for subscription in subscriptions:
        if subscription.endDate < today:  # If subscription is expired
            subscription.status = 'Inactive'
            subscription.save()
