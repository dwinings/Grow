#Grow

A straightforward puzzle/platformer written in Python/Pygame

##How to play

###Running the Game
In order to run Grow just double-click on `main.py` or type `python main.py` into the command line in the Grow directory. Python2.7 and Pygame for Python2.7 must both be installed on the computer before playing.

###Playing the Game

Upon entering the game the player will be confronted with the main menu. The player can either choose to enter the game immediately or view a small set of instructions on how to play. Once in the game, the controls are as follows:

- WASD or Arrow Keys for movement horizontally relative to the current surface
- F to interact with objects in the game world.
- P to pause
- 1 is the hidden button that will cause the game to advance to the next level and as such it is not reflected in the HUD.

In order to advance to each new level the player must walk over and grow grass on all the dirt (brown surfaces) in the level. 

##Code structure

The code for this game is fairly straightforward. The major pieces of the code can be found in the following files and directories:

- Levels/: contains all of the game levels and pictures of them for fast reference.
- res/: contains all of the graphical resources that the game requires to run.
- gblocks.py: contains all of the definition code for the different block types.
- gcolors.py: contains a few static color definitions
- ginput.py: handles the game input
- glevel.py: contains all of the level loading code
- gmath.py: contains a lonely pythagorean theorem function
- gobjects.py: contains most of the heavy game logic. The player class is defined here and all of the collision detection also happens in here. 
- gscreens.py: contains all of the different game screens(pause, game, menu, etc)
- gui.py: contains all of the user interface classes (buttons and so on)
- main.py: loads some files and starts the whole thing off.



##Credits
###Jonathan Haslow-Hall
- Original and Primary Programmer
- Feature Designer and Implementer
- Asset Contributor

###David Winings
- Mathematical Advisor
- Primary Debugger
- Level Designer
- Git Sensei
- Auxiliary Programmer

###Lucy Niedbala
- External Art Contractor


##Git instructions for group members.


The git repository may be found at `http://github.com/wisp558/Grow`

`git <command> <arguments>`  is the basic form of all git commands.

In order to obtain this repository for use, just run the clone command with the link to the repository, given in the box. Example:

	git clone ssh://git@github.com:wisp558/Grow.git

After doing this, you can code as normal for a bit. When you've made a change, you can then commit: 

	$ git add <changedFiles>
	$ git commit -m "Message"

If you want to tag the commit as a release, use git tag:

	$ git tag v0.001

git tag will tag the last commit. Now that you're done editing the code,you can just go forward and push the commit back to github:

	$ git push origin master

This pushes your local branch (`master`)  to a source (`origin`). You can set the origin with `$ git remote add <source> <link>` but it is already set for you when you use `git clone`.

When you want to pull changes from github back to your local git repository, you can either `clone` again into a different directory, or use `git pull`. (It will automatically pull from the `origin` branch.)
