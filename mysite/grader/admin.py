from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from simpleui.admin import AjaxAdmin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from .models import *


# question import export settings
class CommonUserInline(admin.TabularInline):
    model = CommonUser
    can_delete = False
    verbose_name = '用户信息表'
    verbose_name_plural = verbose_name

class UserAdmin(BaseUserAdmin):
    inlines = (CommonUserInline,)

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        import_id_fields = ['set']
        fields = ['id', 'question_title', 'max_score', 'min_score']
        export_order = ['id', 'question_title', 'max_score', 'min_score']

class QuestionAdmin(ImportExportActionModelAdmin, AjaxAdmin):
    resource_class = QuestionResource
    list_display = ['id', 'update_content', 'max_score']
    list_editable = ['max_score']
    list_per_page = 10
    search_fields = ['question_title']
    list_display_links = ['update_content']
    ordering = ['id']

class EssayAdmin(ImportExportActionModelAdmin, AjaxAdmin):
    list_display = ['submitter', 'question', 'content', 'score', 'date']
    list_per_page = 5
    ordering = ['date']

class DocAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'file_obj', 'upload_time']
    list_per_page = 5
    ordering = ['-upload_time']

class ZhEssaysAdmin(ImportExportActionModelAdmin, AjaxAdmin):
    list_display = ['submitter', 'title', 'content', 'logic_score', 'topic_score', 'date']
    list_per_page = 5
    ordering = ['date']


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Doc, DocAdmin)
admin.site.register(Chinese, ZhEssaysAdmin)

admin.site.site_header = 'AES作文评分管理系统'
admin.site.site_title = 'AES作文评分管理系统'
admin.site.index_title = 'AES作文评分管理系统'
