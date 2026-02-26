from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0007_motorcycle_engine_type_motorcycle_transmission"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="slug",
            field=models.SlugField(
                max_length=255,
                unique=True,
                blank=True,
                null=True,
                verbose_name="URL-имя",
            ),
        ),
        migrations.AddField(
            model_name="motorcycle",
            name="slug",
            field=models.SlugField(
                max_length=255,
                unique=True,
                blank=True,
                null=True,
                verbose_name="URL-имя",
            ),
        ),
    ]

