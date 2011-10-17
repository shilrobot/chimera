CHIMERA CHIMERA
A PyWeek September 2011 entry

AUTHOR
======
CODE + ART: Scott Hilbert: http://www.shilbert.com
MUSIC: Kevin MacLeod: http://http://www.incompetech.com/
SOUND FX: Generated with BFXR: http://www.bfxr.net/

HOW TO RUN
==========

WINDOWS:

1) Just run 'chimera.exe'.

If you get an error about not being able to load avbin.dll
(hopefully you don't!) you can set 'music=0' in the config file
to play without music.

LINUX:

1) Ensure that you have the following programs and libraries installed:

     python 2.6+ (but not 3.x)
     pyglet 1.1.2 or 1.1.4
     avbin
     pyopenal (recommended; otherwise pyglet uses ALSA for sound which is
               best described as 'crashy')
    
   Most recent Debian and Ubuntu machines come with python 2.6+.
   You can check what version of python you have by running 'python -V'.
   
   To install the rest:
    
     $ sudo apt-get install python-pyglet python-openal libavbin0
     
   The install procedure will vary for other linux distributions.

2) Run 'python chimera.py'. 

MAC:

1) Download and install the pyglet DMG from here:

     http://www.pyglet.org/download.html

2) If you are on Snow Leopard, from a bash shell in the same directory
   as this README.txt file:

     $ VERSIONER_PYTHON_PREFER_32_BIT=yes python chimera.py

   Otherwise, if you are on Lion:

     $ arch -i386 /usr/bin/python2.6 chimera.py

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
you can modify the 'scale' value in graphics.ini to a smaller number, like 1 or 2.
This may also help remove graphics artifacts.

LICENSE
=======
Source code and copyright (C) 2011 Scott Hilbert

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
