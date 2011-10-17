import pyglet
# the "go fast" button
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.window import key
from pyglet.text import Label
import math
import time 
import os
from xml.etree.ElementTree import parse
import random
import ConfigParser

def get_root():
	from pyglet.resource import get_script_home
	root = get_script_home()
	if root == '':
		root = '.'
	return root
	
def vfs_path(p):
	return os.path.join(FS_ROOT, p)
		
FS_ROOT = get_root()
	
SCALE = 3
ENABLE_SFX = 1
ENABLE_MUSIC = 1


cfg = ConfigParser.ConfigParser()
try:
	cfg.read(vfs_path('config.ini'))
	SCALE = cfg.getint('graphics','scale')
	if SCALE < 1:
		SCALE = 1
	ENABLE_SFX = cfg.getboolean('audio','sfx')
	ENABLE_MUSIC = cfg.getboolean('audio','music')
except:
	print 'Failed to read config.ini'
	import traceback as tb
	tb.print_exc()

if ENABLE_MUSIC:
	music = pyglet.media.load(vfs_path('music/just_nasty.ogg'),streaming=True)
	player = pyglet.media.Player()
	player.queue(music)
	player.eos_action = player.EOS_LOOP
	player.play()

window = pyglet.window.Window(320*SCALE, 240*SCALE, caption='Chimera Chimera')
TEXTURES = {}

class DummySound(object):
	def play(self):
		pass

def get_sfx(name):
	if ENABLE_SFX:
		return pyglet.media.load(vfs_path('sfx/'+name+'.wav'), streaming=False)
	else:
		return DummySound()

SFX_JUMP = get_sfx('jump')
SFX_HIJUMP = get_sfx('hijump')
SFX_MUTATE = get_sfx('mutate')
SFX_SPLASH = get_sfx('splash')
SFX_FLAP = get_sfx('flap')
SFX_WIN = get_sfx('win')
SFX_DIG = get_sfx('dig')

def get_tex(name):
	if name not in TEXTURES:
		tex = pyglet.image.load(vfs_path('images/'+name)).get_texture()
		TEXTURES[name] = tex
		glBindTexture(tex.target, tex.id)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glBindTexture(tex.target, 0)
	return TEXTURES[name]

TILEMAP_TEX = get_tex('tiles.png')

TILE_EMPTY = "TILE_EMPTY"
TILE_DIRT = "TILE_DIRT"
TILE_DIRT_HOLE = "TILE_DIRT_HOLE"
TILE_CONCRETE = "TILE_CONCRETE"
TILE_WATER = "TILE_WATER"
TILE_START = "TILE_START"
TILE_EXIT = "TILE_EXIT"
TILE_SPAWN_BEAR = "TILE_SPAWN_BEAR"
TILE_SPAWN_MOLE = "TILE_SPAWN_MOLE"
TILE_SPAWN_FISH = "TILE_SPAWN_FISH"
TILE_SPAWN_FISH_WATER = "TILE_SPAWN_FISH_WATER"
TILE_SPAWN_KANGAROO = "TILE_SPAWN_KANGAROO"
TILE_SPAWN_EAGLE = "TILE_SPAWN_EAGLE"

TILE_SIZE = 16

TILE_DICT = {
	TILE_DIRT: (0,0),
	TILE_DIRT_HOLE: (1,0),
	TILE_WATER: (0,1),
	TILE_CONCRETE: (0,2),
	TILE_START: (0,3),
	TILE_EXIT: (0,4),
	TILE_SPAWN_BEAR: (2,0),
	TILE_SPAWN_MOLE: (2,1),
	TILE_SPAWN_FISH: (2,2),
	TILE_SPAWN_FISH_WATER: (3,2),
	TILE_SPAWN_KANGAROO: (2,3),
	TILE_SPAWN_EAGLE: (2,4),
}

TILEMAP_SIZE = 256

SPECIES_BEAR="SPECIES_BEAR"
SPECIES_MOLE="SPECIES_MOLE"
SPECIES_FISH="SPECIES_FISH"
SPECIES_KANGAROO="SPECIES_KANGAROO"
SPECIES_EAGLE="SPECIES_EAGLE"

SPECIES_IDX = {
	SPECIES_BEAR: 0,
	SPECIES_MOLE: 1,
	SPECIES_FISH: 2,
	SPECIES_KANGAROO: 3,
	SPECIES_EAGLE: 4,
}

ALL_SPECIES = list(SPECIES_IDX.keys())

