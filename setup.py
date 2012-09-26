from distutils.core import setup
import py2exe
import glob

setup(
	name="chimera_chimera",
	version="1.0",
	description="PyWeek entry",
	author="Scott Hilbert",
	author_email="pyweek@shilbert.com",
	license="BSD",
	
	# make a windows subsystem executable (no console)
	windows=['chimera_pygame.py'],
	
	# pull in necessary data files
	data_files= [
		'chimera_pygame.py',
		'setup.py',
		'Vera.ttf',
		'README.txt',
		#'avbin/avbin.dll',
		'config.ini',
		('images', glob.glob('images/*.png')),
		('levels', glob.glob('levels/*.*')),
		('music', glob.glob('music/*.ogg')),
		('sfx', glob.glob('sfx/*.wav')),
	],
	
	options = {'py2exe': dict(
		excludes=['_ssl', 'pyreadline', 'difflib', 'doctest', 'locale', 'optparse', 'pickle', 'calendar','pdb','doctest','unittest','inspect','popen','Tkinter'],
		packages=['OpenGL','OpenGL.arrays','pygame'],
		#compressed=True,
		bundle_files=1
	)},
	
	zipfile=None,

)