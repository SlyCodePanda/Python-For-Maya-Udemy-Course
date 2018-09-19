from maya import cmds

# A dictionary with all the suffixes.
SUFFIXES = {
    "mesh" : "geo",
    "joint" : "jnt",
    "camera" : None,
    "ambientLight" : "lgt"
}

DEFAULT_SUFFIX = "grp"

def rename(selection=False) :
    # Doc string (what will be returned when someone calls 'help' on the rename function).
    """
    This function will rename any objects to have the correct suffix.
    Args:
        selection: Whether or not we use the current selection.

    Returns:
        A list of all the objects we operate on.
    """
    objects = cmds.ls(selection=selection, dag=True, long=True)

    # If the user sets selection to True and If there are no objects selected, raise an error.
    if selection and not objects :
        raise RuntimeError("You don't have anything selected!")

    # Sort the objects by shortest to longest
    objects.sort(key=len, reverse=True)

    # Loops and assigns a suffix to the objects in the outliner. Making sure to skip cameras.
    for obj in objects:
        # The name will be something like grandparent|parent|child
        # We just want the child part of the name, so we split using the | character which gives us a list of
        # ['grandparent', 'parent', 'child']
        # We need to get the last item in the list, so we use [-1]. This means we go backwards through the list and
        # pick the next item, which would therefore be the last item.
        shortName = obj.split("|")[-1]

        # Get the object type of children. If none, make it an empty list.
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        # Depending on object type, give it a certain suffix name.
        # If the dict donesn't have the suffix we are looking for, assume it is a group and return the "grp" suffix.
        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        # If the suffix is not true (None), continue and skip the rest of the logic.
        if not suffix:
            continue

        # If suffix has already been added to an object, skip it.
        if obj.endswith('_' + suffix) :
            continue

        newName = "%s_%s" % (shortName, suffix)
        # Rename objects to newName.
        cmds.rename(obj, newName)

        # Gives us back the index value of the object in the list.
        index = objects.index(obj)
        # Replace the object in the list with it's new name.
        objects[index] = obj.replace(shortName, newName)

    return objects
