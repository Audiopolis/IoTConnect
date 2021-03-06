# Generated by Django 2.2 on 2019-05-10 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeideIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feide_user_id', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Feide ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=50, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_description', models.CharField(max_length=100, verbose_name="device description")),
                ('hive_manager_id', models.CharField(max_length=80, verbose_name="HiveManager identity")),
                ('psk', models.CharField(max_length=20, verbose_name='PSK')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('feide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_registrations', to='connect.FeideIdentity', verbose_name='Feide identity')),
            ],
        ),
        migrations.AlterModelOptions(
            name='feideidentity',
            options={'verbose_name_plural': 'Feide identities'},
        ),
    ]
