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

def test_register_plugin():
    with patch('maya.api.OpenMaya.MFnPlugin') as mock_mfn_plugin:
        plugin_fn = Mock()
        mock_mfn_plugin.return_value = plugin_fn

        plugin_module.initializePlugin(None)

        plugin_fn.registerNode.assert_called_once_with(CenterPointNode.kTypeName, 
                                                        CenterPointNode.kTypeId, 
                                                        CenterPointNode.creator, 
                                                        CenterPointNode.initialize,
                                                        om.MPxNode.kDependNode)

def test_display_error_if_register_plugin_fails():
    with patch('maya.api.OpenMaya.MFnPlugin') as mock_mfn_plugin, \
         patch('maya.api.OpenMaya.MGlobal') as mock_mglobal:
        
        plugin_fn = Mock()
        error_msg = "error msg"
        plugin_fn.registerNode.side_effect = Exception(error_msg)
        mock_mfn_plugin.return_value = plugin_fn

        plugin_module.initializePlugin(None)
        
        mock_mglobal.displayError.assert_called_with(f"Failed to register node: {CenterPointNode.kTypeName}: {error_msg}")

def test_deregister_plugin():
    with patch('maya.api.OpenMaya.MFnPlugin') as mock_mfn_plugin:
        plugin_fn = Mock()
        mock_mfn_plugin.return_value = plugin_fn

        plugin_module.uninitializePlugin(None)

        plugin_fn.deregisterNode.assert_called_once_with(CenterPointNode.kTypeId)


def test_display_error_if_deregister_plugin_fails():
    with patch('maya.api.OpenMaya.MFnPlugin') as mock_mfn_plugin, \
         patch('maya.api.OpenMaya.MGlobal') as mock_mglobal:
        
        plugin_fn = Mock()
        error_msg = "error msg"
        plugin_fn.deregisterNode.side_effect = Exception(error_msg)
        mock_mfn_plugin.return_value = plugin_fn

        plugin_module.uninitializePlugin(None)
        
        mock_mglobal.displayError.assert_called_with(f"Failed to de-register node: {CenterPointNode.kTypeName}: {error_msg}")

