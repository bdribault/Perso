# Generated by Django 2.0.5 on 2018-05-04 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CV', '0002_formation_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formation',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='company',
            name='website_link',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]