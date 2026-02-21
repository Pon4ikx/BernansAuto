from django.db import models


class Service(models.Model):
    """Услуги: название, описание, иконка (emoji или путь к svg)."""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=500, blank=True, verbose_name="Иконка (emoji или путь к svg)")

    class Meta:
        db_table = "services_service"
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["id"]

    def __str__(self):
        return self.title
