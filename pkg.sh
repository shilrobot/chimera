#!/bin/bash
set -o errexit
set -o noclobber
set -o nounset

TMP=tmp/chimera
rm -rf tmp
mkdir -p $TMP $TMP/images $TMP/levels $TMP/music $TMP/sfx
cp config.ini chimera.py README.txt Vera.ttf $TMP
cp images/*.png $TMP/images
cp levels/*.oe{l,p} $TMP/levels
cp sfx/*.wav $TMP/sfx
cp music/*.ogg $TMP/music
cd tmp
zip -r chimera chimera # look into the mirror