# 环境
* python 3.7
* pygame 安装：  
  ** ``pip install wheel``
  ** https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame 下载 ``pygame‑1.9.3‑cp37‑cp37m‑win_amd64.whl``包
  ** ``python -m pip install --user pygame‑1.9.3‑cp37‑cp37m‑win_amd64.whl``安装下载 的pygame whl包

# 项目笔记
## 创建入口文件 `alien_invasion.py`
## 创建设置文件 `settings.py`，定义设置类 `Settings`
## 创建 `Ship` 类

## 创建 `game_functions`模块，避免`alien_invasion`文件代码过长

## 在`game_functions`中创建飞船移动的操作代码

## 给飞船添加射击功能shotting，并且创建子弹类 `Bullet`

## 创建 `Alien` 类
* 创建多行外星人
* 外星人左右移动，移动到边缘向下移动
* 检查外星人与子弹碰撞
* 检查外星人与飞船碰撞

## 新建统计跟踪游戏信息的类 `GameStats`

## 创建开始游戏按钮，并且提供重置游戏的功能
## 游戏等级设置
## 实现计分显示

## todo:显示等级和剩余飞船数
