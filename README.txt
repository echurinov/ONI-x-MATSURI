ONI x MATSURI
Current Stage: Prototype

--------------------------

How to build:
	Using build.bat:
	    1. Run the build.bat script. This will download and install all requirements, then generate the installer.
	        If this fails, use the manual build method below.

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
In this prototype, most of the back-end has been implemented with at
least one instance of much of the core functionality. This includes:
- Entity and component system
- Sprite rendering and basic animation
- Scene switching (Start, Game, and Game Over screens)
- Player Controller
- Taking and dealing damage
- A level component builder (to be utilized in procedural generation)
- Enemy system
- Physics system