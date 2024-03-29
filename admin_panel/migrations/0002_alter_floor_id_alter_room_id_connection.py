# Generated by Django 4.1 on 2024-01-21 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('from_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_from', to='admin_panel.room')),
                ('to_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_to', to='admin_panel.room')),
            ],
            options={
                'db_table': 'connection',
                'unique_together': {('from_room', 'to_room')},
            },
        ),
    ]
