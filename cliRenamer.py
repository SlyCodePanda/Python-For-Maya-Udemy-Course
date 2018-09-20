import argparse
import re
import os
import shutil

def main():
    """
        This is the function that gets run by default when this module is executed.
        It is common convention to call this first function 'main' but it can be called anything you like
    """

    # First lets create a new parser to parse the command line arguments
    # The arguments we're giving it are ones that will be displayed when a user incorrectly uses your tool or if they ask for help
    parser = argparse.ArgumentParser(description="This is a batch renamer",
                                     usage="To replace all files with hello with goodbye instead: python cliRenamer.py hello goodbye")

    # We'll add two positional arguments. These must be given
    parser.add_argument('inString', help="The word to replace")
    parser.add_argument('outString', help="The word to replace it with")

    # Then we'll add some keyword arguments. Like in python functions, they default to a value so are optional
    # The first one is set to store_true, which means it is False by default but if provided will be set to True
    # Therefore you don't provide a value to it.
    parser.add_argument('-d', '--duplicate',
                        help="Whether to duplicate or replace in spot",
                        action='store_true')
    parser.add_argument('-r', '--regex',
                        help="Whether the patterns are regex or not",
                        action='store_true')
    # This last argument doesn't say store true, which means a value must be given for it, or it will default to None.
    parser.add_argument('-o', '--out', help="The output location defaults to here")

    # Finally we tell the parser to parse the arguments from the command line
    args = parser.parse_args()
    # We use these arguments to provide input to our rename function
    rename(args.inString, args.outString, duplicate=args.duplicate, outDirectory=args.out, regex=args.regex)


def rename(inString, outString, duplicate=True, inDirectory=None, outDirectory=None, regex=False):
    """
       A simple function to rename all the given files in a given directory
       Args:
           inString:  the input string to find and replace
           outString: the output string to replace it with
           duplicate: Whether we should duplicate the renamed files to prevent writing over the originals
           inDir: what the directory we should operate in
           outDir: the directory we should write to.
           regex: Whether we should use regex instead of simple string replace
    """

    # If no input directory is provided, we'll use the current working directory that the script was called from.
    if not inDirectory:
        inDirectory = os.getcwd()

    # If not output directory is provided we'll use the same directory as the current working directory.
    if not outDirectory:
        outDirectory = inDirectory

    # It is possible that the output directory is provided in relative terms ("../../")
    # abspath will convert this to a real path.
    outDirectory = os.path.abspath(outDirectory)

    # It is also possible that the output directory does not exist.
    # We should error early if it does not exist.
    if not os.path.exists(outDirectory):
        raise IOError("%s does not exist" % outDirectory)
    if not os.path.exists(inDirectory):
        raise IOError("%s does not exist" % inDirectory)

    # Finally we loop through all the files in the current directory
    for f in os.listdir(inDirectory):
        # We will start by skipping over files that start with a dot.
        # This is a sign that they are hidden and should not be modified.
        if f.startswith('.'):
            continue

        # If we are told to use regex, then lets use the regex module to replace the string.
        if regex:
            name = re.sub(inString, outString, f)
        else:
            # Otherwise lets just use regular string replace.
            name = f.replace(inString, outString)

        # Finally if the name is identical, then don't bother renaming it because it's wasted time.
        if name == f:
            continue

        # Now lets construct the full paths to copy from since we only currently have the name of the actual file.
        src = os.path.join(inDirectory, f)
        dest = os.path.join(outDirectory, name)

        # If we're told to duplicate, we'll use the shutil library and its' copy2 function to copy the file.
        if duplicate:
            shutil.copy2(src, dest)
        else:
            # Otherwise we'll just use the os module to rename the file.
            os.rename(src, dest)



# If our namespace is main, run main().
# So the main function will only be run if we call this script directly, rather than if we just import it.
if __name__ =='__main__':
    main()