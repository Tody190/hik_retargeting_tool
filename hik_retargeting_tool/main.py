# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/04/09
import os.path
import json

from lib.fuzzywuzzy import fuzz

import ui
import maya_util
import maya_hik
import config


class Response(ui.MainUI):
    instance = None

    def __init__(self):
        super(Response, self).__init__()
        self.current_nodes_list = []  # 当前的节点列表

        self.__setup_data()
        self.__setup_connect()

    def __setup_data(self):
        """
        设置初始化数据，包括UI，以及UI调取到的数据
        Returns:

        """
        # 实例化 hik
        self.hik_char = maya_hik.Characterize()
        # 将初始化映射数据保存到设置中
        self.init_HIK_mapping()
        # 将模板名添加到下拉列表中
        self.refresh_mapping_combobox()
        # 从设置中获取当前需要选中的列表
        current_temp_name = self.settings.value("current_mapping", None)
        if current_temp_name:
            self.temp_combobox.setCurrentText(current_temp_name)
        # 刷新 HIK 名称映射表到UI
        self.refresh_mapping_key()

    def __setup_connect(self):
        # 获取选中的组
        self.group_button.clicked.connect(self.set_group)
        # 创建 HIK 角色
        self.character_button.clicked.connect(self.create_character)
        # 查找映射到的实体
        self.find_mapping_button.clicked.connect(self.batch_find_mapping_key)
        # 开始映射按钮
        self.start_mapping_button.clicked.connect(self.batch_mapping)
        # 创建按钮
        self.create_button.clicked.connect(self.create_mapping_template)
        # 删除按钮
        self.del_button.clicked.connect(self.delete_mapping_template)
        # 模板下拉菜单点击保存当前页面
        self.temp_combobox.clicked.connect(self.save_template)
        # 下拉菜单切换刷新映射列表控件
        self.temp_combobox.currentIndexChanged.connect(self.refresh_mapping_key)
        # 导入
        self.import_button.clicked.connect(self.import_mapping)
        # 导出
        self.export_button.clicked.connect(self.export_mapping)
        # 连接映射列表内单个按钮
        for map_widget in self.hik_mapping_tab.items():
            map_widget.find_button_clicked.connect(self.find_mapping_key)
            map_widget.select_button_clicked.connect(self.select_node)
            map_widget.mapping_button_clicked.connect(self.mapping)

        # 打开使用说明
        self.help_button.clicked.connect(self.open_instruction)

    def import_mapping(self):
        """
        从外部导入映射表
        Returns:

        """
        # 打开文件对话框
        import_file = self.show_form_dialog(u"导入", u"请输入 %s 文件路径" % config.FILE_EXT)
        if not import_file:
            return
        # 检查路径是否存在
        if not os.path.isfile(import_file):
            self.show_warning_dialog(u"%s\n文件不存在" % import_file)
            return
        # 检查格式是否正确
        if not os.path.splitext(import_file)[-1] == config.FILE_EXT:
            self.show_warning_dialog(u"%s\n文件格式不正确" % import_file)
            return
        # 获取文件名为模板名
        mapping_file_name = os.path.basename(import_file)
        mapping_file_name = os.path.splitext(mapping_file_name)[0]
        # 读取json文件
        with open(import_file, "r") as f:
            mapping_dict = json.load(f)

        # 确定是否导入成功
        if not mapping_dict:
            self.show_warning_dialog(u"导入失败")
            return

        # 创建新的映射表
        new_mapping_dict = {"name": mapping_file_name,
                            "map": mapping_dict}
        # 将新的映射列表添加到设置中
        self.add_template(new_mapping_dict)
        # 重置下拉菜单
        self.refresh_mapping_combobox(mapping_file_name)
        self.show_message_dialog(u"映射模板已切换至 %s" % mapping_file_name, title=u"导入成功")

    def export_mapping(self):
        """
        导出当前映射表到外部
        Returns:

        """
        # 保存当前映射表到设置（防止后面的读取时得不到最新消息）
        self.save_template()
        # 从设置获取当前映射表
        mapping_name = self.temp_combobox.currentText()  # 保存的文件名
        mapping_file_name = mapping_name + config.FILE_EXT
        mapping_dict = self.get_mapping(name=mapping_name)  # 保存的数据
        # 打开文件对话框
        export_path = self.show_form_dialog(u"导出", u"请输入导出路径")
        # 检查路径是否存在
        if not export_path:
            return
        if not os.path.isdir(export_path):
            self.show_warning_dialog(u"%s 路径不存在" % export_path)
            return
        # 写入 json 文件
        json_file_name = os.path.join(export_path, mapping_file_name)
        with open(json_file_name, 'w') as f:
            json.dump(mapping_dict, f)
        # 检查是否导出成功
        if os.path.isfile(json_file_name):
            self.show_message_dialog(u"%s\n" % json_file_name, title=u"导出成功")
        else:
            self.show_warning_dialog(u"导出失败")

    def get_mapping(self, name):
        """
        获取映射表
        Returns:

        """
        mapping_list = self.settings.value("mapping", [])
        for m in mapping_list:
            if m["name"] == name:
                return m["map"]

    def get_mapping_name_list(self):
        """
        获取映射表名
        Returns:

        """
        return [m["name"] for m in self.settings.value("mapping", [])]

    def set_group(self):
        """
        获取节点列表
        Returns:

        """
        # 获取选中组
        selected = maya_util.get_one_selection()
        if selected:
            #关闭映射查找按钮
            self.enable_find_mapping_button(True)
            # 设置UI显示的组名
            self.set_group_name(selected.name())
            # 获取选中的节点下所有的子 transform 节点
            self.current_nodes_list = maya_util.get_relatives_transform(selected)
            # 将选中节点也添加到获取的节点列表中
            # 保证以后插件对应节点时，当前选中节点也在匹配范围内
            self.current_nodes_list.insert(0, selected)
        else:
            self.current_nodes_list = []
            #关闭映射查找按钮
            self.enable_find_mapping_button(False)
            # 充值组按钮的配色
            self.clear_group_name()
            #self.show_warning_dialog(u"请先选中一个组, 工具将在选中的组中查找匹配的映射对象")
            return

    def create_character(self):
        """
        创建 HIK 角色
        """
        # 输入 HIK 角色名的UI弹窗
        input_character_name = self.show_form_dialog(u"请输入HIK角色名")
        if not input_character_name:
            # 激活映射按钮
            self.enable_mapping_button(False)
            # UI 配色恢复默认
            self.clear_character_name()
            return

        # 创建 hik 角色， 如果存在就获取
        if self.hik_char.is_character_definition(input_character_name):
            create_character_name = self.hik_char.get_one_character_node(input_character_name)
            self.hik_char.set_current_character(input_character_name)
        else:
            create_character_name = self.hik_char.create_character_node(input_character_name)
            self.hik_char.set_current_character(input_character_name)

        # hik 默认创建的名可能不同，冲获取hik节点名并显示在UI上
        if create_character_name:
            self.enable_mapping_button(True)
            self.set_character_name(create_character_name)

    def best_match(self, match_key, node_list):
        """
        从 match_list 查找与 match_key 最匹配的列表
        Args:
            node_list:
            match_key:
            match_list:

        Returns:

        """
        current_ratio = 0
        current_node_name = None
        current_node = None
        for n in node_list:
            # 遍历节点
            node_name = n.name()
            # 去掉空间名
            #node_name = node_name.split(":", -1)[-1]
            ratio = fuzz.ratio(match_key, node_name)
            if ratio >= current_ratio:
                # 如果当前匹配率相同
                if ratio == current_ratio and ratio > 0:
                    # 计算当前节点名和已记录的节点名的长度
                    new_node_len = len(node_name)
                    old_node_len = len(current_node_name)
                    # 取最短的名字
                    if new_node_len > old_node_len:
                        # 如果当前节点名字长度大于已记录的
                        # 跳过
                        continue

                # 如果匹配率大于等于当前匹配率
                # 保存节点并保存匹配率
                current_ratio = ratio
                current_node_name = node_name
                current_node = n
                # 如果匹配率为 100% 直接返回节点
                if ratio == 100:
                    return current_node
        if current_ratio > 0:
            return current_node

    def batch_find_mapping_key(self):
        """
        批量预览映射
        Returns:

        """
        for map_widget in self.hik_mapping_tab.items():
            map_widget.click_find_button()

    def find_mapping_key(self):
        """
        预览映射，通过映射模板名模糊匹配符合名称的节点
        Returns:

        """
        if self.current_nodes_list:
            # 获取映射表控件
            map_widget = self.sender()
            map_widget.inactivate_hik_code()
            # 获取匹配用的 key
            mapkey = map_widget.get_mapkey()
            # 匹配最佳物体
            match_node = self.best_match(mapkey, self.current_nodes_list)
            if not match_node:
                map_widget.clear_node()
            if match_node:
                # 获取节点类型
                try:
                    match_node_shape = match_node.getShape()
                    match_node_type = match_node_shape.type()
                except:
                    match_node_type = match_node.type()
                # 设置节点名
                node_name = match_node.name()
                # 在UI显示上去除空间名
                if ":" in node_name:
                    node_name = node_name.split(":", -1)[-1]
                map_widget.set_name(match_node_type, node_name)
                # 设置长名
                map_widget.set_long_name(match_node.longName())
                # 设置提示
                map_widget.set_tip()

    def batch_mapping(self):
        """
        批量映射
        Returns:

        """
        for map_widget in self.hik_mapping_tab.items():
            map_widget.click_mapping_button()

    def mapping(self):
        """
        映射节点到角色
        Returns:

        """
        # 获取 hik 角色名
        character_name = self.get_character_name()
        map_widget = self.sender()
        # 要映射的节点名
        mapping_long_name = map_widget.long_name
        # hik 名
        hik_code = map_widget.hik_code
        # hik id
        hik_id = config.HUMAN_IK_CODES.get(hik_code)
        if character_name and mapping_long_name and hik_id:
            # 执行映射
            self.hik_char.set_character_object(character_name, mapping_long_name, hik_id)
            map_widget.activate_hik_code()

    def select_node(self):
        # 获取映射表控件
        map_widget = self.sender()
        long_name = map_widget.get_long_name()
        if long_name:
            maya_util.select_node(long_name)

    def refresh_mapping_combobox(self, current_text=None):
        self.temp_combobox.clear()
        mapping_name_list = self.get_mapping_name_list()
        if mapping_name_list:
            self.temp_combobox.addItems(mapping_name_list)
            if current_text:
                self.temp_combobox.setCurrentText(current_text)

    def refresh_mapping_key(self):
        """
        刷新 HIK 名称映射表到UI
        Returns:
        """
        # 获取当前下拉菜单选中的模板名
        temp_name = self.temp_combobox.currentText()
        if temp_name:
            # 获取对应映射表
            current_map = self.get_mapping(temp_name)
            # 设置实例的 map key
            for hik_code in current_map:
                self.hik_mapping_tab.set_mapkey(hik_code, current_map.get(hik_code))

    def create_mapping_template(self):
        mapping_template_name = self.show_form_dialog(u"请输入模板名称")
        if not mapping_template_name:
            return
        else:
            # 如果创建的模板名存在，返回提示
            if mapping_template_name in self.get_mapping_name_list():
                self.show_warning_dialog(u"创建失败，模板已存在。")
                return

        # 保存当前模板
        self.save_template()
        # 添加新的模板到设置
        self.save_template(mapping_template_name)
        # 重置下拉菜单
        self.refresh_mapping_combobox(mapping_template_name)

    def init_HIK_mapping(self):
        """
        Returns:
             dict, {"Hips": hip, "LeftUpLeg": leftupleg,}
        """
        hik_map = {u"name": u"HIK", u"map": {}}
        for map_widget in self.hik_mapping_tab.items():
            k = map_widget.get_hik_code()
            hik_map[u"map"][k] = k.lower()

        self.add_template(hik_map)

    def add_template(self, new_mapping_dict):
        """
        将新的行映射表添加到模板中，如果映射表存在就替换，不存在就添加
        Args:
            new_mapping_dict:

        Returns:

        """
        # 获取所有保存的映射表
        saved_mapping = self.settings.value("mapping", [])  # 所有的映射表
        is_new_mapping_exist = False
        for i, m in enumerate(saved_mapping):
            # 如果这个映射表存在，替换掉旧的
            if m["name"] == new_mapping_dict["name"]:
                saved_mapping[i] = new_mapping_dict
                is_new_mapping_exist = True
        # 如果这个映射表不存在，添加到当前
        if not is_new_mapping_exist:
            saved_mapping.append(new_mapping_dict)

        # 重新保存到设置
        self.settings.setValue("mapping", saved_mapping)

    def save_template(self, new=None):
        """
        保存当前页面,或将当前页面保存到指定模板名下
        Returns:

        """
        new_mapping_dict = {"name": "", "map": {}}  # 构建一个新的映射表
        if new:
            new_mapping_dict["name"] = new
        else:
            name = self.temp_combobox.currentText()
            if name:
                new_mapping_dict["name"] = name
            else:
                # 下拉列表中获取到了空值，就返回
                return

        # 依次获取映射表的键和值,并添加到新表里
        mws = self.hik_mapping_tab.items()
        for mw in mws:
            hik_code = mw.get_hik_code()
            map_key = mw.get_mapkey()
            if not map_key:
                map_key = ""
            new_mapping_dict["map"][hik_code] = map_key

        self.add_template(new_mapping_dict)

    def delete_mapping_template(self):
        temp_name = self.temp_combobox.currentText()
        saved_mapping = self.settings.value("mapping", [])  # 所有的映射表
        for map_dict in saved_mapping:
            if map_dict["name"] == temp_name:
                # 从映射表中删除
                saved_mapping.remove(map_dict)
                # 重新保存到设置
                self.settings.setValue("mapping", saved_mapping)
        self.refresh_mapping_combobox()

    def open_instruction(self):
        # 打开说明文档
        os.startfile(config.INSTRUCTION_FILE)

    def closeEvent(self, event):
        # 保存当前页面
        self.save_template()
        # 保存当前模板下拉菜单值
        current_temp_name = self.temp_combobox.currentText()
        if current_temp_name:
            self.settings.setValue("current_mapping", current_temp_name)


@ui.handle_error_dialog
def show():
    """

    Returns:

    """
    if not Response.instance:
        Response.instance = Response()
    Response.instance.show()
    Response.instance.raise_()