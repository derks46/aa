# Generated by Django 2.0.10 on 2019-01-16 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autostickrapp', '0003_auto_20190116_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='marca',
            name='id',
            field=models.AutoField(auto_created=True, default=2, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='emblema',
            name='marca',
        ),
        migrations.AddField(
            model_name='emblema',
            name='marca',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='autostickrapp.Marca', to_field='nombre'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='marca',
            name='nombre',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
