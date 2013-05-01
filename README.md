ruzzleSolver.py
=============

ruzzleSolver is a little python script that aims to find all (at least most of) the solution of a Ruzzle game, given the 16 letters.

It comes in a textual version as well as in a version with a GUI, built with Tkinter.
Both are still in a beta phase, since they miss a lot of important features such as input validation and so on.

One of the biggest flaws that needs to be fixed is that the dictionary file is in some points different from the one used in-game: as a consequence, some words found by the script will not be valid when put into Ruzzle and viceversa, the script will not find some words whreas Ruzzle will.

I hope to add support to more dictionaries in the future.

