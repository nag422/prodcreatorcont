# Generated by Django 3.0.5 on 2021-03-22 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0007_productassigns'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgroup',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='products', to='quizz.Content'),
        ),
    ]
