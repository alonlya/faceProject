AI人脸识别操作日志



#### 4.19

1.下载pycharm并破解(无法询问ai如何破解软件)

2.拿到人脸识别模型调用demo(python)

3.pycharm打开demo,不能运行(没有安装python运行环境)

通过chatgpt咨询发现已经安装了python环境

通过ai解决pycharm没有python运行环境问题

4.在pycharm运行人脸向量提取demo

5.编写技术方案文档

​	5.1了解技术选型,java和python优劣势对比

​	5.2了解需要完成的点(自身整理)

​	5.3了解需求背景(通过ai了解)

​	5.4整理已知的资源(自身整理)

​	5.5整理技术选型(通过ai了解技术优劣)

​	5.6各个模块设计(chatgpt生成)

​	5.7接口设计(chatgpt生成后微调)



#### 4.20

搭建flask框架,生成简单的demo,并且生成单元测试

使用agentGpt 

提示词:目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 现在有以下功能需求:1.传入人脸图片后调用接口进行人脸特征向量提取把提取到的特征向量保存到数据库中并进行人脸库管理,2.传入图片后调用人脸检测接口进行人脸检测是否有人脸,3.传入图片调用人脸特征向量提取接口提取特征向量并和数据库中的人脸特征向量对比并返回人脸相似度最高的人脸信息.基于上面的需求在开发数据库使用mysql数据库,缓存使用redis,给出一份基于python语言flask框架下的完整代码,输出的思考过程和结果除代码外都转化为中文





使用chatgpt

提示词:

我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 具体的调用方式可以参考下面的demo.现在有以下功能需求:1.传入人脸图片后调用接口进行人脸特征向量提取把提取到的特征向量保存到数据库中并进行人脸库管理,2.传入图片后调用人脸检测接口进行人脸检测是否有人脸,3.传入图片调用人脸特征向量提取接口提取特征向量并和数据库中的人脸特征向量对比并返回人脸相似度最高的人脸信息.基于上面的需求在开发数据库使用mysql数据库,缓存使用redis,给出一份基于python语言flask框架下的完整代码

以下是人脸检测接口和人脸特征向量提取接口的调用demo



#### 4月21

1.使用chatgpt生成人脸库管理接口

提示词.

我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 具体的调用方式可以参考下面的demo.现在有以下功能需求:传入人脸图片后调用接口进行人脸特征向量提取把提取到的特征向量保存到数据库中并进行人脸库管理,.基于上面的需求在开发数据库使用mysql数据库,缓存使用redis,配置使用config.py文件进行统一管理,调用接口的方法要可以复用,按照下面的接口规范,给出一份基于python语言flask框架下的代码,代码并且说明在pycharm中从0开始运行这些代码,先给出统一的配置

人脸库添加接口规范

URL：/face/add

Method：POST

请求参数：

| 参数名 | 类型   | 是否必须 | 描述           |
| ------ | ------ | -------- | -------------- |
| image  | binary | 是       | base64人脸图片 |
| name   | string | 是       | 姓名           |
| group  | string | 否       | 班组           |

返回值：

| 参数名  | 类型   | 描述     |
| ------- | ------ | -------- |
| success | bool   | 操作结果 |
| message | string | 返回信息 |

##### 

接口调用demo如下



2.代码生成一大部分,需要进行组织结构拆分,询问ai项目结构和目录

得到结果

```
app.py
├── api
│   ├── face.py
│   ├── __init__.py
├── config.py
├── model
│   ├── face_detection.py
│   ├── face_embedding.py
│   ├── __init__.py
├── service
│   ├── face.py
│   ├── __init__.py
├── utils
│   ├── __init__.py
│   ├── alignment.py
│   ├── cache.py
│   └── db.py
├── requirements.txt
├── run.py
└── README.md
```

- app.py: 程序入口文件，启动 Flask 应用。
- api: 存放 API 相关的 Python 文件。
  - face.py: 实现人脸库添加接口的 Python 文件。
  - **init**.py: 初始化 API 模块。
- config.py: 存放配置信息的 Python 文件。
- model: 存放模型相关的 Python 文件。
  - face_detection.py: 人脸检测模型的 Python 文件。
  - face_embedding.py: 人脸特征提取模型的 Python 文件。
  - **init**.py: 初始化模型模块。
- service: 存放服务相关的 Python 文件。
  - face.py: 实现人脸库添加功能的 Python 文件。
  - **init**.py: 初始化服务模块。
- utils: 存放工具相关的 Python 文件。
  - **init**.py: 初始化工具模块。
  - alignment.py: 人脸对齐工具的 Python 文件。
  - cache.py: 缓存工具的 Python 文件。
  - db.py: 数据库工具的 Python 文件。
- requirements.txt: 存放项目所需的 Python 库及其版本号。
- run.py: 启动 Flask 应用的 Python 文件。
- README.md: 项目说明文件。

人脸库接口:

