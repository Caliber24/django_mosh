# Generated by Django 5.0.7 on 2024-08-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_alter_taggeditem_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
