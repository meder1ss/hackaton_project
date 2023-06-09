# Generated by Django 4.2.1 on 2023-05-16 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackaton_main', '0002_task_language_alter_task_input'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
