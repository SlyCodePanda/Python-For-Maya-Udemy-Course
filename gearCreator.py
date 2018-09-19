from maya import cmds

# Default values teeth = 10, length = 0.3.
def createGear( teeth=10, length=0.3 ) :
    """
    This function will create a gear with the given parameters.
    Args:
        teeth: The number of teeth to create
        length: The length of the teeth

    Returns: A tuple of the transform, constructor, and extrude node.

    """
    # Teeth are every alternate face, so spans x 2
    spans = teeth * 2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    sideFaces = range(spans*2, spans*3, 2)

    # Clear any current selection.
    cmds.select(clear=True)

    for face in sideFaces :
        # add=True keeps adding to the selection.
        cmds.select('%s.f[%s]' % (transform, face), add=True)

    # Because this gives us back a list, we have '[0]' on the end to signify the first element of the list.
    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    return transform, constructor, extrude

def changeTeeth( constructor, extrude, teeth=10, length=0.3 ) :
    spans = teeth*2

    cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)

    sideFaces = range(spans*2, spans*3, 2)
    faceNames = []

    for face in sideFaces :
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

    cmds.setAttr('%s.inputComponents' % (extrude), len(faceNames), *faceNames, type="componentList")

    cmds.polyExtrudeFacet(extrude, edit=True, ltz=length)