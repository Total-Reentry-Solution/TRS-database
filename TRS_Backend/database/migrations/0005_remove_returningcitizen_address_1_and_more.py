# Generated by Django 4.1.13 on 2024-03-05 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_rename_mdoc_returningcitizen_mdoc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returningcitizen',
            name='address_1',
        ),
        migrations.RemoveField(
            model_name='returningcitizen',
            name='address_2',
        ),
        migrations.RemoveField(
            model_name='returningcitizen',
            name='city',
        ),
        migrations.RemoveField(
            model_name='returningcitizen',
            name='state',
        ),
        migrations.RemoveField(
            model_name='returningcitizen',
            name='zip_code',
        ),
        migrations.AlterField(
            model_name='returningcitizen',
            name='date_activated',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ParoleAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('returning_citizen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paroleAddress', to='database.returningcitizen')),
            ],
        ),
    ]
