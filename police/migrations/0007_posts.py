# Generated by Django 4.0.5 on 2023-04-11 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0006_alter_register_case_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senderPolice', models.CharField(max_length=255)),
                ('receiverPolice', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('govid', models.CharField(max_length=255)),
            ],
        ),
    ]
