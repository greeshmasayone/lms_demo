# Generated by Django 4.1.5 on 2023-03-02 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0003_alter_user_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='point',
            field=models.PositiveSmallIntegerField(default=0, null=True, verbose_name='User Point'),
        ),
    ]
