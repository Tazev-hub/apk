from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # ← добавляем эту строку
    path('schedule/', views.schedule_view, name='schedule'),
    path('schedule/<int:schedule_id>/', views.schedule_detail_view, name='schedule_detail'),
    path('students/', views.students_view, name='students'),
    path('send-contact/', views.send_contact, name='send_contact'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

