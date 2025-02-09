# Generated by Django 5.0.3 on 2024-04-10 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0009_essay_submitter'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawEssays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(max_length=50, upload_to='', verbose_name='文件名')),
                ('file', models.FileField(upload_to='RawEssays/', verbose_name='文件')),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
            ],
            options={
                'verbose_name': '上传作文文件',
                'verbose_name_plural': '上传作文文件',
                'db_table': 'RawEssays',
            },
        ),
        migrations.AlterField(
            model_name='essay',
            name='submitter',
            field=models.IntegerField(verbose_name='作文提交者'),
        ),
    ]
