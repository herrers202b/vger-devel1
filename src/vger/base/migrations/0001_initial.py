# Generated by Django 3.1.7 on 2021-03-25 01:01

import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleOfCategory', models.CharField(help_text='Please enter a title for this category, ex) Computer Skills.', max_length=100)),
                ('lowWeightText', models.CharField(default='Not like me at all', help_text='Please enter flavor text for the low weight of the category, ex) Not like me at all', max_length=50)),
                ('highWeightText', models.CharField(default='Extremely like me', help_text='Please enter flavor text for the high weight of the category, ex) Extremely like me', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleOfSurvey', models.CharField(help_text='Please enter a name for the survey', max_length=50)),
                ('directions', models.CharField(help_text='Please enter any directions to take the survey', max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('assigned', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_hash', models.CharField(default=base.models.SurveyInstance.create_session_hash, max_length=40, unique=True)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionText', models.CharField(help_text='Please enter a prompt. ex) I know how to install software on my computer.', max_length=100)),
                ('answer', models.IntegerField(blank=True, choices=[(0, 'weight 0'), (1, 'weight 1'), (2, 'weight 2'), (3, 'weight 3'), (4, 'weight 4')], help_text='Results of question', null=True)),
                ('questionNumber', models.IntegerField(default='1', help_text='Please enter a question number')),
                ('category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='base.category', verbose_name='Parent Category')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='survey',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='base.survey', verbose_name='Parent Survey'),
        ),
    ]
