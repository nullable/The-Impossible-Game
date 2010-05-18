#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
from datetime import datetime, timedelta
import sys

class Drawable:
    def draw_into(self, screen, x = 0, y = 0):
        screen.blit(self.image, self.rect.move(x, y))

class Box(Drawable):
    def __init__(self, image, x, y):
	path = os.path.join('..', 'images', image)
	self.image = pygame.image.load(path).convert_alpha()
	self.rect = self.image.get_rect()
        self.jumping = False
        self.x = x
        self.y = y
        self.j_y = 0
        self.jump_max = 70
        self.jump_ssteps = 50

    def jump(self):
        if not self.jumping:
	    self.backup_image = self.image
            self.jumping = True
            self.jump_step = 0
            self.jump_peek = self.jump_ssteps / 2

    def draw_into(self, screen, x = 0, y = 0):
        if self.jumping:
	    self.jump_step += 1
	    if self.jump_step > self.jump_ssteps * 2:
	        self.jumping = False
	        self.j_y = 0
	        self.image = self.backup_image
            elif self.jump_step  <= self.jump_ssteps:
                d = 1.0 * self.jump_step / self.jump_ssteps * self.jump_max
                self.j_y = d
            else:
		d = 1.0 * (self.jump_step-self.jump_ssteps) / self.jump_ssteps
		self.j_y = self.jump_max - (d * self.jump_max)
	    #print self.j_y
	    self.image = pygame.transform.rotate(self.backup_image, -0.5 * self.jump_step / self.jump_ssteps * 90)
	Drawable.draw_into(self, screen, self.x + x, y + self.y - self.j_y)

class Image(Drawable):
    def __init__(self, image):
       path = os.path.join('..', 'images', image)
       self.image = pygame.image.load(path)
       self.rect = self.image.get_rect()
    
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 340))
    pygame.display.set_caption('tig devel')
    pygame.mouse.set_visible(0)
    t = Image('triangle.png')
    b = Image('testback.png')
    box = Box('box.png', 80, 212)
    t_pos = [420, 212]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP: box.jump()
        t_pos[0] -= 1
        if t_pos[0] < 60: t_pos[0] = 420
        b.draw_into(screen)
        box.draw_into(screen)
        t.draw_into(screen, *t_pos)
        pygame.display.flip()
    
    
if __name__ == '__main__':
    main()