SPECIES_NAMES = {
	(SPECIES_BEAR, SPECIES_BEAR): 'BEAR',
	(SPECIES_BEAR, SPECIES_MOLE): 'MOLEBEAR',
	(SPECIES_BEAR, SPECIES_FISH): 'BEARFISH',
	(SPECIES_BEAR, SPECIES_KANGAROO): 'KANGABEAR',
	(SPECIES_BEAR, SPECIES_EAGLE): 'EAGLEBEAR',
	
	(SPECIES_MOLE, SPECIES_MOLE): 'MOLE',
	(SPECIES_MOLE, SPECIES_FISH): 'MOLEFISH',
	(SPECIES_MOLE, SPECIES_KANGAROO): 'MOLE-A-ROO',
	(SPECIES_MOLE, SPECIES_EAGLE): 'EAGLEMOLE',
	
	(SPECIES_FISH, SPECIES_FISH): 'FISH',
	(SPECIES_FISH, SPECIES_KANGAROO): 'FISHEROO',
	(SPECIES_FISH, SPECIES_EAGLE): 'EAGLEFISH',
	
	(SPECIES_KANGAROO, SPECIES_KANGAROO): 'KANGAROO',
	(SPECIES_KANGAROO, SPECIES_EAGLE): 'EAGLEROO',
	
	(SPECIES_EAGLE, SPECIES_EAGLE): 'EAGLE'
}

def clamp(x,min,max):
	if min > max:
		min,max = max,min
	if x < min:
		return min
	elif x > max:
		return max
	else:
		return x

def lerp(x,a,b):
	return a + (b-a)*float(x)

def lerp_clamp(x,a,b):
	return clamp(lerp(x,a,b),a,b)
		
def draw_subrect(tex, x, y, w=-1, h=-1, sx=0, sy=0, flip_x=False, begin=True):
	if begin:
		glEnable(tex.target)
		glBindTexture(tex.target, tex.id)
		glBegin(GL_QUADS)
	if w < 0:
		w = tex.width
	if h < 0:
		h = tex.height
	u0 = float(sx)/tex.width
	u1 = float(sx+w)/tex.width
	v0 = 1-float(sy)/tex.height
	v1 = 1-float(sy+h)/tex.height
	if flip_x:
		u0,u1 = u1,u0
			
	x0 = round(x*SCALE)-0.1
	x1 = x0+(w*SCALE)
	y0 = round(y*SCALE)-0.1
	y1 = y0+(h*SCALE)
	if w == 320 and h == 240:
		print x0, x1, y0, y1
		print u0, u1, v0, v1
	#print u0,v0,u1,v1,x0,y0,x1,y1
	glTexCoord2f(u0,v0)
	glVertex2f(x0,y0)
	glTexCoord2f(u1,v0)
	glVertex2f(x1,y0)
	glTexCoord2f(u1,v1)
	glVertex2f(x1,y1)
	glTexCoord2f(u0,v1)
	glVertex2f(x0,y1)
	if begin:
		glEnd()

class Rect:
	def __init__(self, x=0, y=0, w=0, h=0):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
	@property
	def left(self):
		return self.x
		
	@property
	def right(self):
		return self.x+self.w
		
	@property
	def top(self):
		return self.y
		
	@property
	def bottom(self):
		return self.y+self.h
		
	def normalized(self):
		x2,y2 = self.x, self.y
		w2,h2 = self.w, self.h
		if w2 < 0:
			x2 = x2 + w2
			w2 = abs(w2)
		if h2 < 0:
			h2 = h2 + h2
			h2 = abs(h2)
		return Rect(x2,y2,w2,h2)
		
	def overlap(self,other):
		if (self.right < other.left or 
			other.right < self.left or
			self.top > other.bottom or
			other.top > self.bottom):
			return False
		return True
		
	def __repr__(self):
		return 'Rect(%s,%s,%s,%s)' % (self.x, self.y, self.w, self.h)
		
EDGE_LEFT = "EDGE_LEFT"
EDGE_RIGHT = "EDGE_RIGHT"
EDGE_TOP = "EDGE_TOP"
EDGE_BOTTOM = "EDGE_BOTTOM"
		
class GameObject(object):
	def __init__(self, world):
		self.world = world
		self.killme = False
		self.x = 0
		self.y = 0
		self.priority = 0
		self.visible = True
		
	def update(self, delta):
		pass
		
	def draw(self):
		pass
		
