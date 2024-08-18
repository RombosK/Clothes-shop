# Generated by Django 4.1 on 2024-08-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True, verbose_name='Наименование категории')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/categories', verbose_name='Фото категории')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]
