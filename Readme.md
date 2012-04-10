#Grow

A straightforward puzzle/platformer written in Python/Pygame 

##Git instructions for group members.

`git \<command> \<arguments>`  is the basic form of all git commands.

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

When you want to pull changes from github back to your local git repository, you can either `clone` again into a different directory, or use `git pull`. (It will automatically pull from the `origin` branch.
