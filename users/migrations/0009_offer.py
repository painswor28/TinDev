# Generated by Django 4.0.5 on 2022-12-02 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_post_interested_candidates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=7)),
                ('expiration_date', models.DateField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.candidate')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.recruiter')),
            ],
        ),
    ]