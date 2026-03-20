from django.db import models

from django.db import models

class Announcement(models.Model):
    """Объявления для студентов"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст объявления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_pinned = models.BooleanField(default=False, verbose_name="Закрепить вверху")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-is_pinned', '-created_at']  # Сначала закреплённые, потом новые
    
    def __str__(self):
        return self.title

class Schedule(models.Model):
    """Расписание (общее для всех групп)"""
    title = models.CharField(max_length=100, verbose_name="Название", default="Расписание")
    date = models.DateField(verbose_name="На какую дату")
    is_active = models.BooleanField(default=True, verbose_name="Актуальное")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} от {self.date}"

class SchedulePage(models.Model):
    """Страница расписания (одно фото)"""
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='pages', verbose_name="Расписание")
    image = models.ImageField(upload_to='schedules/', verbose_name="Фото страницы")
    page_number = models.PositiveIntegerField(verbose_name="Номер страницы")
    
    class Meta:
        verbose_name = "Страница расписания"
        verbose_name_plural = "Страницы расписания"
        ordering = ['page_number']
    
    def __str__(self):
        return f"{self.schedule} - страница {self.page_number}"
    
class Material(models.Model):
    """Методические материалы"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    file = models.FileField(upload_to='materials/', verbose_name="Файл (PDF)")
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    class Meta:
        verbose_name = "Методичка"
        verbose_name_plural = "Методички"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
class ContactMessage(models.Model):
    """Сообщения из контактной формы"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"