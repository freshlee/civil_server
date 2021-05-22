# sql的statement拆解功能技术选型调研

## 需求

## 目的

通过横向对比各技术，要实现statement拆解，必须通过对sql进行token化（完整的词法解析），以及一定程度的语法解析。__可以明确的是sql拆分无法绕过词法分析和语法解析__
我们选取了4个开源项目，尝试使用其statement拆解功能。最终选中了andialbrecht-sqlparse,并调研了对应我们目前产品的开发方案。


## 现有开源技术对比

技术|特点|可用性|维护成本|迁移难度
-|-|-|-|-|
jsqlparser| 功能齐全，使用简单，存在部分sql解析吃出错的问题 | 较差|不易维护|直接使用，无需迁移
druid| 功能齐全，使用简单，存在部分sql解析吃出错的问题|较差|不易维护|直接使用，无需迁移
dbeaver| 与eclipse耦合性高，底层依赖Jsqlparser，并且保有独立一套语法解析模块|强|很难维护|难度高
andialbrecht-sqlparse| 使用简单，功能齐全，耦合性低，但是只能通过python调用，与公司主流技术栈不符|强|容易维护|难度较低


__jsqlparser__ 和 __druid__ 目前已经存在解析pgsql函数失败的问题，使用前需要修复其语法解析的bug，__使用成本高__

__dbeaver__ 虽然可以正常拆解sql,但是代码耦合性强，语法解析部分很难单独抽出，__迁移成本高__

__andialbrecht-sqlparse__ 使用简单，虽然是python写的但是抽象程度低,代码逻辑相对不复杂。__迁移成本低__，目前重点对该开源项目进行了迁移调研。


## andialbrecht-sqlparse 可作为二进制插件被Python调用

目前em运维工具通过二进制调用，其流程如下

1 sql序列化后通过执行参数传入二进制包的 runtime。

2 andialbrecht-sqlparse 将sql解析获得拆解的statement列表

3 业务脚本遍历statement列表并且解析，将最后一个select类型的statement植入cursor声明语句

4 将处理好的sql和cursor名称返回

## andialbrecht-sqlparse 迁移可行性分析

仓库地址：
https://github.com/andialbrecht/sqlparse

单纯考虑拆解statement功能：

1 tokenlize
遍历sql各字符，根据正则字典匹配获取该字符的token。

2 StatementSplitter
根据token拆分sql并转为字符流

需要重点迁移：
+ 各Token类
+ 正则字典
+ 词法分析(tokenlize)-业务代码
+ 隔离等级切换(_change_splitlevel)-业务代码
+ 语法解析-sql拆分(StatementSplitter)-业务代码

