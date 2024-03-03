import maya.api.OpenMaya as om
import maya.cmds as cmds

maya_useNewAPI = True

class CenterPointNode(om.MPxNode):

    kTypeName = "centerPoint"
    kTypeId = om.MTypeId(0x0007f7f9)

    inputObjectsAttr = None
    outputPosAttr = None

    @classmethod
    def defineAttributes(cls):
        numericFn = om.MFnMatrixAttribute()
        cls.inputObjectsAttr = numericFn.create("input", "in", om.MFnMatrixAttribute.kDouble)
        numericFn.array = True
        numericFn.storable = True
        numericFn.keyable = True
        numericFn.readable = False
        numericFn.writable  = True

        cls.addAttribute(cls.inputObjectsAttr)
        
        numericAttrFn = om.MFnNumericAttribute()
        cls.outputPosAttr = numericAttrFn.create("outputPosition", "op", om.MFnNumericData.k3Double)
        numericAttrFn.storable = False
        numericAttrFn.writable = False
        numericAttrFn.readable = True

        cls.addAttribute(cls.outputPosAttr)

        cls.attributeAffects(cls.inputObjectsAttr, cls.outputPosAttr)

    def __init__(self):
        super().__init__()
    
    @classmethod
    def creator(cls):
        return CenterPointNode()
    
    @classmethod
    def initialize(cls):
        cls.defineAttributes()

    def compute(self, plug, dataBlock):
        if not self.__is_dirty(plug):
            pass

        inputDataHandle = dataBlock.inputArrayValue(CenterPointNode.inputObjectsAttr)

        positions = []
        while not inputDataHandle.isDone():
            matrixDataHandle = inputDataHandle.inputValue()
            worldMatrix = matrixDataHandle.asMatrix()

            transformationMatrix = om.MTransformationMatrix(worldMatrix)
            translation = transformationMatrix.translation(om.MSpace.kWorld)

            positions.append(translation)

            inputDataHandle.next()

        center_point = self.__find_center_point(positions)
        
        outputHandle = dataBlock.outputValue(self.outputPosAttr)
        outputHandle.set3Double(center_point.x, center_point.y, center_point.z)
        dataBlock.setClean(plug)

    def __is_dirty(self, plug):
        return plug == self.outputPosAttr
    
    def __find_center_point(self, positions):
        sum_vector = om.MVector(0, 0, 0)
        for pos in positions:
            sum_vector += pos
        
        center_point = sum_vector / len(positions)

        return center_point
    

def initializePlugin(plugin):
    vendor = "Adriano Domeniconi" 
    version = "0.0.1"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerNode(CenterPointNode.kTypeName, 
                                  CenterPointNode.kTypeId, 
                                  CenterPointNode.creator, 
                                  CenterPointNode.initialize,
                                  om.MPxNode.kDependNode)
    except Exception as e:
        om.MGlobal.displayError(f"Failed to register node: {CenterPointNode.kTypeName}: {e}")


def uninitializePlugin(plugin):
    plugin_fn = om.MFnPlugin(plugin)

    try:
        plugin_fn.deregisterNode(CenterPointNode.kTypeId)
    except Exception as e:
        om.MGlobal.displayError(f"Failed to de-register node: {CenterPointNode.kTypeName}: {e}")

def __setup_test_scene():
    centerPointNode = cmds.createNode("centerPoint")
    
    sphere1 = cmds.polySphere()[0]
    sphere2 = cmds.polySphere()[0]
    sphere3 = cmds.polySphere()[0]
    sphere4 = cmds.polySphere()[0]

    cmds.connectAttr(f"{sphere1}.worldMatrix[0]", f"{centerPointNode}.input[0]")
    cmds.connectAttr(f"{sphere2}.worldMatrix[0]", f"{centerPointNode}.input[1]")
    cmds.connectAttr(f"{sphere3}.worldMatrix[0]", f"{centerPointNode}.input[2]")
    cmds.connectAttr(f"{centerPointNode}.outputPosition", f"{sphere4}.t")

if __name__ == "__main__":
    plugin_name = "center_point_node.py"

    cmds.file(new=True, force=True)
    
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred('__setup_test_scene()')
    


    