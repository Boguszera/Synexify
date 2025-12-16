from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from infrastructure.orm.models.notification_model import NotificationModel


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(NotificationModel, id=pk, user_id=request.user.id)
    notif.is_read = True
    notif.save()

    if notif.task_id:
        return redirect('web:task_detail', pk=notif.task_id)

    return redirect('web:project_list')


@login_required
def clear_notifications(request):
    NotificationModel.objects.filter(user_id=request.user.id, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'web:project_list'))