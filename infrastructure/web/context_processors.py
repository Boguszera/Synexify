from django.conf import settings

from infrastructure.orm.models.notification_model import NotificationModel


def user_notifications(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        notifications = NotificationModel.objects.filter(user_id=user_id, is_read=False)[:10]

        count = NotificationModel.objects.filter(user_id=user_id, is_read=False).count()

        return {"notifications_list": notifications, "notifications_count": count}
    return {"notifications_list": [], "notifications_count": 0}


def demo_mode(request):
    return {"DEMO_MODE": getattr(settings, "DEMO_MODE", False)}
