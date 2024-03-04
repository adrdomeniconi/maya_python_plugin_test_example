import pytest
from pytest import fixture
from unittest.mock import Mock
from unittest.mock import patch
import maya.api.OpenMaya as om

import center_point_node as plugin_module
from center_point_node import CenterPointNode

def test_should_not_compute_if_not_dirty():
    pass

# def test_should_compute_if_dirty():
#     pass

# def test_should_set_clean_after_computing():
#     pass

# def test_find_center_point():
#     pass