# Generated by Django 2.2.9 on 2020-11-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20201024_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('selling', 'Selling'), ('buying', 'Buying')], default='selling', max_length=255),
        ),
    ]
