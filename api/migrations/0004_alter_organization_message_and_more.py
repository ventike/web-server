# Generated by Django 5.0.6 on 2024-06-26 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_resource_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='message_icon',
            field=models.IntegerField(null=True),
        ),
    ]