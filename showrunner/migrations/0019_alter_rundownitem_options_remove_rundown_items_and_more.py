# Generated by Django 4.0.4 on 2022-04-20 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showrunner', '0018_rundown_rundownitem_rundownitemsthroughmodel_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rundownitem',
            options={'ordering': ('rundown', 'order')},
        ),
        migrations.RemoveField(
            model_name='rundown',
            name='items',
        ),
        migrations.AddField(
            model_name='rundownitem',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rundownitem',
            name='rundown',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='showrunner.rundown'),
        ),
        migrations.DeleteModel(
            name='RundownItemsThroughModel',
        ),
    ]