我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 具体的调用方式可以参考下面的demo.现在有以下功能需求:传入人脸图片后调用接口进行人脸特征向量提取把提取到的特征向量保存到数据库中并进行人脸库管理,.基于上面的需求在开发数据库使用mysql数据库,缓存使用redis,配置使用config.py文件进行统一管理,调用接口的方法要可以复用,按照接口规范,基于python语言flask框架下,整体功能基于项目目录层级进行功能的拆分,根据项目目录层级,给出完整的代码



人脸识别接口:

我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 具体的调用方式可以参考上面的demo.接口开发按照上面的接口规范,现在有需求:传入图片后调用人脸检测接口进行人脸检测,接口返回是否有人脸,配置使用config.py文件进行统一管理,调用接口的方法要可以复用,按照接口规范,基于python语言flask框架下,整体功能基于项目目录层级进行功能的拆分,根据项目目录层级,给出功能的完整代码



封装方法:

问题出现原因:ai给出的代码差别较大,只关注业务本身,没有实现基础的功能代码

思路:进行项目架构拆分,拆分架构和功能粒度的同时,也要确定基础的功能方法模块

对于当前人脸识别项目:

目标功能

1.人脸检测

2.人脸识别

3.人脸库

基础模块:调用人脸检测接口(1,2,3),调用特征值提取接口(2,3),特征值对比方法(2)

优先级1.先实现人脸检测和特征值提取工具类

​			2.实现数据库管理,数据库设计

​			3.实现人脸库管理接口

​			4.实现特征值对比方法

​			5.实现缓存读取特征值,特征值对比业务

​			6.实现人脸识别接口

​			7.实现人脸检测接口			





工具类提示词:

我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 具体的调用方式可以参考上面的demo.需求为需要把上面的demo封装为两个方法,1.人脸检测方法 .入参为读取到的image,出参是json格式的人脸图像,  2.人脸识别方法入参是读取到的image,出参是特征向量的列表,根据以上需求使用python语言给出两个方法的完整代码



#### 4月23日

数据库设计提示词:现有人脸库管理数据库设计需求,需要保存name,group,人脸特征向量,是否逻辑删除,创建时间,修改时间,给出数据库字段设计,数据库使用mysql



人脸库管理表设计:

-- 创建表 face_database，用于保存人脸库信息
CREATE TABLE `face_database` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一ID', -- 自增长的唯一主键
  `name` varchar(255) NOT NULL COMMENT '人脸对应姓名', -- 保存人脸对应的姓名，不能为空
  `group` varchar(255) NOT NULL COMMENT '人脸所属分组', -- 保存人脸所属的分组，不能为空
  `face_feature` mediumblob NOT NULL COMMENT '人脸特征向量', -- 保存人脸特征向量的二进制数据，不能为空
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否逻辑删除', -- 用于逻辑删除，0表示未删除，1表示已删除
  `created_time` datetime NOT NULL COMMENT '创建时间', -- 记录创建时间，不能为空
  `updated_time` datetime DEFAULT NULL COMMENT '最后更新时间', -- 记录最后一次更新时间，可以为空
  PRIMARY KEY (`id`), -- 设定id为主键
  UNIQUE KEY `name_group` (`name`,`group`) -- 设定 name 和 group 组合为唯一键
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='人脸库信息'; -- 表的注释



提示词:我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的工具类,人脸检测方法为:face_detection.人脸特征向量提取方法为:face_embedding. 具体的调用方式可以参考上面的demo.具体的调用方式可以参考下面的demo.现在有以下功能需求:传入人脸图片后调用人脸特征向量提取方法把提取到的特征向量保存到数据库中并进行人脸库管理,.基于上面的需求在开发数据库使用mysql数据库,人脸库表设计如上,缓存使用redis,配置使用config.py文件进行统一管理,config代码如下个,在python的flask框架下,给出redis管理的工具类的代码和注释



提示词:在不使用sqlite数据库,根据上面的db.py的代码生成单元测试代码



提示词:是一个小白,配置统一使用config.py中的配置,config的代码如上,使用config的配置进行初始化,在python的flask框架下,给出redis管理的工具类的代码和注释



提示词:根据下面的util代码,给出一个flask框架下的单元测试代码# 导入必要的模块



在flask框架中全局都使用一个app,并且在app初始化的时候根据db.py方法创建数据库和根据cache.py方法创建redis连接,给出app.py的代码



我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的工具类,使用face_util.py的人脸特征向量提取方法:face_embedding. 现在有以下添加人脸库需求:传入人脸图片后调用人脸特征向量提取方法把提取到的特征向量保存到数据库中,保存数据库使用db.py的方法.之后把人脸特征向量保存到redis中,key为数据库表的主键,value为特征向量,缓存使用cache.py中方法,,根据下面的人添加人脸库接口规范文档,接口入参为base64格式的image,人员name,人员group,在python的flask框架下进行开发,给出实现添加人脸库功能需求的代码