class Map(GameObject):
	def __init__(self,world,filename):
		super(Map, self).__init__(world)
		self.priority = -100
		self.start_x = 0
		self.start_y = 0
		self.exit_x = 0
		self.exit_y = 0
		self.exit_flash_counter = 0
		self.load(filename)
		self.displaylist = None
		self.water_timer = 0
		self.water_frame = 0
		
	def resize(self,w,h):
		assert w > 0 and h > 0
		self.width = w
		self.height = h
		self._tiles = [TILE_EMPTY]*w*h		
		
	def load(self, filename):
		with open(vfs_path('levels/%s.oel'%filename),'rt') as f:
			xml = parse(f)
			w = int(xml.findtext('width'))/TILE_SIZE
			h = int(xml.findtext('height'))/TILE_SIZE
			self.resize(w,h)
			tiles = xml.find('tilesAbove')
			for tile in tiles.findall('tile'):
				tx = int(tile.attrib['tx'])/TILE_SIZE
				ty = int(tile.attrib['ty'])/TILE_SIZE
				cx = int(tile.attrib['x'])/TILE_SIZE
				cy = int(tile.attrib['y'])/TILE_SIZE
				for (k,v) in TILE_DICT.iteritems():
					if (tx,ty) == v:
						self.load_tile(cx,cy,k)
						break
					
	def load_tile(self,x,y,tile):
		if not self.valid_tile(x,y):
			return
		if tile is TILE_START:
			self.start_x = x
			self.start_y = y
			# do not actually set a tile
		elif tile is TILE_SPAWN_BEAR:
			self.spawn(x,y,SPECIES_BEAR)
		elif tile is TILE_SPAWN_MOLE:
			self.spawn(x,y,SPECIES_MOLE)
		elif tile is TILE_SPAWN_FISH:
			self.spawn(x,y,SPECIES_FISH)
		elif tile is TILE_SPAWN_FISH_WATER:
			self.set_tile(x,y,TILE_WATER)
			self.spawn(x,y,SPECIES_FISH)
		elif tile is TILE_SPAWN_KANGAROO:
			self.spawn(x,y,SPECIES_KANGAROO)
		elif tile is TILE_SPAWN_EAGLE:
			self.spawn(x,y,SPECIES_EAGLE)
		else:
			if tile is TILE_EXIT:
				self.exit_x = x
				self.exit_y = y
			self.set_tile(x,y,tile)
			
	def spawn(self,x,y,species):
		animal = WildAnimal(self.world, species)
		animal.x = (x+0.5)*TILE_SIZE
		animal.y = (y+1)*TILE_SIZE - 0.1
		self.world.add(animal)
		
	def valid_tile(self,x,y):
		return x >= 0 and x < self.width and y >= 0 and y < self.height
		
	def get_tile(self,x,y,default=None):
		if self.valid_tile(x,y):
			return self._tiles[x + y*self.width]
		elif default is not None:
			return default
		else:
			assert False
		
	def set_tile(self,x,y,tile):
		assert self.valid_tile(x,y)
		self._tiles[x +y*self.width] = tile
		
	def update(self,delta):
		self.exit_flash_counter = (self.exit_flash_counter + 1)%4
		self.water_timer += delta*10
		while self.water_timer >= TILE_SIZE:
			self.water_timer -= TILE_SIZE
		
	def draw(self):
		if self.displaylist is None:
			self.displaylist = glGenLists(1)
			glNewList(self.displaylist, GL_COMPILE)
			glBindTexture(GL_TEXTURE_2D, TILEMAP_TEX.id)
			glBegin(GL_QUADS)
			for y in range(self.height):
				for x in range(self.width):
					t = self._tiles[x+y*self.width]
					if t == TILE_EMPTY:
						continue
					if t not in TILE_DICT:
						continue
					if self.is_water_surface(x,y):
						continue
					(tx,ty) = TILE_DICT[t]
					draw_subrect(TILEMAP_TEX,
								x*TILE_SIZE, y*TILE_SIZE,
								TILE_SIZE, TILE_SIZE,
								tx*TILE_SIZE, ty*TILE_SIZE, begin=False)
			glEnd()		
			glEndList()
		glCallList(self.displaylist)
		
		if self.world.won and self.exit_flash_counter < 2:
			draw_subrect(TILEMAP_TEX, self.exit_x*TILE_SIZE,
							self.exit_y*TILE_SIZE,
							TILE_SIZE,
							TILE_SIZE,
							0, 5*TILE_SIZE)
							
		
		glBindTexture(GL_TEXTURE_2D, TILEMAP_TEX.id)
		glBegin(GL_QUADS)
		for y in range(self.height):
			for x in range(self.width):
				if self.is_water_surface(x,y):
					draw_subrect(TILEMAP_TEX,
								x*TILE_SIZE, y*TILE_SIZE-1,
								TILE_SIZE, TILE_SIZE+1,
								(4*TILE_SIZE) + round(self.water_timer), 1*TILE_SIZE-1, begin=False)
		glEnd()	
		
	def is_water_surface(self,x,y):
		t = self.get_tile(x,y)
		return ( t == TILE_WATER and self.get_tile(x,y-1,TILE_CONCRETE) not in [TILE_CONCRETE, TILE_DIRT, TILE_WATER])		
						
	def visit_tiles(self,rect):
		minX = int(math.floor(float(rect.left)/TILE_SIZE))
		minY = int(math.floor(float(rect.top)/TILE_SIZE))
		maxX = int(math.floor(float(rect.right)/TILE_SIZE))
		maxY = int(math.floor(float(rect.bottom)/TILE_SIZE))
		for y in range(minY, maxY+1):
			for x in range(minX, maxX+1):
				yield (x,y)
		
	def to_tile_coords(self,x,y):
		tx = int(math.floor(x/TILE_SIZE))
		ty = int(math.floor(y/TILE_SIZE))
		return (tx,ty)	
		
	def discard_list(self):
		if self.displaylist is not None:
			glDeleteLists(self.displaylist, 1)
			self.displaylist = None
			
			
