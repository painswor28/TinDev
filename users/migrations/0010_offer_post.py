# Generated by Django 4.0.5 on 2022-12-02 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.post'),
            preserve_default=False,
        ),
    ]
