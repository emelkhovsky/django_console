# Generated by Django 2.2.4 on 2019-09-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ipdata_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_username', models.CharField(blank=True, max_length=50)),
                ('ip_ip', models.CharField(blank=True, max_length=15)),
                ('ip_user', models.CharField(blank=True, max_length=50)),
                ('ip_password', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'db_table': 'IP_DB',
                'managed': True,
            },
        ),
    ]