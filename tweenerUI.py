from maya import cmds


def tween(percentage, obj=None, attrs=None, selection=True) :

    # If obj is not given and selection is set to False, error early.
    if not obj and not selection :
        raise ValueError("No object given to tween.")

    # If no obj is specified, get it from the first selection.
    if not obj :
        obj = cmds.ls(selection=True)[0]

    if not attrs :
        # List all the attributes on the object that are keyable.
        attrs = cmds.listAttr(obj, keyable=True)

    # Get current frame.
    currentTime = cmds.currentTime(query=True)

    for attr in attrs :
        # Construct the full name of the attribute with its object.
        attrFull = '%s.%s' % (obj, attr)
        # Get the keyframes of the attribute on this object.
        keyFrames = cmds.keyframe(attrFull, query=True)

        # If there are no keyframes, then continue.
        if not keyFrames :
            continue

        # Without using list comprehension.
        previousKeyFrames = []
        for frame in keyFrames :
            if frame < currentTime :
                previousKeyFrames.append(frame)

        # With using list comprehension.
        laterKeyframes = [frame for frame in keyFrames if frame > currentTime]

        # If there are no previous keyframes, and there are no later keyframes, then continue.
        if not previousKeyFrames and not keyFrames :
            continue

        if previousKeyFrames :
            # Go through all the frames in the previousKeyFrames list and get the maximum value.
            previousFrame = max(previousKeyFrames)
        else :
            previousFrame = None

        nextFrame = min(laterKeyframes) if laterKeyframes else None

        if not previousFrame or not nextFrame :
            continue

        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        difference = nextValue - previousValue
        weightedDifference = (difference * percentage) / 100.0
        currentValue = previousValue + weightedDifference

        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)

class TweenWindow( object ) :

    windowName = "TweenerWindow"

    def show(self) :

        # If a window with the window name "Tweener Window" already exists, delete UI. This stops you from being able
        # to open multiple tweener windows at once.
        if cmds.window(self.windowName, query=True, exists=True) :
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()

    def buildUI(self) :
        column = cmds.columnLayout()

        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    # the *args parameter means that any extra arguments given to this function will be stored inside 'args'.
    def reset(self, *args) :
        cmds.floatSlider(self.slider, edit=True, value=50)

    def close(self, *args) :
        cmds.deleteUI(self.windowName)