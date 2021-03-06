# Generated by Django 2.0 on 2018-01-18 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BaseInfo', '0003_auto_20180112_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('material_situation', models.AutoField(primary_key=True, serialize=False, verbose_name='工程材料情况主键')),
                ('expected_scale', models.CharField(blank=True, max_length=50, verbose_name='设计量')),
                ('lis_scale', models.CharField(blank=True, max_length=50, verbose_name='LIS量')),
                ('good_arrived_scale', models.CharField(blank=True, max_length=50, verbose_name='到货量')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='信息创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='信息更新时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BaseInfo.BaseInfo')),
            ],
        ),
    ]
