# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/04/16


import traceback

from PySide2 import QtWidgets
from PySide2 import QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

from . import config




def handle_error_dialog(func):
    '''
    弹出窗户口显示 traceback.format_exc() 的报错
    '''

    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  u"错误",
                                  traceback.format_exc()).exec_()
    return handle


def getMayaWindow():
    main_window_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_pointer), QtWidgets.QWidget)


class ComboBox(QtWidgets.QComboBox):
    clicked = QtCore.Signal()

    def mousePressEvent(self, event):
        super(ComboBox, self).mousePressEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton:  ##判断是否鼠标左键点击
            self.clicked.emit()


class DropLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(DropLineEdit, self).__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(DropLineEdit, self).dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url_object = event.mimeData().urls()[0]
            self.setText(url_object.toLocalFile())
        else:
            super(DropLineEdit, self).dropEvent(event)


class Form_Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None, title=None, message=None):
        super(Form_Dialog, self).__init__(parent)
        self.title = title
        self.message = message

        self.input_value = None

        self.__setup_ui()
        self.__retranslate_ui()
        self.__setup_connect()

    def __setup_ui(self):
        self.message_label = QtWidgets.QLabel()
        self.edit = DropLineEdit()
        self.button = QtWidgets.QPushButton()

        layout = QtWidgets.QVBoxLayout()
        if self.message:
            layout.addWidget(self.message_label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def __retranslate_ui(self):
        if self.message:
            self.message_label.setText(self.message)
        if self.title:
            self.setWindowTitle(self.title)
        self.setMinimumWidth(220)
        self.button.setText(u"确定")

    def __setup_connect(self):
        self.button.clicked.connect(self.save_value)
        #self.edit.editingFinished.connect(self.button.clicked.emit)

    def save_value(self):
        self.input_value = self.edit.text()
        self.close()

    def get_value(self):
        return self.input_value


class MappingBaseWidget(QtWidgets.QWidget):
    find_button_clicked = QtCore.Signal()
    select_button_clicked = QtCore.Signal()
    mapping_button_clicked = QtCore.Signal()

    def __init__(self, hik_code):
        super(MappingBaseWidget, self).__init__()

        self.hik_code = hik_code
        self.long_name = ""
        self.type = ""

        self.__setup_ui()
        self.__retranslate_ui()
        self.__setup_connect()

    def __setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.map_key = QtWidgets.QLineEdit()
        self.find_button = QtWidgets.QPushButton()
        self.node_button = QtWidgets.QPushButton()
        self.mapping_button = QtWidgets.QPushButton()
        self.hik_code_label = QtWidgets.QLabel(self.hik_code)
        #self.hik_code_label = QtWidgets.QPushButton(self.hik_code)

        self.main_layout.addWidget(self.map_key)
        self.main_layout.addWidget(self.find_button)
        self.main_layout.addWidget(self.node_button)
        self.main_layout.addWidget(self.mapping_button)
        self.main_layout.addWidget(self.hik_code_label)

    def __retranslate_ui(self):
        self.map_key.setMinimumWidth(80)
        self.find_button.setText(">")
        self.mapping_button.setText(">")
        self.hik_code_label.setStyleSheet("font-weight:bold;")

    def __setup_connect(self):
        self.find_button.clicked.connect(self.click_find_button)
        self.node_button.clicked.connect(self.click_select_button)
        self.mapping_button.clicked.connect(self.click_mapping_button)

    def get_hik_code(self):
        return self.hik_code_label.text()

    def click_find_button(self):
        self.find_button_clicked.emit()

    def click_mapping_button(self):
        self.mapping_button_clicked.emit()

    def click_select_button(self):
        self.select_button_clicked.emit()

    def get_mapkey(self):
        return self.map_key.text()

    def set_mapkey(self, key_str):
        self.map_key.setText(key_str)

    def __make_parent_tree(self, long_name):
        parent_list = long_name.split("|")
        hierarchy = 0
        tree = ""
        for p in parent_list:
            if p == parent_list[0]:
                tree += p + u"\n"
                continue
            tree += u" " * hierarchy + u"| " + p + u"\n"
            hierarchy += 1
        return tree

    def set_tip(self, node_type="", long_name=""):
        if not node_type:
            node_type = self.type
        if not long_name:
            long_name = self.long_name

        tip = ""
        if node_type:
            tip += "%s\n" % node_type
        if long_name:
            tip += "%s" % self.__make_parent_tree(long_name)
        self.node_button.setToolTip(tip)

    def set_long_name(self, long_name):
        self.long_name = long_name

    def get_long_name(self):
        return self.long_name

    def set_name(self, node_type, node_name):
        if node_name:
            self.node_button.setText(node_name)
            self.type = node_type
            if node_type == "joint":
                self.node_button.setStyleSheet("background-color:#9276D9;text-align:left;color:#373737;")
            elif node_type == "nurbsCurve":
                self.node_button.setStyleSheet("background-color:#429ECC;text-align:left;color:#373737;")
            else:
                self.node_button.setStyleSheet("background-color:#979797;text-align:left;color:#373737;")
        else:
            self.node_button.setText("")
            self.node_button.setStyleSheet("QPushButton{background-color:#5d5d5d;}")

    def clear_node(self):
        self.long_name = ""
        self.type = ""
        self.node_button.setToolTip(None)
        self.node_button.setStyleSheet("background-color:#5d5d5d")
        self.node_button.setText("")

    def activate_hik_code(self):
        self.hik_code_label.setStyleSheet("font-weight:bold;color: GreenYellow")

    def inactivate_hik_code(self):
        self.hik_code_label.setStyleSheet("color: #eeeeee")


class MappingTabWidget(QtWidgets.QTabWidget):
    def __init__(self, hik_codes_sort):
        super(MappingTabWidget, self).__init__()

        self.hik_codes_sort = hik_codes_sort
        self.__map_widgets_dict = {}  # 保存所有映射控件类

        self.__setup_ui()

    def __setup_ui(self):
        for tab_name in self.hik_codes_sort:
            # 每个tab控件（addtab 添加部分）
            self.tab_widget = QtWidgets.QWidget()
            # 将tab布局添加到tab控件中
            self.tab_layout = QtWidgets.QHBoxLayout(self.tab_widget)
            for hik_code_part in self.hik_codes_sort[tab_name]:
                # 创建一个垂直布局来装每一条映射表
                part_layout = QtWidgets.QVBoxLayout()
                # 创建每一条映射表添加到垂直布局中
                for hik_code_name in hik_code_part:
                    map_widget = MappingBaseWidget(hik_code=hik_code_name)
                    self.__map_widgets_dict[hik_code_name] = map_widget
                    part_layout.addWidget(map_widget)
                part_layout.addStretch()
                # 将垂直布局添加到主布局
                self.tab_layout.addLayout(part_layout)
            self.addTab(self.tab_widget, tab_name)

    def set_mapkey(self, hik_code, key_str):
        mw = self.__map_widgets_dict.get(hik_code)
        if mw:
            mw.set_mapkey(key_str)

    def items(self):
        return self.__map_widgets_dict.values()


class MainUI(QtWidgets.QWidget):
    def __init__(self):
        super(MainUI, self).__init__()
        self.settings = QtCore.QSettings(u"hz_soft", u"hik_retargeting_tool")  # 保存设置类

        self.__setup_ui()
        self.__retranslate_ui()

    def __setup_ui(self):
        self.setParent(getMayaWindow(), QtCore.Qt.Window)  # 设置maya为父级窗口
        # region UI
        # 主窗口垂直布局
        self.main_window = QtWidgets.QVBoxLayout(self)

        # region HIK 工具架
        # HIK 工具架布局
        self.template_tool_layout = QtWidgets.QHBoxLayout()
        # HIK 工具架
        self.temp_label = QtWidgets.QLabel()
        self.temp_combobox = ComboBox()
        self.create_button = QtWidgets.QPushButton()
        self.del_button = QtWidgets.QPushButton()
        self.template_step = QtWidgets.QLabel()
        self.import_button = QtWidgets.QPushButton()
        self.export_button = QtWidgets.QPushButton()
        self.help_button = QtWidgets.QPushButton()
        # 添加 HIK 工具架
        self.template_tool_layout.addWidget(self.temp_label)
        self.template_tool_layout.addWidget(self.temp_combobox)
        self.template_tool_layout.addWidget(self.create_button)
        self.template_tool_layout.addWidget(self.del_button)
        self.template_tool_layout.addWidget(self.template_step)
        self.template_tool_layout.addWidget(self.import_button)
        self.template_tool_layout.addWidget(self.export_button)
        self.template_tool_layout.addStretch()
        self.template_tool_layout.addWidget(self.help_button)
        # endregion

        # region 映射标签页
        self.hik_mapping_tab = MappingTabWidget(config.HIK_CODES_SORT)
        # endregion

        # region HIK 执行栏
        # HIK 执行栏 布局
        self.process_layout = QtWidgets.QHBoxLayout()
        # self.character_name_label = QtWidgets.QLabel()
        self.group_button = QtWidgets.QPushButton()
        self.group_character_step_label = QtWidgets.QLabel()
        self.character_button = QtWidgets.QPushButton()
        self.group_to_mapping_step = QtWidgets.QLabel()
        self.find_mapping_button = QtWidgets.QPushButton()
        self.start_mapping_button = QtWidgets.QPushButton()
        # 添加到 HIK 执行栏
        # self.process_layout.addWidget(self.character_name_label)
        self.process_layout.addWidget(self.group_button)
        self.process_layout.addWidget(self.group_character_step_label)
        self.process_layout.addWidget(self.character_button)
        self.process_layout.addWidget(self.group_to_mapping_step)
        self.process_layout.addWidget(self.find_mapping_button)
        self.process_layout.addWidget(self.start_mapping_button)
        self.process_layout.addStretch()
        # endregion

        # 添加到主窗口
        self.main_window.addLayout(self.template_tool_layout)
        self.main_window.addWidget(self.hik_mapping_tab)
        self.main_window.addLayout(self.process_layout)
        # endregion

    def __retranslate_ui(self):
        self.setWindowTitle(u"HIK 批量映射工具")
        self.temp_label.setText(u"映射模板:")
        self.temp_combobox.setMinimumWidth(80)
        self.del_button.setText(u"删除")
        self.del_button.setStyleSheet(":hover{background-color: Brown;}")
        self.create_button.setText(u"新建")
        self.template_step.setText(u" | ")
        self.import_button.setText(u"导入")
        self.export_button.setText(u"导出")
        self.help_button.setText(u"使用说明")
        self.help_button.setStyleSheet("background-color: Brown;")

        # self.character_name_label.setText(u"HIK角色名:")
        self.group_button.setMinimumWidth(80)
        #self.group_name.setStyleSheet("border:1px solid #2b2b2b")
        self.group_button.setText(u"获取选中的组")
        self.group_character_step_label.setText("->")
        self.character_button.setMinimumWidth(80)
        #self.character_label.setStyleSheet("border:1px solid #2b2b2b")
        # self.character_label.setStyleSheet("border:1px solid gray")
        self.character_button.setText(u"创建/匹配HIK角色")
        #self.character_button.setMinimumSize(25, 25)
        #self.character_button.setStyleSheet(":hover{background-color: DarkOliveGreen;}")
        self.group_to_mapping_step.setText(u" | ")
        self.find_mapping_button.setText(u"批量匹配")
        self.start_mapping_button.setText(u"批量映射")

        # 关闭映射按钮
        self.enable_find_mapping_button(False)
        self.enable_mapping_button(False)

    def set_character_name(self, text):
        self.character_button.setText(str(text))
        self.character_button.setStyleSheet("background-color:#4b4b4b; font-weight:bold;color: GreenYellow")

    def clear_character_name(self):
        self.character_button.setText(u"创建/匹配HIK角色")
        self.character_button.setStyleSheet("color: white")

    def set_group_name(self, text):
        self.group_button.setText(str(text))
        self.group_button.setStyleSheet("background-color:#979797;color:#373737;")

    def clear_group_name(self):
        self.group_button.setText(u"获取选中的组")
        self.group_button.setStyleSheet("background-color:#5d5d5d;color:white;")

    def get_character_name(self):
        return self.character_button.text()

    def show_message_dialog(self, content, title=u"注意"):
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, title, content).exec_()

    def show_warning_dialog(self, content, title=u"警告", ):
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, content).exec_()

    def show_form_dialog(self, title, message=None):
        form_dialog = Form_Dialog(parent=self, title=title, message=message)
        form_dialog.exec_()
        return form_dialog.get_value()

    def enable_find_mapping_button(self, status):
        # 激活映射查找按钮
        for mw in self.hik_mapping_tab.items():
            mw.find_button.setEnabled(status)
            mw.node_button.setEnabled(status)
        self.find_mapping_button.setEnabled(status)

    def enable_mapping_button(self, status):
        # 激活映射映射按钮
        for mw in self.hik_mapping_tab.items():
            mw.mapping_button.setEnabled(status)
        self.start_mapping_button.setEnabled(status)
