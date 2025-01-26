# Automated Essay Scoring System自动作文评分系统
> 基于深度学习和大模型的中英文自动作文评分分析系统

英文数据集来自Kaggle的[Hewlett Foundation - Essay scoring](https://www.kaggle.com/code/mpwolke/hewlett-foundation-essay-scoring)。

中文数据集参考了[cubenlp/CEDCC_corpus](https://github.com/cubenlp/CEDCC_corpus)以及[cnunlp/Chinese-Essay-Dataset-For-Organization-Evaluation: A Chinese argumentative student essay dataset for Organization Evaluation and Discourse Element Identification](https://github.com/cnunlp/Chinese-Essay-Dataset-For-Organization-Evaluation)

**mysite** 文件夹包含了基于Django的Web应用，运行manage.py并使用**venu**文件夹中的解释器即可在本地进行测试。





## 环境配置
- 环境配置已在**venu**文件夹中配置好，本地运行时选择**venu**中的解释器即可运行。



## 主要内容
- 系统登录界面

![image-20250125213929997](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125213929997.png)

`Web应用入口。`

* 用户登录界面

![image-20250125214117872](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125214117872.png)

`已注册用户账号：20201108	密码：szx12345`

`也可自行注册用户测试。`

* 作文评分页面

![image-20250125214354131](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125214354131.png)

![image-20250125214714345](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125214714345.png)

* 支持文件上传及OCR

![image-20250125214839893](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125214839893.png)

`OCR实例测试`

* 评分可视化呈现

![image-20250125215025983](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125215025983.png)

* 后端管理系统

![image-20250125215117929](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125215117929.png)

`默认用户：admin 密码：123456`

![image-20250125215211350](https://github.com/SpoonShawn/AESS/blob/master/img/image-20250125215211350.png)

`登录后可实现后端管理`
