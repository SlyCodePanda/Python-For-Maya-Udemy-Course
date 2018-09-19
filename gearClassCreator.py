from maya import cmds

class Gear(object) :
    """
    This is a gear object that lets us create and modify a gear.
    Example of use:
        import gearClassCreator as gearCreator
        reload(gearCreator)

        gear = gearCreator.Gear()
        gear.createGear()
        gear.changeTeeth(teeth=12, length=0.4)
    """

    # When we first initialize a new gear, set these values.
    def __init__(self):
        # The init method lets us set default values.
        self.transform = None
        self.extrude = None
        self.constructor = None

    def createGear( self, teeth=10, length=-0.3 ):
        """

        Args:
            teeth: The number of teeth to create.
            length: The length of the teeth.

        Returns:

        """
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)

        sideFaces = range(spans * 2, spans * 3, 2)

        # Clear any current selection.
        cmds.select(clear=True)

        for face in sideFaces:
            # add=True keeps adding to the selection.
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        # Because this gives us back a list, we have '[0]' on the end to signify the first element of the list.
        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]


    def changeTeeth( self, teeth=10, length=0.3 ) :
        spans = teeth*2

        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        sideFaces = range(spans*2, spans*3, 2)
        faceNames = []

        for face in sideFaces :
            faceName = 'f[%s]' % (face)
            faceNames.append(faceName)

        cmds.setAttr('%s.inputComponents' % (self.extrude), len(faceNames), *faceNames, type="componentList")

        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)


