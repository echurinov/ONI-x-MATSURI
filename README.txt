<<<<<<< HEAD
ONI x MATSURI
Current Stage: Prototype

--------------------------

Build command:
    Run the following script in the project root folder:
        build.bat
    The resulting main.exe will be located in the dist\main\ directory.
    IF THE SCRIPT FAILS, run the following two commands manually (in command prompt as an administrator):
        pip install -r requirements.txt
        pyinstaller --onefile --add-data "assets;assets" main.py --windowed

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