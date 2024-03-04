import pytest
from pytest import fixture
from unittest.mock import Mock
from unittest.mock import patch
import maya.api.OpenMaya as om

import center_point_node as plugin_module
from center_point_node import CenterPointNode

@fixture
def center_point_node():
    return CenterPointNode()

def test_should_not_compute_if_not_dirty(center_point_node):
    plug = CenterPointNode.outputPosAttr
    dataBlock = Mock()
    
    center_point_node.compute(plug, dataBlock)

    dataBlock.outputValue.set3Double.assert_not_called()

def test_should_compute_if_dirty(center_point_node):
    plug = CenterPointNode.outputPosAttr
    dataBlock = Mock()
    outputValue = Mock()
    dataBlock.outputValue.return_value = outputValue
    
    center_point_node.compute(plug, dataBlock)

    outputValue.set3Double.assert_called()

def test_should_set_clean_after_computing(center_point_node):
    plug = CenterPointNode.outputPosAttr
    dataBlock = Mock()
    outputValue = Mock()
    dataBlock.outputValue.return_value = outputValue
    
    center_point_node.compute(plug, dataBlock)

    dataBlock.setClean.assert_called_with(plug)

def test_find_center_point(center_point_node):
    input_positions = [om.MVector(0.0, 0.0, 0.0), 
                       om.MVector(0.5, 10.3, 50.8), 
                       om.MVector(-15.5, -8.0, -30.0), 
                       om.MVector(34.4, 56.66, -45.0)]
    
    expected_result = om.MVector(4.850, 14.740, -6.050)

    result = center_point_node._find_center_point(input_positions)

    assert result == expected_result