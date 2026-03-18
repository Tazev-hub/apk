// ==========================================
// 1. ГЛОБАЛЬНЫЕ ФУНКЦИИ
// ==========================================

// Переключение тёмной темы
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
        themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
}

// Функция для открытия модалки с описанием специальности
function showSpecialty(title, code, duration, description, subjects, jobs) {
    document.getElementById('specialtyModalLabel').textContent = title;
    
    const body = document.getElementById('specialtyModalBody');
    body.innerHTML = `
        <p><strong>Код:</strong> ${code}</p>
        <p><strong>Срок обучения:</strong> ${duration}</p>
        <p>${description}</p>
        <div class="row">
            <div class="col-md-6">
                <strong>Ключевые дисциплины:</strong>
                <ul>${subjects}</ul>
            </div>
            <div class="col-md-6">
                <strong>Кем работать:</strong>
                <ul>${jobs}</ul>
            </div>
        </div>
    `;
    
    // Показываем модалку
    var myModal = new bootstrap.Modal(document.getElementById('specialtyModal'));
    myModal.show();
}

// ==========================================
// 2. ЗАГРУЗКА СТРАНИЦЫ
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== 2.1. Загрузка тёмной темы =====
    const savedTheme = localStorage.getItem('theme');
    const themeIcon = document.getElementById('themeIcon');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeIcon) themeIcon.textContent = '☀️';
    }
    
    // ===== 2.2. Инициализация AOS =====
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100,
        });
    }
    
    // ===== 2.3. Обработка контактной формы =====
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const formStatus = document.getElementById('formStatus');
            const formData = new FormData(this);
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Отправка...';
            formStatus.innerHTML = '';
            
            fetch('/send-contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    formStatus.innerHTML = '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                        '<strong>Спасибо!</strong> Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.' +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                        '</div>';
                    contactForm.reset();
                } else {
                    formStatus.innerHTML = '<div class="alert alert-danger">' +
                        '<strong>Ошибка!</strong> ' + (data.message || 'Не удалось отправить сообщение. Попробуйте позже.') +
                        '</div>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                formStatus.innerHTML = '<div class="alert alert-danger">' +
                    '<strong>Ошибка сети!</strong> Проверьте подключение и попробуйте снова.' +
                    '</div>';
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Отправить';
            });
        });
    }
    
    // ===== 2.4. Обработка формы на странице абитуриента =====
    const abiturientForm = document.getElementById('abiturientForm');
    if (abiturientForm) {
        abiturientForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const formStatus = document.getElementById('formStatus');
            const formData = new FormData(this);
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Отправка...';
            formStatus.innerHTML = '';
            
            fetch('/send-contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    formStatus.innerHTML = '<div class="alert alert-success">' +
                        'Спасибо! Ваш вопрос отправлен. Мы ответим вам в ближайшее время.' +
                        '</div>';
                    abiturientForm.reset();
                } else {
                    formStatus.innerHTML = '<div class="alert alert-danger">' +
                        'Ошибка: ' + (data.message || 'Не удалось отправить') +
                        '</div>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                formStatus.innerHTML = '<div class="alert alert-danger">' +
                    'Ошибка сети. Попробуйте позже.' +
                    '</div>';
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Отправить сообщение';
            });
        });
    }
});