ANIMALS_TEX = get_tex('animals.png')
ANIMALS_TEX_FLASH = get_tex('animals_flash.png')



			
def draw_species(species,x,y,face_right=True,flash=False):
	if len(species) == 1:
		src_x = SPECIES_IDX[species[0]]
		src_y = src_x
	else:
		src_x = SPECIES_IDX[species[0]]
		src_y = SPECIES_IDX[species[1]]
		if src_y > src_x:
			src_x,src_y = src_y,src_x
		
	draw_subrect(ANIMALS_TEX_FLASH if flash else ANIMALS_TEX, x-8, y-16, 16,16, src_x*16,src_y*16,flip_x = not face_right)
		
		
class WildAnimal(GameObject):
	def __init__(self, world, species):
		super(WildAnimal, self).__init__(world)
		self.species = species
		self.face_right = True
		self.priority = -1
		self.world.wild_animals.append(self)
		self.vy = 0
		self.on_ground = False
		
	def update(self, delta):
		speed = 30
		if self.face_right:
			newx = self.x + speed*delta
		else:
			newx = self.x - speed*delta
		
		if not self.solid_at(self.x,self.y+0.1):
			newy = self.y + 80*delta
			for n in range(5):
				if self._can_move_to(self.x,newy):
					self.y = newy
					break
				else:
					newy = (self.y + newy)*0.5
					
		elif not self.solid_at(newx,self.y+2):
			self.face_right = not self.face_right
		else:			
			if self._can_move_to(newx,self.y):
				self.x = newx
			else:
				self.face_right = not self.face_right
			
	def solid_at(self,x,y):
		map = self.world.map
		tx,ty = map.to_tile_coords(x,y)
		if self.species == SPECIES_FISH and map.get_tile(tx,ty,TILE_CONCRETE) == TILE_WATER:
			return True			
		return self.species == SPECIES_EAGLE or map.get_tile(tx,ty,TILE_CONCRETE) in [TILE_CONCRETE, TILE_DIRT]
		
		
	def draw(self):
		draw_species([self.species], self.x, self.y, self.face_right)
		
	def _can_move_to(self,x,y):
		r = Rect(x-6, y-12,12,12)
		m = self.world.map
		for (x,y) in m.visit_tiles(r):
			if m.get_tile(x,y,TILE_CONCRETE) in [TILE_DIRT, TILE_CONCRETE]:
				return False
		return True
		
	@property
	def collider(self):
		return Rect(self.x-6,self.y-12,12,12)
		
