from django.conf import settings
from django.db import models


class Car(models.Model):
    """Автомобили."""
    marka = models.CharField(max_length=100, verbose_name="Марка", default="")
    car_model = models.CharField(max_length=100, verbose_name="Модель", default="")
    year = models.PositiveIntegerField(verbose_name="Год выпуска", default=2000)
    mileage = models.PositiveIntegerField(verbose_name="Пробег", default=0)
    body_type = models.CharField(max_length=50, blank=True, verbose_name="Тип кузова")
    engine_type = models.CharField(max_length=50, blank=True, verbose_name="Тип двигателя")
    transmission = models.CharField(max_length=50, blank=True, verbose_name="Коробка передач")
    drive_type = models.CharField(max_length=50, blank=True, verbose_name="Привод")
    price_byn = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Цена BYN"
    )
    price_usd = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Цена USD"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Доступно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "cars_car"
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.marka} {self.car_model} ({self.year})"


class Motorcycle(models.Model):
    """Мототехника: марка, модель, год, пробег, объём двигателя, тип (мотоцикл/квадроцикл/скутер), цены, описание, доступно, дата_создания."""
    MOTO_TYPE_CHOICES = [
        ("мотоцикл", "Мотоцикл"),
        ("квадроцикл", "Квадроцикл"),
        ("скутер", "Скутер"),
    ]
    marka = models.CharField(max_length=100, verbose_name="Марка", default="")
    moto_model = models.CharField(max_length=100, verbose_name="Модель", default="")
    year = models.PositiveIntegerField(verbose_name="Год выпуска", default=2000)
    mileage = models.PositiveIntegerField(verbose_name="Пробег", default=0)
    engine_volume = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Объём двигателя"
    )
    moto_type = models.CharField(
        max_length=50, blank=True, verbose_name="Тип", choices=MOTO_TYPE_CHOICES
    )
    price_byn = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Цена BYN"
    )
    price_usd = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Цена USD"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Доступно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "cars_motorcycle"
        verbose_name = "Мототехника"
        verbose_name_plural = "Мототехника"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.marka} {self.moto_model} ({self.year})"


class Car_Photo(models.Model):
    """Фото_авто: авто_id (FK → Автомобили), ссылка_на_фото (строка)."""
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="photos", verbose_name="Автомобиль"
    )
    link = models.CharField(max_length=500, verbose_name="Ссылка на фото")

    class Meta:
        db_table = "cars_car_photo"
        verbose_name = "Фото автомобиля"
        verbose_name_plural = "Фото автомобилей"
        ordering = ["id"]

    def __str__(self):
        return f"Фото — {self.car}"


class Moto_Photo(models.Model):
    """Фото_мототехники: мототехника_id (FK → Мототехника), ссылка_на_фото (строка)."""
    motorcycle = models.ForeignKey(
        Motorcycle, on_delete=models.CASCADE, related_name="photos", verbose_name="Мототехника"
    )
    link = models.CharField(max_length=500, verbose_name="Ссылка на фото")

    class Meta:
        db_table = "cars_moto_photo"
        verbose_name = "Фото мототехники"
        verbose_name_plural = "Фото мототехники"
        ordering = ["id"]

    def __str__(self):
        return f"Фото — {self.motorcycle}"


class Favorite(models.Model):
    """Избранное: пользователь_id, авто_id (NULL), мототехника_id (NULL), дата_добавления."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, null=True, blank=True, related_name="favorites", verbose_name="Автомобиль"
    )
    motorcycle = models.ForeignKey(
        Motorcycle, on_delete=models.CASCADE, null=True, blank=True, related_name="favorites", verbose_name="Мототехника"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        db_table = "cars_favorite"
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(car__isnull=False) | models.Q(motorcycle__isnull=False),
                name="favorite_car_or_moto",
            ),
            models.UniqueConstraint(
                fields=["user", "car"], condition=models.Q(car__isnull=False), name="unique_user_car"
            ),
            models.UniqueConstraint(
                fields=["user", "motorcycle"], condition=models.Q(motorcycle__isnull=False), name="unique_user_moto"
            ),
        ]

    def __str__(self):
        if self.car_id:
            return f"{self.user} — {self.car}"
        return f"{self.user} — {self.motorcycle}"
