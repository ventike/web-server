# Generated by Django 5.0.6 on 2024-06-29 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_partner_image_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='message_title',
            field=models.TextField(null=True),
        ),
    ]
