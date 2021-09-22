# ArmA 3 Launch Parameter Generator
Sometimes you don't want to start ArmA 3 from the launcher, for various reasons. However, launching directly won't enable any mods you've installed, you have to add parameters to let them work.

Yes, you could get all the parameters from the launcher's log file. But that's not always going to work, sometimes you just have too many mods that the line containing parameters will be trimmed. It makes sense, but still sucks.

And yes, you could write parameters manually, but are you sure about that?

Introducing this generator! It reads your launcher's presets and logs, it produces parameters that you'll need, it makes your day!

> Note: This tool only supports Windows at this time.

## Usage
Before we get started, you should have Python 3 installed on your PC. [Go get it](https://www.python.org/downloads/) if you haven't already.

Also, make sure you have started the game via the launcher once.

1. Download this repo as ZIP. See that big green button? Click it and you'll know where to go. (Sure, you could also clone this repo.)
2. Extract that ZIP file.
3. Fire up your command prompt, with `Win + R` and enter `cmd`.
4. Use `cd` to go to the directory where you've just extracted.
5. Enter `python .` and follow what it says. (**Remember there's a trailing dot in the command**)
