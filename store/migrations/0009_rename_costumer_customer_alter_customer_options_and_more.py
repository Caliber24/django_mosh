# Generated by Django 5.0.7 on 2024-08-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Costumer',
            new_name='Customer',
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='costumer',
            new_name='customer',
        ),
        migrations.RenameIndex(
            model_name='customer',
            new_name='store_custo_last_na_e6a359_idx',
            old_name='store_costu_last_na_66ca2f_idx',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1),
        ),
        migrations.AlterModelTable(
            name='customer',
            table='store_customers',
        ),
    ]
