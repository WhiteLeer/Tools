# -*- coding: gbk -*-
import inspect
import os

import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

class ADV_MocapConverter:
    def __init__(self):
        self.mocap_bones_name_list = []
        self.mocap_prefix = "Mocap:"

        self.create_ui()


    def create_ui(self, *_):
        # ---------------------------
        window_name = "ADV_MocapTool"
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name)

        # ---------------------------
        cmds.window(window_name, title="ADV - Mocap 工具")
        main_layout = cmds.columnLayout(adj=True)

        # ---------------------------
        cmds.frameLayout(label="", collapsable=False, parent=main_layout)
        cmds.button("1、加载动捕数据", command=partial(self.import_mocap), bgc=(0.58, 0.88, 0.83))
        cmds.button("2、清理动捕数据", command=partial(self.clear_mocap), bgc=(0.58, 0.88, 0.83))
        cmds.button("3、创建 动捕 对应 HIK", command=lambda _: self.map_to_hik("Mocap"), bgc=(0.58, 0.88, 0.83))
        cmds.setParent('..')

        # ---------------------------
        cmds.frameLayout(label="", collapsable=False, parent=main_layout)
        cmds.button("4、引用 ADV 数据", command=partial(self.import_adv), bgc=(0.92, 1.00, 0.82))
        cmds.button("5、检查 ADV 数据", command=partial(self.check_adv), bgc=(0.92, 1.00, 0.82))
        cmds.button("6、创建 ADV 对应 HIK", command=lambda _: self.map_to_hik("ADV"), bgc=(0.92, 1.00, 0.82))
        cmds.setParent('..')

        # ---------------------------
        cmds.frameLayout(label="", collapsable=False, parent=main_layout)
        cmds.button("7、映射动捕动画", command=partial(self.map_hik), bgc=(0.99, 0.89, 0.54))
        cmds.button("8、烘焙动捕动画", command=partial(self.bake_hik), bgc=(0.95, 0.51, 0.51))

        cmds.setParent('..')

        # ---------------------------
        cmds.showWindow(window_name)


    def map_hik_base(self, is_adv, my_str, my_index):
        current_character = mel.eval('hikGetCurrentCharacter()')

        if is_adv:
            skeleton_ = my_str
        else:
            skeleton_ = self.mocap_prefix + my_str
        mel.eval('setCharacterObject("{}", "{}", {}, 0);'.format(skeleton_, current_character, my_index))


    def map_hik_left(self, is_adv, my_str, my_index):
        current_character = mel.eval('hikGetCurrentCharacter()')

        if is_adv:
            skeleton_ = my_str + "_L"
        else:
            skeleton_ = self.mocap_prefix + my_str + "_L"
        mel.eval('setCharacterObject("{}", "{}", {}, 0);'.format(skeleton_, current_character, my_index))


    def map_hik_right(self, is_adv, my_str, my_index):
        current_character = mel.eval('hikGetCurrentCharacter()')

        if is_adv:
            skeleton_ = my_str + "_R"
        else:
            skeleton_ = self.mocap_prefix + my_str + "_R"
        mel.eval('setCharacterObject("{}", "{}", {}, 0);'.format(skeleton_, current_character, my_index))


    def map_adv_to_hik(self, *_):
        script_path = inspect.getfile(inspect.currentframe())
        maya_root = os.path.dirname(os.path.abspath(script_path))
        maya_root = os.path.dirname(maya_root.rstrip("\\/"))
        plugin_path = os.path.join(maya_root, "plug-ins", "MyMocapTool")
        mel_script_path = os.path.join(plugin_path, "AdvancedSkeleton.mel")
        mel_script_path = mel_script_path.replace("\\", "//")

        if os.path.exists(mel_script_path):
            mel.eval('source "{}";'.format(mel_script_path))
        else:
            print("找不到 MEL 脚本文件: {}".format(mel_script_path))

        mel.eval('asCreateHumanIK')
        mel.eval("hikUnlockDefinition;")


    def map_to_hik(self, prefix, *_):
        if prefix == "ADV":
            hik_root = "Root_M"
            mel.eval('select - r {};'.format(hik_root))
        else :
            if prefix == "Mocap":
                hik_root = self.mocap_prefix + "Root_M"
                mel.eval('select - r {};'.format(hik_root))

        cmds.joint(e=True, apa=True, ch=True)
        cmds.evalDeferred('mel.eval("hikUpdateCharacterListCallback;")')
        cmds.evalDeferred('mel.eval("hikUpdateCharacterControlsUICallback;")')

        if prefix == "ADV":
            mel.eval('hikCreateCharacter("Character1");')
        else:
            if prefix == "Mocap":
                mel.eval('hikCreateCharacter("Character1_mocap");')

        mel.eval('hikUpdateCharacterListCallback;')
        mel.eval('hikControlRigSelectionChangedCallback;')

        name_head = "Head_M"
        name_neck = "Neck_M"
        name_spine1 = "Spine2_M"
        name_spine2 = "Chest_M"
        name_spine = "Spine1_M"
        name_hips = "Root_M"

        name_shoulder = "Scapula"
        name_arm = "Shoulder"
        name_fore_arm = "Elbow"
        name_hand = "Wrist"
        name_HandThumb1 = "ThumbFinger1"
        name_HandThumb2 = "ThumbFinger2"
        name_HandThumb3 = "ThumbFinger3"
        name_HandThumb4 = "ThumbFinger4"
        name_HandIndex1 = "IndexFinger1"
        name_HandIndex2 = "IndexFinger2"
        name_HandIndex3 = "IndexFinger3"
        name_HandIndex4 = "IndexFinger4"
        name_HandMiddle1 = "MiddleFinger1"
        name_HandMiddle2 = "MiddleFinger2"
        name_HandMiddle3 = "MiddleFinger3"
        name_HandMiddle4 = "MiddleFinger4"
        name_HandRing1 = "RingFinger1"
        name_HandRing2 = "RingFinger2"
        name_HandRing3 = "RingFinger3"
        name_HandRing4 = "RingFinger4"
        name_HandPinky1 = "PinkyFinger1"
        name_HandPinky2 = "PinkyFinger2"
        name_HandPinky3 = "PinkyFinger3"
        name_HandPinky4 = "PinkyFinger4"

        name_up_leg = "Hip"
        name_leg = "Knee"
        name_foot = "Ankle"
        name_ToeBase = "Toes"

        is_adv = (prefix == "ADV")

        self.map_hik_base(is_adv, name_head, 15)
        self.map_hik_base(is_adv, name_neck, 20)
        self.map_hik_base(is_adv, name_spine1, 23)
        self.map_hik_base(is_adv, name_spine2, 24)
        self.map_hik_base(is_adv, name_spine, 8)
        self.map_hik_base(is_adv, name_hips, 1)

        self.map_hik_left(is_adv, name_shoulder, 18)
        self.map_hik_left(is_adv, name_arm, 9)
        self.map_hik_left(is_adv, name_fore_arm, 10)
        self.map_hik_left(is_adv, name_hand, 11)

        self.map_hik_left(is_adv, name_HandThumb1, 50)
        self.map_hik_left(is_adv, name_HandThumb2, 51)
        self.map_hik_left(is_adv, name_HandThumb3, 52)
        self.map_hik_left(is_adv, name_HandThumb4, 53)
        self.map_hik_left(is_adv, name_HandIndex1, 54)
        self.map_hik_left(is_adv, name_HandIndex2, 55)
        self.map_hik_left(is_adv, name_HandIndex3, 56)
        self.map_hik_left(is_adv, name_HandIndex4, 57)
        self.map_hik_left(is_adv, name_HandMiddle1, 58)
        self.map_hik_left(is_adv, name_HandMiddle2, 59)
        self.map_hik_left(is_adv, name_HandMiddle3, 60)
        self.map_hik_left(is_adv, name_HandMiddle4, 61)
        self.map_hik_left(is_adv, name_HandRing1, 62)
        self.map_hik_left(is_adv, name_HandRing2, 63)
        self.map_hik_left(is_adv, name_HandRing3, 64)
        self.map_hik_left(is_adv, name_HandRing4, 65)
        self.map_hik_left(is_adv, name_HandPinky1, 66)
        self.map_hik_left(is_adv, name_HandPinky2, 67)
        self.map_hik_left(is_adv, name_HandPinky3, 68)
        self.map_hik_left(is_adv, name_HandPinky4, 69)

        self.map_hik_right(is_adv, name_shoulder, 19)
        self.map_hik_right(is_adv, name_arm, 12)
        self.map_hik_right(is_adv, name_fore_arm, 13)
        self.map_hik_right(is_adv, name_hand, 14)

        self.map_hik_right(is_adv, name_HandThumb1, 74)
        self.map_hik_right(is_adv, name_HandThumb2, 75)
        self.map_hik_right(is_adv, name_HandThumb3, 76)
        self.map_hik_right(is_adv, name_HandThumb4, 77)
        self.map_hik_right(is_adv, name_HandIndex1, 78)
        self.map_hik_right(is_adv, name_HandIndex2, 79)
        self.map_hik_right(is_adv, name_HandIndex3, 80)
        self.map_hik_right(is_adv, name_HandIndex4, 81)
        self.map_hik_right(is_adv, name_HandMiddle1, 82)
        self.map_hik_right(is_adv, name_HandMiddle2, 83)
        self.map_hik_right(is_adv, name_HandMiddle3, 84)
        self.map_hik_right(is_adv, name_HandMiddle4, 85)
        self.map_hik_right(is_adv, name_HandRing1, 86)
        self.map_hik_right(is_adv, name_HandRing2, 87)
        self.map_hik_right(is_adv, name_HandRing3, 88)
        self.map_hik_right(is_adv, name_HandRing4, 89)
        self.map_hik_right(is_adv, name_HandPinky1, 90)
        self.map_hik_right(is_adv, name_HandPinky2, 91)
        self.map_hik_right(is_adv, name_HandPinky3, 92)
        self.map_hik_right(is_adv, name_HandPinky4, 93)

        self.map_hik_left(is_adv, name_up_leg, 2)
        self.map_hik_left(is_adv, name_leg, 3)
        self.map_hik_left(is_adv, name_foot, 4)
        self.map_hik_left(is_adv, name_ToeBase, 16)

        self.map_hik_right(is_adv, name_up_leg, 5)
        self.map_hik_right(is_adv, name_leg, 6)
        self.map_hik_right(is_adv, name_foot, 7)
        self.map_hik_right(is_adv, name_ToeBase, 17)

        if prefix == "ADV":
            mel.eval('hikCreateCustomRig(hikGetCurrentCharacter());')

            name_ctrl_hips = "RootX_M"
            name_ctrl_spine = "FKRoot_M"
            name_ctrl_spine1 = "FKSpine1_M"
            name_ctrl_spine2 = "FKSpine2_M"
            name_ctrl_chest = "FKChest_M"
            name_ctrl_neck = "FKNeck_M"
            name_ctrl_head = "FKHead_M"

            name_ctrl_left_collar = "FKScapula_L"
            name_ctrl_left_arm = "FKShoulder_L"
            name_ctrl_left_elbow = "FKElbow_L"
            name_ctrl_left_wrist = "FKWrist_L"

            name_ctrl_right_collar = "FKScapula_R"
            name_ctrl_right_arm = "FKShoulder_R"
            name_ctrl_right_elbow = "FKElbow_R"
            name_ctrl_right_wrist = "FKWrist_R"

            name_ctrl_left_up_leg = "Hip_L"
            name_ctrl_left_knee = "Knee_L"
            # name_ctrl_left_knee = "PoleLeg_L"
            # name_ctrl_left_ankle = "Ankle_L"
            name_ctrl_left_ankle = "IKLeg_L"

            name_ctrl_right_up_leg = "Hip_R"
            name_ctrl_right_knee = "Knee_R"
            # name_ctrl_right_knee = "PoleLeg_R"
            # name_ctrl_right_ankle = "Ankle_R"
            name_ctrl_right_ankle = "IKLeg_R"

            cmds.select(name_ctrl_hips)
            mel.eval('hikCustomRigAssignEffector 1;')
            cmds.select(name_ctrl_spine)
            mel.eval('hikCustomRigAssignEffector 8;')
            cmds.select(name_ctrl_spine1)
            mel.eval('hikCustomRigAssignEffector 23;')
            cmds.select(name_ctrl_chest)
            mel.eval('hikCustomRigAssignEffector 1000;')
            cmds.select(name_ctrl_neck)
            mel.eval('hikCustomRigAssignEffector 20;')
            cmds.select(name_ctrl_head)
            mel.eval('hikCustomRigAssignEffector 15;')

            cmds.select(name_ctrl_spine2)
            mel.eval('hikCustomRigAssignEffector 24;')

            cmds.select(name_ctrl_left_collar)
            mel.eval('hikCustomRigAssignEffector 18;')
            cmds.select(name_ctrl_left_arm)
            mel.eval('hikCustomRigAssignEffector 9;')
            cmds.select(name_ctrl_left_elbow)
            mel.eval('hikCustomRigAssignEffector 10;')
            cmds.select(name_ctrl_left_wrist)
            mel.eval('hikCustomRigAssignEffector 11;')

            cmds.select(name_ctrl_right_collar)
            mel.eval('hikCustomRigAssignEffector 19;')
            cmds.select(name_ctrl_right_arm)
            mel.eval('hikCustomRigAssignEffector 12;')
            cmds.select(name_ctrl_right_elbow)
            mel.eval('hikCustomRigAssignEffector 13;')
            cmds.select(name_ctrl_right_wrist)
            mel.eval('hikCustomRigAssignEffector 14;')

            cmds.select(name_ctrl_left_up_leg)
            mel.eval('hikCustomRigAssignEffector 2;')
            cmds.select(name_ctrl_left_knee)
            mel.eval('hikCustomRigAssignEffector 3;')
            cmds.select(name_ctrl_left_ankle)
            mel.eval('hikCustomRigAssignEffector 4;')

            cmds.select(name_ctrl_right_up_leg)
            mel.eval('hikCustomRigAssignEffector 5;')
            cmds.select(name_ctrl_right_knee)
            mel.eval('hikCustomRigAssignEffector 6;')
            cmds.select(name_ctrl_right_ankle)
            mel.eval('hikCustomRigAssignEffector 7;')

            mel.eval('setAttr "HIKproperties2.ReachActorHead" 1;')
            mel.eval('setAttr "HIKproperties2.ReachActorHeadRotation" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlPullHead" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorChest" 1;')
            mel.eval('setAttr "HIKproperties2.ReachActorChestRotation" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlResistChestPosition" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorLowerChestRotation" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorLeftElbow" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlPullLeftElbow" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorLeftWrist" 1;')
            mel.eval('setAttr "HIKproperties2.ReachActorLeftWristRotation" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlChestPullLeftHand" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorRightElbow" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlPullRightElbow" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorRightWrist" 1;')
            mel.eval('setAttr "HIKproperties2.ReachActorRightWristRotation" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlChestPullRightHand" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorLeftKnee" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlPullLeftKnee" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorLeftAnkle" 0;')
            mel.eval('setAttr "HIKproperties2.ReachActorLeftAnkleRotationRotation" 0;')
            mel.eval('setAttr "HIKproperties2.CtrlPullLeftFoot" 0;')

            mel.eval('setAttr "HIKproperties2.ReachActorRightKnee" 1;')
            mel.eval('setAttr "HIKproperties2.CtrlPullRightKnee" 1;')

            mel.eval('setAttr "HIKproperties2.ReachActorRightAnkle" 0;')
            mel.eval('setAttr "HIKproperties2.ReachActorRightAnkleRotation" 0;')
            mel.eval('setAttr "HIKproperties2.CtrlPullRightFoot" 0;')


    def map_hik(self, *_):
        cmds.optionMenuGrp('hikCharacterList', edit=True, select=2)
        mel.eval('hikUpdateCharacterListCallback;')
        mel.eval('hikUpdateCurrentCharacterFromUI();')

        cmds.optionMenuGrp('hikSourceList', edit=True, select=2)
        mel.eval('hikControlRigSelectionChangedCallback;')
        mel.eval('hikUpdateCurrentSourceFromUI();')


    def bake_hik(self, *_):
        mel.eval('hikBakeCharacter 0;')


    def import_mocap(self, *_):
        fbx_path = cmds.fileDialog2(fileMode=1, caption="选择", fileFilter="FBX Files (*.fbx)")
        if fbx_path:
            fbx_path[0] = fbx_path[0].replace("\\", "/")
            cmds.FBXImportMode("-v", "add")
            cmds.file(fbx_path[0], i=True, type="FBX", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, namespace="Mocap")

            all_objects = cmds.ls(type="joint")
            for mocap_obj in all_objects:
                mocap_name = mocap_obj.split('|')[-1]
                if mocap_name.startswith("Mocap:"):
                    self.mocap_bones_name_list.append(mocap_name[6:])


    def import_adv(self, *_):
        mel.eval('CreateReference;')


    def check_adv(self, *_):
        error_list = []
        name_list = []
        offset_list = []
        adv_deformation_system = "DeformationSystem"

        if cmds.objExists(adv_deformation_system):
            all_objects = cmds.listRelatives(adv_deformation_system, allDescendents=True, type="joint") or []
            all_objects.sort(key=lambda x: len(x.split("|")), reverse=True)

        for adv_obj in all_objects:
            adv_name = adv_obj.split('|')[-1]
            if adv_name not in self.mocap_bones_name_list:
                error_list.append(adv_name)
            else:
                mocap_objects = cmds.ls("Mocap:" + adv_name, long=True)
                mocap_obj = mocap_objects[0]

                # adv_pos = cmds.xform(adv_obj, query=True, translation=True, worldSpace=True)
                # mocap_pos = cmds.xform(mocap_obj, query=True, translation=True, worldSpace=True)
                # cmds.xform(adv_obj, translation=mocap_pos, worldSpace=True)
                #
                # offset = [round(m - a, 1) for m, a in zip(mocap_pos, adv_pos)]
                # if not all(abs(o) == 0 for o in offset):
                #     offset_list.append(offset)
                #     name_list.append(adv_name)

        output = "--- 骨骼检查信息  ---\n"
        if error_list:
            output += "*** 由于骨骼数量尚未对齐，无法确保动画信息完全准确 ***\n\n"
            output += "\n".join(["{:<30} \t 没有对应的动捕骨骼".format(name) for name in error_list])
        else:
            output += "*** 所有 ADV 骨骼都有对应的动捕骨骼 ***"

        # output += "\n\n*** ****************************************** ***\n\n"
        #
        # if offset_list:
        #     output += "*** 由于骨骼位置尚未对齐，这里对 ADV 骨骼位置做了一些调整 ***\n\n"
        #     output += "\n".join(["将 \t {:<30} 偏移 \t {} ".format(name, offset) for name, offset in zip(name_list, offset_list)])
        # else:
        #     output += "*** 动捕骨骼和对应 ADV 骨骼的初始位置完全一致 ***"

        win = cmds.window(title="骨骼检查", widthHeight=(600, 525))
        cmds.columnLayout(adjustableColumn=True)
        cmds.scrollField(editable=False, wordWrap=False, text=output, width=580, height=500)
        cmds.button(label="我已知晓", command=lambda _: cmds.deleteUI(win))
        cmds.showWindow(win)


    def clear_mocap(self, *_):
        all_objects = cmds.ls(type="transform")
        non_joint_objects = [obj for obj in all_objects if cmds.nodeType(obj) != "joint"]
        for mocap_obj in non_joint_objects:
            mocap_name = mocap_obj.split('|')[-1]
            if mocap_name.startswith("Mocap:") and mocap_obj in cmds.ls(type="transform"):
                cmds.delete(mocap_obj)


    # def clear_adv(self, *_):
    #     ### Rename ADV - 0
    #     all_objects = cmds.ls(type="transform")
    #     sel_list = om.MSelectionList()
    #     name_list = []
    #
    #     for obj in all_objects:
    #         adv_name = obj.split('|')[-1]
    #
    #         if adv_name.startswith("ADV:"):
    #             sel_list.add(obj)
    #             name_list.append(adv_name[4:])
    #
    #     ### Rename ADV - 1
    #     for i in range(sel_list.length()):
    #         now_obj = om.MObject()
    #         sel_list.getDependNode(i, now_obj)
    #         dep_node = om.MFnDependencyNode(now_obj)
    #
    #         new_name = name_list[i]
    #         dep_node.setName(new_name)


if __name__ == "__main__":
    tool = ADV_MocapConverter()