class Animal(GameObject):
	def __init__(self, world):
		super(Animal, self).__init__(world)
		self.vy = 0
		self.on_ground = False
		self.face_right = True
		self.last_vy = 0
		self.was_in_water = False
		self.splash = Splash(world)
		self.splash.priority = 5
		self.crosshair = Crosshair(world)
		world.add(self.splash)
		world.add(self.crosshair)
		self.dig_dir_x = 1
		self.dig_dir_y = 0
		self.species = [SPECIES_BEAR, SPECIES_BEAR]
		self.cooling_down = False
		self.cooldown_timer = 0
		self.flicker_counter = 0
		self.breath_counter =0
		
	def update(self, delta):
	
		# Update dig dir
		if engine.key_down(key.LEFT):
			self.dig_dir_x = -1
			self.dig_dir_y = 0
		elif engine.key_down(key.RIGHT):
			self.dig_dir_x = +1
			self.dig_dir_y = 0
		elif engine.key_down(key.UP):
			self.dig_dir_x = 0
			self.dig_dir_y = -1
		elif engine.key_down(key.DOWN):
			self.dig_dir_x = 0
			self.dig_dir_y = +1
	
		if self.can_dig() and engine.key_pressed(key.D):
			m = self.world.map
			tx,ty = m.to_tile_coords(*self.get_dig_coords())
			if m.valid_tile(tx,ty):
				if m.get_tile(tx,ty) == TILE_DIRT:
					m.set_tile(tx,ty,TILE_DIRT_HOLE)
					m.discard_list() # redraw map to DL
					SFX_DIG.play()
					#print 'DIG OK'
				else:
					#print 'DIG FAIL'
					pass
					#c = Crosshair(self.world)
					#c.x,c.y = self.get_dig_coords()
					#self.world.add(c)
	
		# Move in the X direction
		xdir = 0
		if engine.key_down(key.LEFT):
			xdir -= 1
			self.face_right = False
		if engine.key_down(key.RIGHT):
			xdir += 1
			self.face_right = True
		
		in_water, waterline = self._in_water()
		
		if in_water != self.was_in_water:
			SFX_SPLASH.play()
			self.world.water_particles.splash(self.x,self.y)
		
		if in_water and SPECIES_FISH in self.species:
			self.breath_counter += delta
			if self.breath_counter > 1:
				self.breath_counter = 0
				self.world.bubbles.bubble(self.x + (6 if self.face_right else -6),self.y-8)
		
		# Respond to "JUMP" key
		if engine.key_pressed(key.SPACE):
			if (self.on_ground or in_water):
				self.vy = (-220 if self.can_high_jump() else -150)
				self.on_ground = False
				if self.can_high_jump():
					SFX_HIJUMP.play()
				else:
					SFX_JUMP.play()
			elif self.can_air_jump():
				self.vy = -100
				self.on_ground = False
				SFX_FLAP.play()
		
		if in_water and self.can_swim():
			swim_y=0
			if engine.key_down(key.UP):
				swim_y -= 1
				self.on_ground = False
			elif engine.key_down(key.DOWN):
				swim_y += 1
			if swim_y != 0:
				self.vy += swim_y * 600 * delta
				
		if not self.on_ground:
			apply_drag = False
			apply_gravity = False
			apply_bouyancy = False
			
			if in_water:
				if self.can_swim():
					apply_drag = True
				else:
					apply_drag = True
					apply_bouyancy = True
					apply_gravity = True
			else:
				apply_gravity = True
				
			if apply_bouyancy:
				# bouyancy
				self.vy -= (self.y - waterline)*100*delta
				
			if apply_gravity:
				# gravity
				self.vy += 400*delta
		
			if apply_drag:
				# actual math is happening here, look out.
				self.vy *= (0.0001)**delta

		# Perform horizontal motion
		self._move(self.x + xdir*100*delta, self.y)
		
		# slightly less shitty integration (I think)
		newY = self.y + (self.vy + self.last_vy) * delta * 0.5
		
		if in_water or (not self.on_ground):
			if self._move(self.x, self.y + self.vy*delta):
				if self.vy > 0:
					self.on_ground = True
				self.vy = 0
		elif (not in_water) and self.on_ground:
			if not self._move(self.x, self.y + 1):
				self.y -= 1
				self.on_ground = False
			
		# Update splash sprite
		if in_water and (self.y - waterline) < 16:
			self.splash.x = self.x
			self.splash.y = waterline
			self.splash.visible = True
		else:
			self.splash.visible = False
			
		if self.can_dig():
			self.crosshair.visible = True
			self.crosshair.x, self.crosshair.y = self.get_dig_coords()
		else:
			self.crosshair.visible = False
		
		self.last_vy = self.vy
		self.was_in_water = in_water
		
		if self.did_win():
			self.world.win()
			
		if not self.cooling_down:
			for wa in self.world.wild_animals:
				if wa.collider.overlap(self.collider):
					self.species = self.species[1:] + [wa.species]
					wa.killme = True
					self.world.wild_animals.remove(wa)
					self.cooling_down = True
					self.cooldown_timer = 0.5
					self.world.update_species()
					SFX_MUTATE.play()
					break
		else:
			self.cooldown_timer -= delta
			if self.cooldown_timer <= 0:
				self.cooling_down = False
		
		
	def _move(self, newx, newy):
		if self._can_move_to(newx, newy):
			self.x = newx
			self.y = newy
			return False
		
		start = 0
		end = 1
		bestT = 0
		for n in range(10):
			mid = (start+end) * 0.5
			testx = lerp(mid, self.x, newx)
			testy = lerp(mid, self.y, newy)
			if self._can_move_to(testx,testy):
				bestT = mid
				start,end = mid,end
			else:
				start,end = start,mid
		
		self.x = lerp(bestT, self.x, newx)
		self.y = lerp(bestT, self.y, newy)
		return True
		
	def _can_move_to(self,x,y):
		r = self.collider_at(x,y)
		m = self.world.map
		for (x,y) in m.visit_tiles(r):
			if m.get_tile(x,y,TILE_CONCRETE) in [TILE_DIRT, TILE_CONCRETE]:
				return False
		return True
		
	def _in_water(self):
		r = self.collider
		r.x += 4
		r.w -= 8
		waterline = 1e9
		m = self.world.map
		for (x,y) in m.visit_tiles(r):
			if m.get_tile(x,y,TILE_CONCRETE) is TILE_WATER:
				
				while m.get_tile(x, y-1, TILE_CONCRETE) is TILE_WATER:
					y -=1
						
				waterline = min(waterline, y*TILE_SIZE)
				return True, waterline
		return False, 0
				
	def collider_at(self, x,y):
		return Rect(x-6, y-10, 12, 10)
		
	def did_win(self):
		r = self.collider
		m = self.world.map
		for (x,y) in m.visit_tiles(r):
			if m.get_tile(x,y,TILE_CONCRETE) in [TILE_EXIT]:
				return True
		return False
				
	@property
	def collider(self):
		return self.collider_at(self.x, self.y)
		
	def draw(self):
		#draw_subrect(self.tex, self.x-8, self.y-16, 16,16, 4*16,4*16,flip_x = not self.face_right)
		flash = False
		if self.cooling_down:
			flash = self.flicker_counter < 2
			if flash:
				glColor3f(0.5,1,0.2)
		draw_species(self.species, self.x, self.y, self.face_right, flash=flash)
		glColor3f(1,1,1)
		self.flicker_counter = (self.flicker_counter + 1)%4
		
	def can_high_jump(self):
		return SPECIES_KANGAROO in self.species
		
	def can_air_jump(self):
		return SPECIES_EAGLE in self.species
		
	def can_dig(self):
		return SPECIES_MOLE in self.species
		
	def get_dig_coords(self):
		return (self.x + self.dig_dir_x * 16,
				self.y + self.dig_dir_y * 16 - 8)
				
	def can_swim(self):
		return SPECIES_FISH in self.species
		
		
		
