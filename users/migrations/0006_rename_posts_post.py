# Generated by Django 4.0.5 on 2022-11-30 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_posts_creator'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]