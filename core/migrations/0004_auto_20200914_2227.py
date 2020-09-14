# Generated by Django 3.1.1 on 2020-09-14 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_scraped_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListedSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