class Splash(GameObject):
	def __init__(self,world):
		super(Splash,self).__init__(world)
		self.frames = [get_tex('waterline1.png'),
						get_tex('waterline2.png')]
		self.t = 0
		self.frame = 0
		
	def update(self,delta):
		self.t += delta
		if self.t >= 0.2:
			self.t = 0
			self.frame += 1
			if self.frame == 2:
				self.frame = 0
				
	def draw(self):
		draw_subrect(self.frames[self.frame], self.x-8, self.y-8, 16,16)
		
class Crosshair(GameObject):
	def __init__(self,world):
		super(Crosshair,self).__init__(world)
		self.tex = get_tex('crosshair.png')
		
	def draw(self):
		draw_subrect(self.tex, self.x-7, self.y-7, 16,16)

		
class Particle:
	def __init__(self):
		self.wiggle_rate = 0
		self.wiggle_pos = 0
		self.x = 0
		self.y = 0
		self.vy = 0
		self.vx = 0
		self.r = 0
		self.g = 0
		self.b = 0
		self.age = 0
	
class Confetti(GameObject):
	def __init__(self,world,infinite=False):
		super(Confetti,self).__init__(world)
		self.infinite = infinite
		self.particles = []
		for n in range(1000):
			p = Particle()
			p.x = random.uniform(0,320)
			if infinite:
				p.y = random.uniform(0,240)
			else:
				p.y = random.uniform(-50, 0)
			p.vy = random.uniform(10,100)
			p.wiggle_rate = random.uniform(0.5, 2)
			p.wiggle_pos = random.uniform(0, math.pi*2)
			p.r,p.g,p.b = random.choice([
				(1,1,1),
				(1,0.5,0.5),
				(1,1,0.5),
				(0.5,1,0.5),
				(0.5,0.5,1),
				(0.5,1,1),
				(1,0.5,1),
			])
			self.particles.append(p)
		self.particles.sort(key=lambda p:(p.r,p.g,p.b))
		
	def update(self, delta):
		for p in self.particles:
			p.y += p.vy*delta
			p.wiggle_pos += p.wiggle_rate*delta
		if self.infinite:
			for p in self.particles:
				if p.y > 240:
					p.y = 0
		
	def draw(self):
		#glBindTexture(self.tex.target, self.tex.id)
		glDisable(GL_TEXTURE_2D)
		glPointSize(SCALE)
		glBegin(GL_POINTS)
		r,g,b = -1,-1,-1
		for p in self.particles:
			if p.y < 0 or p.y > 240:
				continue
			x = p.x + math.sin(p.wiggle_pos)*10
			if (p.r,p.g,p.b) != (r,g,b):
				glColor3f(p.r,p.g,p.b)
				r,g,b = p.r,p.g,p.b
			glVertex2f(x*SCALE, p.y*SCALE);
		glEnd()
		glColor3f(1,1,1)
		glEnable(GL_TEXTURE_2D)
		
DROPLET_AGE = 1.0
		
