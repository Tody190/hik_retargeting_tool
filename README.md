# 功能描述

<img src=doc/img/主界面.png>

本工具用于动捕项目中，角色绑定系统与HIK的绑定系统快速批量匹配

支持模糊名称搜索骨骼名进行批量

支持根据模糊名批量生成模板，并支持模板导入导出

支持根据模糊名称模板批量匹配角色批量

# 使用说明

## 1.查找骨骼和控制器

<img src=doc\img\大纲.bmp>

工具在启动后，首先选中一个Maya大纲中的一个组,点击左下角的<img src=doc\doc\img\获取选中的组按钮.bmp>

，工具将获取此层级下所有节点，以备后续节点搜索功能使用。

<img src=doc\img\选中组.bmp>

当节点获取成功时，按钮名将显示组名，并且工具所有匹配功能控件变为启用状态。

<img src=doc\img\映射控件.bmp>

匹配功能启用后，第一栏输入需要查找的骨骼或者控制器关键字，点击右侧<img src=doc\img\向右.bmp>即可模糊查找节点，右侧按钮将显示与关键词最匹配的节点名。

点击<img src=doc\img\批量匹配.bmp>可以执行批量查找。

## 2. 映射 HumanIK

在执行映射功能前，先创建HumanIK角色

点击<img src=doc\img\创建角色.bmp>

<img src=doc\img\创建角色弹窗.bmp>

输入角色名，点击确定或者回车键

<img src=doc\img\创建角色成功.bmp>

创建成功后，HumanIK界面将自动索引到当前角色。

如果输入角色名已存在，工具将直接所以到当前角色，不再另行创建。

<img src=doc\img\映射骨骼.bmp>

工具执行查找并找到对应节点后，点击 <img src=doc\img\向右.bmp>按钮执行节点与骨骼的映射，可以从HumanIK图示中查看映射状态。

点击 <img src=doc\img\批量映射按钮.bmp>可以执行批量映射功能

## 3. 模板的创建删除与导入导出

本工具支持多套控制器命名和HumanIK角色映射

<img src=doc\img\创建模板.bmp>

点击新建模板输入模板名称

<img src=doc\img\下拉菜单.bmp>

创建成功后下拉菜单选择不同的映射模板

本工具也支持模板的导入导出

<img src=doc\img\导入映射.bmp>

点击导入按钮，可以将导出的 HIKM 文件导入映射表

<img src=doc\img\导出.bmp>

点击导出按钮可以将当前映射信息导出

## 4. 节点的操作

<img src=doc\img\节点提示.bmp>

当查到节点，鼠标在节点上短暂停留，会显示这个节点的节点类型，以及节点所在层级

<img src=doc\img\点选节点.bmp>

点击节点按钮，此节点会在Maya中选中，maya视图也将导航到节点所在位置

工具使用不同颜色区分不同的节点类型

<img src=doc\img\蓝色节点.bmp> 蓝色 曲线控制器

<img src=doc\img\骨骼节点.bmp> 紫色 Maya骨骼

<img src=doc\img\灰色.bmp> 灰色 其它类型节点
