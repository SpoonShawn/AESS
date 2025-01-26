import datetime
import json
import requests
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db import connection
from django.db.models import Q, Count
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import escape_uri_path

from .models import *
from .forms import AnswerForm,UserCustomRegister,UserCustomChange,RawEssaysForm,ChineseForm

from .utils.model import *
from .utils.helpers import *
from .utils.file2text import *
import glob

import os
current_path = os.path.abspath(os.path.dirname(__file__))

# Create your views here.
def loging(request):
    return render(request,'login.html')

def userlogin(request):
    if request.method == 'POST':
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'userlogin.html',{'error':'用户不存在或密码错误!'})
        else:
            login(request, user)
            return redirect('grader:index')
    else:
        return render(request,'userlogin.html')

def userlogout(request):
    logout(request)
    return redirect('grader:login')

def register(request):
    if request.method == 'POST':
        registerForm = UserCustomRegister(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            newUser = authenticate(username=registerForm.cleaned_data['username'],password=registerForm.cleaned_data['password1'])
            newUser.email = registerForm.cleaned_data['email']
            CommonUser(user=newUser,name=registerForm.cleaned_data['name'],
                cate=registerForm.cleaned_data['cate'],
                faculty=registerForm.cleaned_data['faculty']).save()
            login(request,newUser)
            return redirect('grader:index')
    else:
        registerForm = UserCustomRegister
    content = {'registerForm':registerForm}
    return render(request,'register.html',content)

# 用户查看个人信息，需要先登录
@login_required(login_url='grader:login')
def userCentre(request):
    # 修改个人信息
    if request.method == 'POST':
        changeForm = UserCustomChange(request.POST, instance=request.user)
        if changeForm.is_valid():
            changeForm.save()
            request.user.commonuser.name = changeForm.cleaned_data['name']
            request.user.commonuser.save()
    else:
        pass
    changeForm = UserCustomChange()
    content = {'currentUser': request.user, 'changeForm': changeForm}
    return render(request, 'userCentre.html', content)

# 用户修改密码
@login_required(login_url='grader:login')
def changePassword(request):
    if request.method == 'POST':
        changepasswordForm = PasswordChangeForm(data=request.POST, user=request.user)
        if changepasswordForm.is_valid():
            changepasswordForm.save()
            return redirect('grader:userlogin')
    else:
        pass
    changepasswordForm = PasswordChangeForm(user=request.user)
    content = {
        'currentUser': request.user,
        'changepasswordForm': changepasswordForm
    }
    return render(request, 'changePassword.html', content)

# 用户信息界面
def userInfo(request):
    return render(request, 'usr_info.html')

def index(request):
    questions_list = Question.objects.order_by('set')
    context = {
        'questions_list': questions_list,
    }
    return render(request, 'grader/index.html', context)

def essay(request, question_id, essay_id):
    essay = get_object_or_404(Essay, pk=essay_id)
    enessay = essay.content
    wcount = en_word_count(enessay)
    pcount = para_count(enessay)
    words = en_word(enessay)
    context = {
        "essay": essay,
        'wcount': wcount,
        'pcount': pcount,
        'words': words,
    }
    return render(request, 'grader/essay.html', context)

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnswerForm(request.POST)

        if form.is_valid():

            content = form.cleaned_data.get('answer')

            if len(content) > 20:
                num_features = 300
                model = word2vec.KeyedVectors.load_word2vec_format(os.path.join(current_path, "deep_learning_files/word2vec.bin"), binary=True)
                clean_test_essays = []
                clean_test_essays.append(essay_to_wordlist( content, remove_stopwords=True ))
                testDataVecs = getAvgFeatureVecs( clean_test_essays, model, num_features )
                testDataVecs = np.array(testDataVecs)
                testDataVecs = np.reshape(testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1]))

                lstm_model = get_model()
                lstm_model.load_weights(os.path.join(current_path, "deep_learning_files/final_lstm.h5"))
                preds = lstm_model.predict(testDataVecs)

                if math.isnan(preds):
                    preds = 0
                else:
                    preds = np.around(preds)

                if preds < 0:
                    preds = 0
                if preds > question.max_score:
                    preds = question.max_score
            else:
                preds = 0

            K.clear_session()
            essay = Essay.objects.create(
                content=content,
                question=question,
                score=preds,
                submitter=request.user.id
            )
        return redirect('grader:essay', question_id=question.set, essay_id=essay.id)
    else:
        form = AnswerForm()

    context = {
        "question": question,
        "form": form,
    }
    return render(request, 'grader/question.html', context)

