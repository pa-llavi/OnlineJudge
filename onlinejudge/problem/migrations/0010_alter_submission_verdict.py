# Generated by Django 3.2.7 on 2021-09-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0009_alter_submission_verdict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='verdict',
            field=models.CharField(choices=[('TT', 'testing'), ('AC', 'accepted'), ('WA', 'wrong answer'), ('TLE', 'time limit exceeded'), ('RE', 'runtime error')], default='TT', max_length=3),
        ),
    ]