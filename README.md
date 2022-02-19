# NEUWaterNet
python, html, css, javascript, flask, bootstrap

### 使用说明

- 需要新建一个数据库，然后新建一个schema，右键schema选择 run SQL Script，选择我文件中的web_work.sql文件，这样就成功导入数据库的相关数据了。我是使用的是MYSQL。

- 在Terminal中输入`app.py runserver`，用于启动项目

### 文件介绍

本项目分为多个文件，保存不同的部分。

#### migrations

文件夹为建立数据库时自动生成，保存着数据库中的历史缓存。

#### project

- \__init\__.py：建立python模块时自动生成，用于初始化python模块，用于创建app,并和app.py文件建立联系
- model.py：用于建立数据库模型
- view.py：保存着绝大部分的视图函数，用来实现网页的后端功能。

#### static

- image：文件夹中保存网页中所有使用到的图片
- echarts.js：从Apache ECharts网站上下载得到，用于可视化数据中图标的js代码
- mystyle.css：css代码

#### templates

- base.html：父模板
- user：子模板，保存着网页中所有的前端页面

#### app.py：初始化app

#### settings.py：配置文件，用于连接数据库等等配置。
