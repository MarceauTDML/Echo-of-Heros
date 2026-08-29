import pygame
import sys
from src.settings import *
from src.ui.menu import MainMenu

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        
        self.running = True
        self.state = "MENU"
        
        self.menu = MainMenu(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            if self.state == "MENU":
                self.menu.handle_events(event)

    def update(self):
        if self.state == "MENU":
            self.menu.update(self.dt)

    def draw(self):
        if self.state == "MENU":
            self.menu.draw()
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            self.dt = self.clock.tick(FPS) / 1000.0
