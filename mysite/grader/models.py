import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CommonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('用户名',blank=True,max_length=50)
    cate = models.BooleanField('是否学生',default=False)
    faculty = models.CharField('院系',blank=True,max_length=20,default='undefine')

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)

class Question(models.Model):
    """ A model of the 8 questions. """
    question_title = models.TextField(max_length=100000, verbose_name='英文作文题目')
    set = models.IntegerField(unique=True, verbose_name='作文集序号')
    min_score = models.IntegerField(verbose_name='最低分')
    max_score = models.IntegerField(verbose_name='作文分值')

    def update_content(self):
        if len(str(self.question_title)) > 35:
            return '{}...'.format(str(self.question_title)[0:35])
        else:
            return self.question_title
    update_content.short_description = '英文作文题目'

    class Meta:
        verbose_name = '英文作文题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.set)

class Essay(models.Model):
    """ Essay to be submitted. """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='作文题号')
    content = models.TextField(max_length=100000, verbose_name='作文内容')
    score = models.IntegerField(null=True, blank=True, verbose_name='作文得分')
    submitter = models.IntegerField(null=False, verbose_name='作文提交者')
    date = models.DateTimeField('上传时间', auto_now_add=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        verbose_name = '用户提交英文作文'
        verbose_name_plural = verbose_name

class Chinese(models.Model):
    title = models.TextField(max_length=100, verbose_name='作文题目')
    content = models.TextField(max_length=100000, verbose_name='作文内容')
    logic_score = models.IntegerField(null=True, blank=True, verbose_name='连贯度')
    topic_score = models.IntegerField(null=True, blank=True, verbose_name='切题度')
    submitter = models.IntegerField(null=False, verbose_name='作文提交者')
    date = models.DateTimeField('上传时间', auto_now_add=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        verbose_name = '用户提交中文作文'
        verbose_name_plural = verbose_name

class Doc(models.Model):
    file_name = models.CharField('文件名字', max_length=50)
    file_obj = models.FileField('文件', upload_to='files/')
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = 'doc'
        verbose_name = '相关文件信息表'
        verbose_name_plural = verbose_name

class RawEssays(models.Model):
    file_name = models.FileField('文件名', max_length=50)
    file = models.FileField('文件', upload_to='RawEssays/')
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = 'RawEssays'
        verbose_name = '上传作文文件'
        verbose_name_plural = verbose_name


