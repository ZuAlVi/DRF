# Generated by Django 5.0.1 on 2024-02-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_remove_subscription_is_subscribed_course_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]
