# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/04/16


import pymel.core as pm


class Characterize(object):
    """
        hik 指令
    """
    def __init__(self):
        # Load Plugins
        if not pm.pluginInfo('mayaHIK', q=True, l=True):
            pm.loadPlugin('mayaHIK')
        if not pm.pluginInfo('mayaCharacterization', q=True, l=True):
            pm.loadPlugin('mayaCharacterization')
        if not pm.pluginInfo('retargeterNodes', q=True, l=True):
            pm.loadPlugin('retargeterNodes')

    def is_character_definition(self, char):
        # 查看节点是否存在
        if not pm.objExists(char):
            return False

        # 插件节点类型
        if pm.objectType(char) != 'HIKCharacterNode':
            return False

        return True

    def set_current_character(self, char):
        """

        Args:
            char:

        Returns:

        """
        # 设置当前角色
        pm.mel.hikSetCurrentCharacter(char)
        # 刷新角色列表
        try:
            pm.mel.hikUpdateCharacterList()
            pm.mel.hikSelectDefinitionTab()
        except:
            pass
        pm.mel.hikUpdateCurrentCharacterFromUI()
        pm.mel.hikUpdateContextualUI()

    def is_character_definition_locked(self, char):
        """

        Args:
            char:

        Returns:

        """
        # Check Character Definition
        if not self.is_character_definition(char):
            raise Exception(
                'Invalid character definition node! Object "' + char + '" does not exist or is not a valid HIKCharacterNode!')

        # Check Lock
        lock = pm.getAttr(char + '.InputCharacterizationLock')

        # Return Result
        return lock

    def character_definition_lock(self, char, lock_state=True):
        """

        Args:
            char:
            lock_state:

        Returns:

        """
        # Check Character Definition
        if not self.is_character_definition(char):
            raise Exception(
                'Invalid character definition node! Object "' + char + '" does not exist or is not a valid HIKCharacterNode!')

        # Set Current
        self.set_current_character(char)

        # Check Lock State
        isLocked = self.is_character_definition_locked(char)

        # Set Lock State
        if lock_state != isLocked:
            pm.mel.eval('hikToggleLockDefinition')
            # pm.mel.eval('mayaHIKcharacterLock("'+char+'",'+str(int(lockState))+','+str(int(saveStance))+')')

        # Return State
        return lock_state

    def set_character_object(self, char_def, char_bone, bone_id, delete_bone=False):
        pm.mel.setCharacterObject(char_bone, char_def, bone_id, delete_bone)
        pm.mel.hikUpdateCurrentCharacterFromUI()

    def create_character_node(self, char_name):
        # 创建并选择角色
        #char_def = pm.mel.eval('CreateHIKCharacterWithName "' + char_name + '"')
        char_def = pm.mel.hikCreateCharacter(char_name)
        self.set_current_character(char_def)

        # 尝试刷新列表
        try:
            #pm.mel.eval('hikUpdateCharacterList()')
            pm.mel.hikUpdateCharacterList()
            #pm.mel.eval('hikSelectDefinitionTab()')
            pm.mel.hikSelectDefinitionTab()
        except:
            pass
        return char_def

    def get_character_nodes(self, char):
        """

        Returns:

        """
        # 检查节点
        if not self.is_character_definition(char):
            raise Exception(
                'Invalid character definition node! Object "' + char + '" does not exist or is not a valid HIKCharacterNode!')

        # 获取节点
        #charNodes = pm.mel.eval('hikGetSkeletonNodes "' + char + '"')
        char_nodes = pm.ls(char, type="HIKCharacterNode")

        # Return Result
        return char_nodes

    def get_one_character_node(self, char):
        return self.get_character_nodes(char)[0]

    def get_hik_nodes(self):
        return pm.ls(type="HIKCharacterNode")
