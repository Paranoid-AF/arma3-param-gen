# ArmA 3 Launch Parameter Generator
Sometimes you don't want to start ArmA 3 from the launcher, for various reasons. However, launching directly won't enable any mods you've installed, you have to add parameters to let them work.

Sometimes you just have too many mods, which is going to make launch parameters being too long that [Windows can't even handle](https://docs.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/command-line-string-limitation). This tool is going to shorten it by making symbolic links when parameters getting too long.

Yes, you could get all the parameters from the launcher's log file. But that's tedious, especially when you have a lot of presets. Not to mention that too many mods may result in some mods not being loaded, as said above.

And yes, you could write parameters manually, but are you sure about that?

Introducing this tool! It reads your launcher's presets and logs, it produces parameters that you'll need, it shortens parameter if needed, it makes your day!

> Note: This tool only supports Windows at this time.

## Usage
Before we get started, you should have Python 3 installed on your PC. [Go get it](https://www.python.org/downloads/) if you haven't already.

Also, make sure you have started the game via the launcher once.

1. [Download](https://github.com/Paranoid-AF/arma3-param-gen/archive/refs/heads/master.zip) this tool.
2. Extract that ZIP file.
3. Double-click `PLAY.bat`.
4. Follow what it says.

![Screenshot](https://github.com/Paranoid-AF/arma3-param-gen/raw/master/screenshot.png)