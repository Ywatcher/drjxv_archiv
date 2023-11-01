# Drjxu Archiv
知-乎-爬-取-与-存-档-程-序


## 功能
该项目使用 selenium 模拟浏览器提取问题和回答信息，并在本地
存档，以及记录它们的版本；由于使用模拟浏览器的方式，它的效
率并不支持用于爬取用于大数据分析的材料；但您可以使用它相对高效且有条理地记录您的阅读。<br>
问题和答案，以及它们的历史版本使用 sqlite3 关系型数据库进行
管理；不久将对多份分别管理的存档的合并进行实现；


git log 管理版本:
![version_through_git_log](https://github.com/Ywatcher/drjxv_archiv/assets/93801008/de7efcd1-6bcd-4205-b1ab-70829fc83da0)

在 obsidian 中查看回答：
![obsidian_view](https://github.com/Ywatcher/drjxv_archiv/assets/93801008/aa012551-6b3c-491f-8734-9204bd7b1172)


## 环境依赖
该项目基于 python, 关键依赖如下：
```
beautifulsoup4==4.12.2
GitPython==3.1.40
PyYAML==6.0.1
selenium==2.52.0
ipykernel==6.25.1 # 如果你要使用 jupyter
```
详细依赖请见`requirements.txt`。<br>
注意：其中 selenium 的版本要求较为严格，这里使用的是旧版；
由于使用最新版 (4.14.0; 4.15.0) 时出现了一些尚难以解决的错
误，且 selenium 在更新时涉及兼容性的改动较多同时没有及时针
对改动更新文档，因此使用了相对稳定的旧版本；<br>
这里使用的旧版本是 2.52.0，这一版本不在 conda 源中，建议使
用 pip 安装这一依赖；

## 使用前的准备
除了安装 python 环境依赖，还需要：
- 安装 git
- 准备 webdriver
- 在 `src/config.py` 中作必要的配置，以使得程序可以找到您
	电脑的路径，以及其他 

#### 安装 git 
git 是一个版本管理工具，这个项目使用它的 python binding，
以实现网络内容的版本管理；如果您还没有安装
git，请在您的计算机上安装它；

#### 准备 webdriver
各大浏览器都有相应的 webdriver，这是一个可执行程序，以可
调试的方式运行浏览器；selenium 通过运行 webdriver 来查看网
站；<br>
可以参考[链接](https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location/#download-the-driver)
进行下载

#### 在 `src/config.py` 中作必要的配置
必要配置为修改字典 `drivers` 中的 webdriver 路径为其真实所
在路径；其他配置请见[自定义](#自定义)

## 使用方法
使用命令行调用 python 脚本: <br>
正在实现
使用 jupyter notebook:<br>
- 运行 `src/controller.ipynb` 

## 项目结构
```
.
├── README.md
└── src
    ├── common.py  # 通用的数据类型
    ├── config.py  # 配置
    ├── controller.ipynb  # 程序 jupyter 入口
    ├── controller.py     # 程序 .py 入口
    ├── data_handler      # 管理数据的部分
    │   ├── database.py   # 数据库操作
    │   ├── initialization.py  # 创建仓库
    │   ├── __init__.py   
    │   ├── master.py     # 协调数据库与 git
    │   └── vcs.py        # git 操作
    ├── util              # 工具函数
    │   ├── db.py
    │   ├── file_rendering.py
    │   ├── logger.py
    │   ├── time.py
    │   └── web_util.py
    └── web_parser        # 爬取部分
        ├── answer_parser.py  # 答案爬取器
        ├── __init__.py   
        └── question_parser.py # 问题爬取器

```
该项目分为两个主要部分，分别是爬取部分和管理部分；<br>
其中爬取部分分为问题爬取器和答案爬取器，每个爬取器对象
会使用一个 webdriver 并单独占据一个进程，在爬取时会使用
进程队列`multiprocess.Queue`进行通信；这其中涉及两个队列
————一个任务队列和一个结果队列；
问题爬取器会把当前问题下的回答简要信息送入任务队列，回答
爬取器会根据它查找回答；
问题爬取器和回答爬取器爬取当前问题/回答本身的信息后都会将
这些信息送入结果队列，这些内容将由管理数据的部分处理，并
根据它们更新仓库；<br>
仓库的主要部分包括一个 sqlite3 数据库，和一个 git 仓库；
问题和回答的富文本，以及它们的 metadata 会组织成 markdown
的形式写入文件并由 git 提交。每次提交都对应一个单独的文件
的更新。<br>
数据库中由五张表，分别包括问题，问题版本，回答，回答版本，
以及当前的 git head；git head 以及各版本的 hexsha 会被存入
数据库.


## 自定义
在 `src/config.py` 中进行配置；<br>
**您的提交标识：**该项目的存档是设计为由个人管理，并可
以互相合并；当合并者众多后，爬取的来源和可靠性可能
会变得混杂而使整个大存档的置信度降低；您可以通过在
填充自己的存档时标记来源，来增加辨识度；
```python
# 这部分将作为 git 提交时的 commiter 信息，用于标
# 识内容的记录者；同时，所爬取的回答的作者将作为
# git 提交时的 author 的信息；
default_owner_name = "me" # 修改为您的昵称
default_owner_email = "me@email" # 修改为您的邮箱
```
**回答爬取器的进程数量：**该项目使用多个进程同时爬取
问题和回答，目前已经实现支持的是单个问题爬取进程和
多个回答爬取进程；
```python
nr_answer_parsers = 3  # 修改回答进程的数量
# 总共的进程数为 2 + nr_answer_parsers,
# 除此之外还有一个问题爬取进程和一个读取爬取结果并
# 写入存档进程
```
## TODO:
 - [ ] 改为使用事件在爬取与存档进程间通信 
 - [ ] 存档合并的实现
 - [ ] 对操作失败需要回退情形的测试
 - [x] 滚动读取
 - [ ] 支持 xpath 的配置，加强可拓展性
 - [ ] 为存档 Master 设置 logger
 - [ ] 存储图片
 - [ ] 创建用于保存评论的 table 并读取评论 
 - [ ] 设置更加完善的滚动策略，并提供配置
