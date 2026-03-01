# Generated manually

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_alter_motorcycle_moto_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_favorites', to='cars.car', verbose_name='Автомобиль')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранный автомобиль',
                'verbose_name_plural': 'Избранные автомобили',
                'db_table': 'cars_car_favorite',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MotoFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('motorcycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moto_favorites', to='cars.motorcycle', verbose_name='Мототехника')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moto_favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранная мототехника',
                'verbose_name_plural': 'Избранная мототехника',
                'db_table': 'cars_moto_favorite',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='carfavorite',
            constraint=models.UniqueConstraint(fields=('user', 'car'), name='unique_user_car_favorite'),
        ),
        migrations.AddConstraint(
            model_name='motofavorite',
            constraint=models.UniqueConstraint(fields=('user', 'motorcycle'), name='unique_user_moto_favorite'),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
