# Generated by Django 4.0.5 on 2023-03-23 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0003_notification_case_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='image',
            field=models.ImageField(default='', upload_to='notifications'),
        ),
    ]
