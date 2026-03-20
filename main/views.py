from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Schedule, Announcement, Material, ContactMessage
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@cache_page(60 * 15)
def home(request):
    """Главная страница"""
    return render(request, 'index.html')

def schedule_view(request):
    """Страница с расписанием (список всех)"""
    # Берём последнее активное расписание
    current = Schedule.objects.filter(is_active=True).first()
    
    # Берём все расписания для архива (кроме текущего, если оно есть)
    archive = Schedule.objects.all()
    if current:
        archive = archive.exclude(pk=current.pk)
    
    return render(request, 'schedule.html', {
        'current': current,
        'archive': archive
    })

def schedule_detail_view(request, schedule_id):
    """Страница просмотра конкретного расписания"""
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    pages = schedule.pages.all().order_by('page_number')
    
    return render(request, 'schedule_detail.html', {
        'schedule': schedule,
        'pages': pages,
    })

def students_view(request):
    """Страница для студентов с вкладками"""
    announcements = Announcement.objects.filter(is_active=True)
    materials = Material.objects.all()
    
    return render(request, 'students.html', {
        'announcements': announcements,
        'materials': materials,
    })

def contacts_view(request):
    """Страница контактов"""
    return render(request, 'contacts.html')

def sveden_view(request):
    """Страница сведений об образовательной организации"""
    return render(request, 'sveden.html')

def abiturient_view(request):
    """Страница для абитуриентов"""
    return render(request, 'abiturient.html')

@csrf_exempt
def send_contact(request):
    """Отправка сообщения с контактной формы на почту"""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        # Формируем текст письма
        subject = f'Сообщение с сайта от {name}'
        body = f"""
        Имя: {name}
        Email: {email}
        
        Сообщение:
        {message}
        """
        
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Отправляем себе же
                fail_silently=False,
            )
            return JsonResponse({'status': 'ok', 'message': 'Сообщение отправлено!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=400)

@csrf_exempt
def send_contact(request):
    """Сохранение сообщения в базу данных"""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            return JsonResponse({'status': 'ok', 'message': 'Сообщение отправлено!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Заполните все поля'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=400)