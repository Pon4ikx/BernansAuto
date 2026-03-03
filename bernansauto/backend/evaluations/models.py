from django.db import models
from cars.models import Car, Motorcycle


APPLICATION_TYPE_CHOICES = [
    ("покупка", "Покупка"),
    ("консультация", "Консультация"),
    ("кредит", "Кредит"),
    ("трейд-ин", "Трейд-ин"),
    ("обратный_звонок", "Обратный звонок"),
]


class CarApplication(models.Model):
    """Заявки на автомобили."""
    name = models.CharField(max_length=150, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    application_type = models.CharField(
        max_length=50, verbose_name="Тип заявки", choices=APPLICATION_TYPE_CHOICES
    )
    message = models.TextField(blank=True, verbose_name="Сообщение")
    car = models.ForeignKey(
        Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="car_applications", verbose_name="Автомобиль"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "evaluations_car_application"
        verbose_name = "Заявка на автомобиль"
        verbose_name_plural = "Заявки на автомобили"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_application_type_display()} ({self.created_at.date()})"


class MotoApplication(models.Model):
    """Заявки на мототехнику."""
    name = models.CharField(max_length=150, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    application_type = models.CharField(
        max_length=50, verbose_name="Тип заявки", choices=APPLICATION_TYPE_CHOICES
    )
    message = models.TextField(blank=True, verbose_name="Сообщение")
    motorcycle = models.ForeignKey(
        Motorcycle, on_delete=models.SET_NULL, null=True, blank=True, related_name="moto_applications", verbose_name="Мототехника"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "evaluations_moto_application"
        verbose_name = "Заявка на мототехнику"
        verbose_name_plural = "Заявки на мототехнику"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_application_type_display()} ({self.created_at.date()})"