class WaterParticles(GameObject):
	def __init__(self,world):
		super(WaterParticles,self).__init__(world)
		self.particles = []
		self.priority = -1
		
	def update(self, delta):
		for p in self.particles:
			p.age += delta
			p.vy += 700*delta
			p.y += p.vy*delta
			p.x += p.vx*delta
		self.particles = [p for p in self.particles if p.age < DROPLET_AGE]
		
	def draw(self):
		#glBindTexture(self.tex.target, self.tex.id)
		glDisable(GL_TEXTURE_2D)
		glPointSize(SCALE)
		glBegin(GL_POINTS)
		for p in self.particles:
			glColor4f(p.r,p.g,p.b,1.0 -p.age/DROPLET_AGE)
			glVertex2f(p.x*SCALE, p.y*SCALE);
		glEnd()
		glColor4f(1,1,1,1)
		glEnable(GL_TEXTURE_2D)
		
	def splash(self,x,y):
		for n in range(20):
			p = Particle()
			p.x = x + random.uniform(-8,8)
			p.y = y
			p.vy = random.uniform(-100,-200)
			p.vx = random.uniform(-50,50)
			p.age = 0
			p.r,p.g,p.b = 126/255.0,1,253/255.0
			if random.random() < 0.25:
				p.r,p.g,p.b = 1,1,1
			self.particles.append(p)
		
class Bubbles(GameObject):
	def __init__(self,world):
		super(Bubbles,self).__init__(world)
		self.particles = []
		self.priority = -1
		
	def update(self, delta):
		for p in self.particles:
			p.age += delta
			p.y -= 50*delta
			tempx = self.get_x(p)
			tx,ty = self.world.map.to_tile_coords(tempx,p.y)
			if self.world.map.get_tile(tx,ty,TILE_CONCRETE) != TILE_WATER:
				p.kill = True
		self.particles = [p for p in self.particles if not p.kill]
			
	def get_x(self,p):
		return p.x + 5*math.sin(p.age*5)
		
	def draw(self):
		#glBindTexture(self.tex.target, self.tex.id)
		glDisable(GL_TEXTURE_2D)
		glPointSize(SCALE*2)
		glBegin(GL_POINTS)
		for p in self.particles:
			glVertex2f(self.get_x(p)*SCALE, p.y*SCALE);
		glEnd()
		glEnable(GL_TEXTURE_2D)
		
	def bubble(self,x,y):
		p = Particle()
		p.x = x
		p.y = y
		p.age = 0
		p.kill = False
		self.particles.append(p)
			
class World(object):
	def __init__(self):
		self._gos = []
		
	def add(self,go):
		assert go is not None
		assert go.world == self
		self._gos.append(go)
					
	def update(self, delta):
		n = 0
		dead = 0
		while n < len(self._gos):
			go = self._gos[n]
			if not go.killme:
				go.update(delta)
			else:
				dead += 1
			n += 1
		if dead > 0:
			self._gos = [go for go in self._gos if not go.killme]	

	def draw(self):
		sorted = self._gos[:]
		sorted.sort(key=lambda go:go.priority)
		for go in sorted:
			if go.visible:
				go.draw()

	def become_active(self):
		pass
			
	def become_inactive(self):
		pass
		
bg_timer =0
BG_TEX = get_tex('bg.png')

def update_bg(delta):
	global bg_timer
	
	bg_timer = (bg_timer + delta*31)%(62*2)
	
		
def draw_bg():
	glClearColor(0,0,0,1)
	glClear(GL_COLOR_BUFFER_BIT)
	
	for x in range(-2,6):
		for y in range(-2,5):
			draw_subrect(BG_TEX, x*62 + bg_timer,y*62 + bg_timer*0.5,62,62)
		
