ONI x MATSURI
Current Stage: Finished

--------------------------

How to build:
	Using build.bat:
	    1. Run the build.bat script. This will download and install all requirements, then generate the installer.
	     Follow the on-screen instructions to install NSIS (a requirement for building the installer).
	     The finished installer will be build/nsis/ONI-x-MATSURI_1.0.exe.
	     This installer will create a Start Menu entry, use this to launch the game.

	     ***Make sure that your screen resolution is at full HD (1920x1080) and scaling in Windows is set to 100%.***

	     If this batch file fails, use the manual build method below.

	Manually:
        1. Install NSIS: http://nsis.sourceforge.net/Download
        2. Install pynsist from pip with the following command:
            pip install pynsist
        3. Run the following command to generate the installer:
            pynsist installer.cfg
        3a. If pynsist isn't found, run the following alternative command:
            python -m nsist installer.cfg

--------------------------

GitHub Repository: https://github.com/echurinov/ONI-x-MATSURI

--------------------------

PROJECT DESCRIPTION:

ONI x MATSURI is a side-scrolling platformer where the main player must
fight and progress through a Japanese summer festival invaded by Oni.
