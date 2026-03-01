# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_motorcycle_alter_car_table_car_photo_moto_photo_and_more'),
        ('evaluations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('phone', models.CharField(max_length=50, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('application_type', models.CharField(choices=[('покупка', 'Покупка'), ('консультация', 'Консультация'), ('кредит', 'Кредит'), ('трейд-ин', 'Трейд-ин'), ('обратный_звонок', 'Обратный звонок')], max_length=50, verbose_name='Тип заявки')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_applications', to='cars.car', verbose_name='Автомобиль')),
            ],
            options={
                'verbose_name': 'Заявка на автомобиль',
                'verbose_name_plural': 'Заявки на автомобили',
                'db_table': 'evaluations_car_application',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MotoApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('phone', models.CharField(max_length=50, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('application_type', models.CharField(choices=[('покупка', 'Покупка'), ('консультация', 'Консультация'), ('кредит', 'Кредит'), ('трейд-ин', 'Трейд-ин'), ('обратный_звонок', 'Обратный звонок')], max_length=50, verbose_name='Тип заявки')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('motorcycle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moto_applications', to='cars.motorcycle', verbose_name='Мототехника')),
            ],
            options={
                'verbose_name': 'Заявка на мототехнику',
                'verbose_name_plural': 'Заявки на мототехнику',
                'db_table': 'evaluations_moto_application',
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Application',
        ),
    ]
