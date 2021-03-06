# Generated by Django 3.0.3 on 2020-05-19 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventsP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ev_name',
            field=models.CharField(max_length=50, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_features',
            field=models.CharField(blank=True, max_length=40000, null=True, verbose_name='Особенности'),
        ),
        migrations.AlterField(
            model_name='room',
            name='features',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='id_event',
            field=models.ForeignKey(db_column='id_event', on_delete=django.db.models.deletion.CASCADE, to='EventsP.Event', verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='id_person_post',
            field=models.ForeignKey(db_column='id_person_post', on_delete=django.db.models.deletion.CASCADE, to='EventsP.PersonWithPost', verbose_name='Человек + Должность'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='place',
            field=models.ForeignKey(blank=True, db_column='id_place', null=True, on_delete=django.db.models.deletion.CASCADE, to='EventsP.Place', verbose_name='Место'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='team',
            field=models.ForeignKey(blank=True, db_column='id_team', null=True, on_delete=django.db.models.deletion.CASCADE, to='EventsP.Team', verbose_name='Команда'),
        ),
    ]
