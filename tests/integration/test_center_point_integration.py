import pytest
from pytest import fixture
from unittest.mock import Mock
from unittest.mock import patch
import maya.api.OpenMaya as om
import maya.cmds as cmds

import center_point_node as plugin_module
from center_point_node import CenterPointNode

PLUGIN_NAME = "center_point_node.py"

@fixture(scope="function", autouse=True)
def load_plugin():
    if not cmds.pluginInfo({PLUGIN_NAME}, q=True, loaded=True):
        cmds.loadPlugin(PLUGIN_NAME)

def test_plugin_initialization():
    assert cmds.pluginInfo({PLUGIN_NAME}, q=True, loaded=True)

def test_plugin_deinitialization():
    cmds.unloadPlugin(PLUGIN_NAME)
    assert not cmds.pluginInfo({PLUGIN_NAME}, q=True, loaded=True)

def test_node_is_created():
    center_point_node = cmds.createNode("centerPoint")
    assert cmds.objExists(center_point_node)

def test_node_type():
    center_point_node = cmds.createNode("centerPoint")
    assert cmds.objectType(center_point_node) == "centerPoint"

def test_input_obj_attr_type():
    center_point_node = cmds.createNode("centerPoint", name="any_name")
    obj_exists = cmds.objExists(f"{center_point_node}.input")
    node_type = cmds.attributeQuery("input", node=center_point_node, attributeType=True)

    assert obj_exists and node_type == "matrix"

def test_input_obj_attr_properties():
    center_point_node = cmds.createNode("centerPoint", name="any_name")
    
    is_array = cmds.attributeQuery("input", node=center_point_node, multi=True)
    is_storable = cmds.attributeQuery("input", node=center_point_node, storable=True)
    is_keyable = cmds.attributeQuery("input", node=center_point_node, keyable=True)
    is_readable = cmds.attributeQuery("input", node=center_point_node, readable=True)
    is_writable = cmds.attributeQuery("input", node=center_point_node, writable=True)

    assert is_array
    assert is_storable 
    assert is_keyable
    assert not is_readable
    assert is_writable

def test_output_position_attr_type():
    center_point_node = cmds.createNode("centerPoint", name="any_name")

    obj_exists = cmds.objExists(f"{center_point_node}.outputPosition")
    node_type = cmds.attributeQuery("outputPosition", node=center_point_node, attributeType=True)

    assert obj_exists and node_type == "double3"

def test_output_position_attr_properties():
    center_point_node = cmds.createNode("centerPoint", name="any_name")
    
    is_array = cmds.attributeQuery("outputPosition", node=center_point_node, multi=True)
    is_storable = cmds.attributeQuery("outputPosition", node=center_point_node, storable=True)
    is_keyable = cmds.attributeQuery("outputPosition", node=center_point_node, keyable=True)
    is_readable = cmds.attributeQuery("outputPosition", node=center_point_node, readable=True)
    is_writable = cmds.attributeQuery("outputPosition", node=center_point_node, writable=True)

    assert not is_array
    assert not is_storable 
    assert not is_keyable
    assert is_readable
    assert not is_writable

def test_compute():
    center_point_node = cmds.createNode("centerPoint", name="any_name")
    input_positions = [[0.0, 0.0, 0.0], [0.5, 10.3, 50.8], [-15.5, -8.0, -30.0], [34.4, 56.66, -45.0]]
    expected_result = [4.850, 14.740, -6.050]

    for idx, pos in enumerate(input_positions):
        transform = cmds.createNode("transform")
        cmds.xform(transform, translation=pos, worldSpace=True)
        cmds.connectAttr(f"{transform}.worldMatrix[0]", f"{center_point_node}.input[{idx}]")

    output_transform = cmds.createNode("transform")
    cmds.connectAttr(f"{center_point_node}.outputPosition", f"{output_transform}.t")

    assert cmds.xform(output_transform, query=True, translation=True, worldSpace=True) == expected_result

    

