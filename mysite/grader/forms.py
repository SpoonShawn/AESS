from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Essay
from .models import RawEssays
from .models import Chinese


# 用户注册表单
class UserCustomRegister(UserCreationForm):
    name = forms.CharField(required=False, max_length=50)
    cate = forms.BooleanField(required=True)
    faculty = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',
                  'name', 'cate', 'faculty')

# 用户修改信息表单
class UserCustomChange(UserChangeForm):
    name = forms.CharField(required=False, max_length=50)

    class Meta:
        model = User
        fields = ('email', 'password', 'name')

class UserRegister(UserCreationForm):
    name = forms.CharField(required=False, max_length=50)
    cate = forms.BooleanField(required=True)
    faculty = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'name', 'cate', 'faculty']

class UserUpdate(UserChangeForm):
    name = forms.CharField(required=False, max_length=50)

    class Meta:
        model = User
        fields = ['email', 'password', 'name']

class AnswerForm(forms.ModelForm):
    answer = forms.CharField(label='作文内容', max_length=100000,
                             widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "请输入作文内容"}))

    class Meta:
        model = Essay
        fields = ['answer']

class RawEssaysForm(forms.ModelForm):
    class Meta:
        model = RawEssays
        fields = ('file',)

        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["txt", "doc", "docx", "pdf", "jpg", "jpeg", "png"]:
            raise forms.ValidationError("请上传txt, doc/docx, pdf, jpg, jpeg 以及 png 格式的文件")
        return file

class ChineseForm(forms.ModelForm):
    title = forms.CharField(label='作文题目', max_length=100,
                              widget=forms.Textarea(attrs={'rows': 1, 'placeholder': "请输入作文内容"}))
    content = forms.CharField(label='作文内容', max_length=100000,
                              widget=forms.Textarea(attrs={'rows': 10, 'placeholder': "请输入作文内容"}))

    class Meta:
        model = Chinese
        fields = ['title', 'content']