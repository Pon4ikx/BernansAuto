from django.db import models
from cars.models import Car, Motorcycle


class Application(models.Model):
    """Заявки: имя, телефон, email, тип_заявки, сообщение, авто_id, мототехника_id, дата_создания."""
    APPLICATION_TYPE_CHOICES = [
        ("покупка", "Покупка"),
        ("консультация", "Консультация"),
        ("кредит", "Кредит"),
        ("трейд-ин", "Трейд-ин"),
        ("обратный_звонок", "Обратный звонок"),
    ]
    name = models.CharField(max_length=150, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    application_type = models.CharField(
        max_length=50, verbose_name="Тип заявки", choices=APPLICATION_TYPE_CHOICES
    )
    message = models.TextField(blank=True, verbose_name="Сообщение")
    car = models.ForeignKey(
        Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications", verbose_name="Автомобиль"
    )
    motorcycle = models.ForeignKey(
        Motorcycle, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications", verbose_name="Мототехника"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "evaluations_application"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_application_type_display()} ({self.created_at.date()})"