把base64.b64decode返回的参数转化为cv2.imread返回的参数



face.py时提示出现下面的  File "/opt/pyProjects/flaskProject/face/libiary/face.py", line 29, in add_face
    face_id = FaceDatabaseManager.add_face(name, group, image_data)
TypeError: add_face() missing 1 required positional argument: 'feature'错误,要如何解决



人脸特征向量对比方法



详细展开说明每种人脸特征向量对比方法的优缺点以及适合的场景



特征向量维度高低的判断标准



500维的特征向量适合用那种人脸特征向量对比方法



#### 4月24



使用欧式距离特征向量对比法,特征向量为512维,基于python下进行开发,给出一个1比n人脸向量对比工具方法入参为np.array类型两个人脸特征向量,出参为对比结果小数,给出完整代码



在下面的cache.py的代码中,添加获取所有FACE_KEY_INDEX相关key的方法



我是一个小白,现在有以下人脸对比需求:传入人脸图片后调用人脸特征向量提取方法,使用face_util.py的人脸特征向量提取方法:face_embedding. 提取传入图片的特征向量,之后使用cache.py的get_all_face_keys方法遍历读取redis中的所有人脸特征向量,ridis的人脸向量key 的构造方法如(FACE_KEY_INDEX + face_id),之后使用下面compare_util.py的人脸特征向量对比的face_distance方法得到最相似度最高的人脸特征的redis,用key中的face_id去mysql中查询人脸库数据,并返回,数据库操作使用下面db.py的方法,接口格式参考下面的人脸识别接口文档,接口入参为base64格式的图片,出参返回最符合的人脸信息,在python的flask框架下进行开发,参考下面face.py中代码,给出添加实现人脸识别接口方法功能需求的代码



生成下面代码的单元测试代码,接口请求使用requests.post

4月25

补全技术方案

1.添加项目目录层级和文件

app.py
├── api
│   ├── face.py
│   ├── __init__.py
├── config.py
├── model
│   ├── face.py
│   ├── __init__.py
├── utils
│   ├── __init__.py
│   ├── face_util.py
│   ├── compare_util.py
│   ├── cache_util.py
│   └── db_util.py
├── test
│   ├── __init__.py
│   ├── compare_test.py
│   ├── cache_test.py
│   ├── face_test.py
│   ├── util_test.py
│   └── db_test.py
└── README.md

2.增加项目结构说明文档

提示词:我是一个小白,目前在已经有人脸识别接口,人脸特征向量提取接口的条件下,人脸检测接口:http://172.16.0.21:8501/v1/models/face/versions/3:predict1.人脸特征向量提取接口:http://172.16.0.21:8501/v1/models/face/versions/2:predict. 具体的调用方式可以在face_uitl.py.现在有以下功能需求:1.传入人脸图片后调用接口进行人脸特征向量提取把提取到的特征向量保存到数据库中并进行人脸库管理,2.传入图片后调用人脸检测接口进行人脸检测是否有人脸,3.传入图片调用人脸特征向量提取接口提取特征向量并和数据库中的人脸特征向量对比并返回人脸相似度最高的人脸信息.基于上面的需求在开发数据库使用mysql数据库,缓存使用redis,根据下面的项目目录层级,对各个目录和文件进行说明

3.增加AI编程方法封装顺序

4,增加项目技术选型说明



进行需求叠代:

1.增加前端界面

2.增加后台登录接口流量控制接口



人脸库数据库添加字段用来存储base64的图片

在下面的人脸库添加一个字段用来存储base64的图片,给出添加字段的sql语句

在下面db_test.py的代码中生成下面db.py代码中get_face_list方法的单元测试方法,给出测试方法的代码


现在有如下需求,数据库分页调用db.py中的分页查询方法,参考下面face.py的代码,按照人脸库分页查询接口设计文档的出入参,给出face.py中分页查询接口的代码



生成下面代码的单元测试代码,接口请求使用requests



在下面的db.py中添加一个修改人脸库数据的方法,如果当前参数没传,就不更新当前字段,在db.py中给出方法的代码 



现在有如下需求:实现一个修改人脸库数据的接口,入参参考修改人脸库数据功能接口设计文档 ,如果修改人脸库接口传入了图片数据,那么需要调用人脸特征向量提取方法face_embedding提取传入的人脸特征向量,并修改数据库中当前人员的人员向量特征和传入的参数,最后还要更新人脸特成缓存,需要在下面face.py的代码,根据下面的修改人脸库数据功能接口设计文档的请求URL,接口出入参,给出实现上述需求的方法代码



现在有如下需求:实现一个删除人脸库数据的接口,入参参考修改人脸库数据功能接口设计文档 ,如果修改人脸库接口传入了图片数据,需要在下面face.py的代码,根据下面的修改人脸库数据功能接口设计文档的请求URL,接口出入参,给出实现上述需求的方法代码