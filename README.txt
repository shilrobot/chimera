CHIMERA CHIMERA
A PyWeek September 2011 entry

AUTHOR
======
CODE + ART: Scott Hilbert: http://www.shilbert.com
MUSIC: Kevin MacLeod: http://http://www.incompetech.com/
SOUND FX: Generated with BFXR: http://www.bfxr.net/
FONT: Bitstream Vera by Bitstream, Inc.: http://www-old.gnome.org/fonts/

REQUIREMENTS
============
Python 2.6+ (not 3.x): http://www.python.org/download/
Pygame: http://www.pygame.org/download.shtml
PyOpenGL: http://pyopengl.sourceforge.net/documentation/installation.html

Tested combinations:
Windows 7 x64, Python 2.7.3 (32-bit), pygame 1.9.1release, PyOpenGL 3.0.2b2
Ubuntu 10.04 x64, Python 2.6.5, pygame 1.9.1release, PyOpenGL 3.0.0
OS X 10.8 Mountain Lion, Python 2.7.3, pygame 1.9.1release, PyOpenGL 3.0.2

HOW TO RUN
==========

WINDOWS:

1) Install python, pygame and PyOpenGL

2) Run chimera.py

LINUX:

1) Ensure that you have the required libraries.

   Most recent Debian and Ubuntu machines come with python 2.6+.
   You can check what version of python you have by running 'python -V'.
   
   To install the rest:
    
     $ sudo apt-get install python-pygame python-opengl
     
   The install procedure will vary for other linux distributions.

2) Run 'python chimera.py'. 

MAC (last tested on Mountain Lion):

1) Install python 2.7 for Mac from http://www.python.org.
   Run the "Update Shell Profile.command" in Applications/Python2.7.

2) Install pygame from http://www.pygame.org/download.shtml.

   As of this writing, the appropriate package is:
   http://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg
   This is the 32-bit installer for python 2.7.

3) Install PyOpenGL using pip or easy_install.

4) If you are on Lion or Mountain Lion:

     $ arch -i386 python chimera.py

   If you are on Snow Leopard, from a bash shell in the same directory
   as this README.txt file:

     $ VERSIONER_PYTHON_PREFER_32_BIT=yes python chimera.py

   I have not tried earlier versions of OS X.
   
CONTROLS
========
F1 - Help
LEFT/RIGHT - Move
SPACE - Jump, or fly (if you are part eagle)
D - Dig (if you are part mole. use LEFT/RIGHT/UP/DOWN to aim before digging.)
UP/DOWN - Swim (if you are part fish; everything else just floats)
R - Restart level
ESC - Quit game entirely

OTHER TIPS
============
If you have a screen that is smaller than the default size (3x magnification, ie 960x720)
you can modify the 'scale' value in config.ini to a smaller number, like 1 or 2.
This may also help remove graphics artifacts.

LICENSE
=======
Source code and copyright (C) 2011 Scott Hilbert

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
