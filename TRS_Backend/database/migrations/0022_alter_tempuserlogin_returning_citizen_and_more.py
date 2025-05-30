# Generated by Django 4.1.13 on 2024-03-14 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_threedailyactions_date_only'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempuserlogin',
            name='returning_citizen',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp_user', to='database.returningcitizen'),
        ),
        migrations.CreateModel(
            name='TempParoleOfficerLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=6, unique=True)),
                ('valid_until', models.DateField()),
                ('parole_officer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp_paroleOfficer', to='database.paroleofficer')),
            ],
        ),
        migrations.CreateModel(
            name='TempMentorLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=6, unique=True)),
                ('valid_until', models.DateField()),
                ('mentor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp_mentor', to='database.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='ApiKeyForParoleOfficer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(max_length=100)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apiKey_po', to='database.paroleofficer')),
            ],
        ),
        migrations.CreateModel(
            name='ApiKeyForMentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(max_length=100)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apiKey_m', to='database.mentor')),
            ],
        ),
    ]
