import re

from paddleocr import PaddleOCR
import fitz
import win32com.client
import glob
import os
import jieba

class OCRrecognition:
    def __init__(self):
        self.PdOCR = PaddleOCR(use_angle_cls=True)
    def ocr(self, img_path):
        try:
            print("====OCR START====")
            result = self.PdOCR.ocr(img_path, cls=True)
            return result
        except Exception as e:
            print("In OCRrecognition class -> ocr function:", e)
            return []

def change_word_to_txt(word_path, save_path):
    print('读取'+word_path)
    word = win32com.client.Dispatch('Word.Application')  # 调用word应用import pythoncom
    doc = word.Documents.Open(word_path)
    print('保存中。。。')
    doc.SaveAs(save_path, 2)  # 保存格式为txt
    doc.Close()
    word.Quit()

def pdf2img(pdf_path, img_path):
    pdfDoc = fitz.open(pdf_path)
    for page in pdfDoc:
        # 将页面转换为图片
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72
        # pix = page.get_pixmap()
        zoom_x = 1.33333333
        zoom_y = 1.33333333
        # (1.33333333-->1056x816)   (2-->1584x1224)  (3-->3572x2526)
        # x和y的值越大越清晰，图片越大，但处理也越耗时间，这里取决于你想要图片的清晰度
        # 默认为1.333333，一般日常使用3就够了，不能设置太大，太大容易使电脑死机
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat, dpi=None, colorspace='rgb', alpha=False)
        imageName = pdf_path.split("\\")[len(pdf_path.split("\\")) - 1]
        target_img_name = img_path + '\\%s%i.png' % (imageName,page.number)   # 构造图片名字
        # 保存图片
        pix.save(target_img_name)

def txt2string(file):
    with open(file, "r") as f:  # 打开文件
        data = f.read()  # 读取文件
        return data

def next_png(path):
    for i in glob.glob(path+'*.png'):
        yield i

def delete_files(directory):
    file_list = os.listdir(directory)
    for file in file_list:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def para_count(str):
    para = str.split('\n')
    return len(para)

def en_word_count(str):
    content = str.split(' ')
    word_list = []
    for w in content:
        word_list.append(w)
    wc = len(word_list)
    if wc > 200:
        grade = 100
    if 150 < wc < 200:
        grade = 90
    if 120 < wc < 150:
        grade = 80
    if 90 < wc < 120:
        grade = 70
    if wc < 90:
        grade = 60
    return grade

def zh_word_count(str):
    content = jieba.lcut(str)
    word_list = []
    for w in content:
        word_list.append(w)
    wc = len(word_list)
    if wc > 650:
        grade = 100
    if 600 < wc < 650:
        grade = 90
    if 550 < wc < 600:
        grade = 80
    if 500 < wc < 550:
        grade = 70
    if wc < 500:
        grade = 60
    return grade

def zh_word(str):
    word=re.findall('([\u4e00-\u9fa5])', str)
    words = len(word)
    if words > 800:
        grade = 100
    if 700 < words < 750:
        grade = 90
    if 650 < words < 700:
        grade = 80
    if 600 < words < 650:
        grade = 70
    if words < 600:
        grade = 60
    return grade

def en_word(str):
    words = len(str)
    grade = 0
    if words>200:
        grade = 100
    if 150<words<200:
        grade = 90
    if 100<words<150:
        grade = 80
    if 80<words<100:
        grade = 70
    if words<80:
        grade = 60
    return grade