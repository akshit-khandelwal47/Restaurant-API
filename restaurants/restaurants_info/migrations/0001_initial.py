# Generated by Django 4.2.1 on 2023-05-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='storestatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]