# 关于界面，只接受get请求
def about(request):
    if request.method == 'GET':
        docList = Doc.objects.all()  # 文件信息
        return render(request, 'about.html', locals())

# 文件资料下载
def download_file(request, doc_id):
    # 获取资料信息用户显示
    if request.method == 'GET':
        file_result = Doc.objects.filter(id=doc_id)
        if file_result:
            file = list(file_result)[0]
            ip = 'http://127.0.0.1:8000/media/'
            path = ip + str(file.file_obj)

            # 下载资料
            try:
                response = FileResponse(requests.get(path, stream=True))
            except requests.exceptions.ConnectionError as e:
                response.status_code = '链接请求失败'
            file_ext = path.split(".")[-1]
            if not file_ext:
                pass
            else:
                file_ext = file_ext.lower()
            response['Content-Type'] = 'application/octet-stream'
            FileName = escape_uri_path(path).split('/')[-1]
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(FileName)
            return response
        else:
            return HttpResponse("文件不存在")

def file2txt(request):
    result = ''
    if request.method == "POST":
        form = RawEssaysForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
        filepath = path + "/media/RawEssays/"
        filename = os.listdir(filepath)[0]
        ext = filename.split('.')[-1].lower()
        if ext not in ["txt", "doc", "docx", "pdf", "jpg", "jpeg", "png"]:
            result = '请上传txt, doc/docx, pdf, jpg, jpeg, png类型的文件！'
        else:
            if ext == 'txt':
                result = txt2string(filepath+filename)
            if ext in ['doc', 'docx']:
                readpath = filepath+filename
                savepath = filepath+"res.txt"
                change_word_to_txt(readpath,savepath)
                result = txt2string(savepath)
            if ext in ["jpg", "jpeg", "png"]:
                ocr = OCRrecognition()
                res = ocr.ocr(filepath+filename)[0]
                for item in res:
                    item = item[1][0]
                    result += item + '\n'
            if ext == 'pdf':
                pdf_path = filepath+filename
                img_path = filepath
                pdf2img(pdf_path,img_path)
                pdf2img(pdf_path,img_path)
                ocr = OCRrecognition()
                for i in next_png(img_path):
                    res = ocr.ocr(i)[0]
                    for item in res:
                        item = item[1][0]
                        result += item + '\n'
        delete_files(filepath)
    else:
        form = RawEssaysForm()

    return render(request, 'grader/file2txt.html', {'form': form,
                                                    'result': result,})
def chinese(request):
    if request.method == 'POST':
        form = ChineseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            chinese = Chinese.objects.create(
                title=title,
                content=content,
                logic_score=100,
                topic_score=100,
                submitter=request.user.id
            )
        return redirect('grader:zhessay', chinese_id=chinese.id)
    else:
        form = ChineseForm()
    context = {
        "form":form,
    }
    return render(request, 'grader/chinese.html', context)

def zhessay(request, chinese_id):
    essay = get_object_or_404(Chinese, pk=chinese_id)
    zhessay = essay.content
    wcount = zh_word_count(zhessay)
    pcount = para_count(zhessay)
    words = zh_word(zhessay)
    context = {
        "essay": essay,
        'wcount': wcount,
        'pcount': pcount,
        'words': words,
    }
    return render(request, 'grader/zhessay.html', context)