class PuzzleWorld(World):
	def __init__(self, levels):
		global bg_timer
		assert len(levels) > 0
		super(PuzzleWorld, self).__init__()
		self.levels = levels
		self.wild_animals = []
		self.water_particles = WaterParticles(self)
		self.add(self.water_particles)
		self.bubbles = Bubbles(self)
		self.add(self.bubbles)
		self._won = False
		self.hud_tex = get_tex('hud.png')
		self.help_tex = get_tex('help.png')
		self.label = Label('MOLEBEAR!', font_name='Arial, Helvetica, Sans', font_size=8*SCALE,
							anchor_x='center',
							x = 160*SCALE,
							y = (240-40)*SCALE)
		
		#self.map = Map(self,TEST_MAP)
		self.map = Map(self, self.levels[0])
		self.add(self.map)
		
		player = Animal(self)
		player.x, player.y = (self.map.start_x + 0.5)*TILE_SIZE, (self.map.start_y+1)*TILE_SIZE-0.1
		self.add(player)
		self.player = player
		
		self.update_species()
		
		self.win_timer = 0
		
		self.show_help = False
		
		#self.add(Confetti(self))
		
	def update(self, delta):
		update_bg(delta)
		
		if self.show_help:
			if engine.key_pressed(key.F1) or engine.key_pressed(key.ESCAPE):
				self.show_help = False
		else:
			if engine.key_pressed(key.ESCAPE):
				pyglet.app.exit()
				return
			if engine.key_pressed(key.F1):
				self.show_help = True
		
			if engine.key_pressed(key.R):
				engine.next_world = PuzzleWorld(self.levels)
			#if engine.key_pressed(key.W):
			#	self.win()
			super(PuzzleWorld,self).update(delta)
			
			
			if self._won:
				self.win_timer += delta
				if self.win_timer > 2:
					if len(self.levels) > 1:
						engine.next_world = PuzzleWorld(self.levels[1:])
					else:
						engine.next_world = WinWorld()
		
		
	def draw(self):
		draw_bg()
		
		if self.show_help:
			draw_subrect(self.help_tex,0,0)
		else:
			super(PuzzleWorld,self).draw()
			
			draw_species([self.player.species[1]], 142,24, True)
			draw_species([self.player.species[0]], 178,24, True)
			draw_subrect(self.hud_tex, 0, 0)
			
			glMatrixMode(GL_PROJECTION)
			glPushMatrix()
			glLoadIdentity()
			glOrtho(0, 320*SCALE, 0, 240*SCALE, -1, 1)
			
			labelX = self.label.x
			labelY = self.label.y
			self.label.x += 2
			self.label.y -= 2
			self.label.color = (0,0,0,255)
			self.label.draw()
			
			self.label.x = labelX
			self.label.y = labelY
			self.label.color = (255,255,255,255)
			self.label.draw()
			
			glPopMatrix()
			glMatrixMode(GL_MODELVIEW)
		
	def win(self):
		if not self._won:
			self._won = True
			SFX_WIN.play()
			self.add(Confetti(self))
			
	@property
	def won(self):
		return self._won
			
	def become_inactive(self):
		self.map.discard_list()
		
	def update_species(self):
		a = self.player.species[0]
		b = self.player.species[1]
		for (k,v) in SPECIES_NAMES.iteritems():
			if k in [(a,b), (b,a)]:
				self.label.text = v + "!"
				break

class WinWorld(World):
	def __init__(self):
		super(WinWorld,self).__init__()
		self.confetti = Confetti(self, infinite=True)
		self.win_tex = get_tex('win.png')
		self.add(self.confetti)
		
	def update(self,delta):
		if engine.key_pressed(key.ESCAPE):
			pyglet.app.exit()
			return
				
		update_bg(delta)	
		super(WinWorld,self).update(delta)
		
	def draw(self):
		draw_bg()
		draw_subrect(self.win_tex,0,0)
		super(WinWorld,self).draw()
	
class Engine(object):
	def __init__(self):
		self._world = World()
		self.next_world = None
		self._updated = False
		self._checkedKeys = [
			key.SPACE,
			key.LEFT,
			key.RIGHT,
			key.UP,
			key.DOWN,
			key.ENTER,
			key.D,
			key.R,
			key.ESCAPE,
			key.W,
			key.F1
		]
		self._lastFrameKeys = {}
		self._thisFrameKeys = {}
		
	def draw(self):
		if not self._updated:
			self.update(1/60.0)
			self._updated = True
			
		t = time.clock()
		#glClear(GL_COLOR_BUFFER_BIT)
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, 320*SCALE, 240*SCALE, 0, -1, 1)
		glColor4f(1,1,1,1)
		
		glDisable(GL_CULL_FACE)
		glEnable(GL_TEXTURE_2D)
		glDisable(GL_DEPTH_TEST)
		glDepthMask(GL_FALSE)
		glEnable(GL_BLEND)
		
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
			
		self._world.draw()
		#print 'D: %.3f'%( (time.clock()-t)*1000)
		
	def update(self, delta):
		t = time.clock()
		delta = clamp(delta, 0, 0.1)
		if self.next_world is not None:
			if self._world is not None:
				self._world.become_inactive()
			self._world = self.next_world
			self._world.become_active()
			self.next_world = None
		
		self._lastFrameKeys = self._thisFrameKeys
		self._thisFrameKeys = {}
		for k in self._checkedKeys:
			self._thisFrameKeys[k] = _keys[k]
			
			
		self._world.update(delta)
		#print 'U: %.3f'%( (time.clock()-t)*1000)
		
	def key_down(self, k):
		return self._thisFrameKeys[k]
		
	def key_pressed(self, k):
		return self._thisFrameKeys[k] and not self._lastFrameKeys[k]
		
					
engine = Engine()
engine.next_world = PuzzleWorld(['intro','0','1','2','3','4','5'])
			
@window.event
def on_draw():
	engine.draw()
	
def update(delta):
	engine.update(delta)
	
# Keep ESC from killing the game always
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        return pyglet.event.EVENT_HANDLED
		
window.push_handlers(on_key_press)
	
_keys = key.KeyStateHandler()
window.push_handlers(_keys)
	
pyglet.clock.schedule(update)
pyglet.app.run()