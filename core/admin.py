from django.contrib import admin
from .models import Notification


#

# REMOVED FOR NOW
#
#######################################
# class AdminSite(admin.AdminSite):
#     def get_urls(self):
#         urls = super().get_urls()
#         urls += [
#             path('notify/', self.admin_view(self.send_notification))
#         ]
#
#         return urls
#
#     def send_notification(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             context = self.each_context(request)
#
#             request.current_app = self.name
#             return TemplateResponse(request, 'admin-custom/core/notify.html', context=context)
#
#         if request.method == 'POST':
#             notification_text = request.POST.get('notification-text')
#
#             if notification_text is not None:
#                 layer = get_channel_layer()
#                 async_to_sync(layer.group_send)(
#                     'notifications',
#                     {
#                         "type": "handle.notification",
#                         "notification": {
#                             'content': notification_text
#                         }
#                     }
#                 )
#
#                 return HttpResponse(status=204)
#
#
# admin_site = AdminSite(name='default-admin-site')
#######################################

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
