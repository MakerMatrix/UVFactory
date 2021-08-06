#!/usr/bin/python3

import os
import pygame

def checkDisplay():

	if pygame.display.get_init():
		print("Display initialized")
		print(pygame.display.get_driver())
		videoInfo = pygame.display.Info()
		print(videoInfo)
		return videoInfo.current_w, videoInfo.current_h
	else:
		print("Display not initialized!")
	
# Make this start on a console framebuffer
# It needs to run as root if this isn't launched from the console device
#os.unsetenv('DISPLAY')
os.putenv('SDL_FBDEV', "/dev/fb0")
os.putenv('SDL_VIDEODRIVER', "RPI")
#os.putenv('SDL_VIDEODRIVER', "KMSDRM")
#os.putenv('SDL_RENDER_DRIVER', "software")
os.putenv('SDL_VIDEO_EGL_DRIVER', "libEGL.so")
os.putenv('SDL_VIDEO_GL_DRIVER', "libGLESv2.so")


pygame.display.init()
lcdWidth, lcdHeight = checkDisplay()
uvlcd = pygame.display.set_mode([lcdWidth, lcdHeight])

black = (0,0,0)
clock = pygame.time.Clock()

crashed = False
maskedLayer = pygame.surface.Surface([lcdWidth, lcdHeight])
layer = pygame.image.load('assets/BlackBanner-1200x300.bmp').convert()
mask = pygame.image.load('assets/Mask2560x1600.png').convert()

x = y = 0
xmax = lcdWidth-1200
ymax = lcdHeight-300
xincr = 5
yincr = 8
while(1):
	
	# ~ # Make a regular surface offscreen and work there
	# ~ maskedLayer.fill(black)
	# ~ pygame.Surface.blit(maskedLayer, layer, [x, y])
	# ~ pygame.Surface.blit(maskedLayer, mask, [0,0], special_flags=pygame.BLEND_MULT)
	# ~ # Now blit to the display surface
	# ~ uvlcd.blit(maskedLayer, [0,0])
	
	# Working directly on the display surface seems faster:
	uvlcd.fill(black) 
	uvlcd.blit(layer, (x,y))
	uvlcd.blit(mask, (0,0), special_flags=pygame.BLEND_MULT)
		
	pygame.display.update()
	if (((x + xincr) > xmax) or ((x + xincr) < 0)):
		xincr = -xincr
	if (((y + yincr) > ymax) or ((y + yincr) < 0)):
		yincr = -yincr
	x += xincr
	y += yincr
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
