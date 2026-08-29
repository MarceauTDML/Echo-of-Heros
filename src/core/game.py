import pygame
import sys
from src.settings import *
from src.ui.menu import MainMenu
from src.ui.shop_menu import ShopMenu
from src.ui.level_select import LevelSelectMenu
from src.editor.editor_main import EditorState
from src.core.player_data import PlayerData

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        
        self.running = True
        self.state = "MENU"
        
        self.player_data = PlayerData()
        
        self.menu = MainMenu(self.screen, self.go_to_shop, self.go_to_level_select)
        self.shop = ShopMenu(self.screen, self.player_data, self.go_to_menu)
        self.level_select = LevelSelectMenu(self.screen, self.go_to_menu, self.go_to_editor)
        self.editor = EditorState(self.screen, self.go_to_level_select)

    def go_to_shop(self):
        self.state = "SHOP"

    def go_to_menu(self):
        self.state = "MENU"
        
    def go_to_level_select(self):
        self.state = "LEVEL_SELECT"
        
    def go_to_editor(self, world, level):
        self.editor.load_level(world, level)
        self.state = "EDITOR"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "SHOP":
                        self.go_to_menu()
                    else:
                        self.running = False
            
            if self.state == "MENU":
                self.menu.handle_events(event)
            elif self.state == "SHOP":
                self.shop.handle_events(event)
            elif self.state == "LEVEL_SELECT":
                self.level_select.handle_events(event)
            elif self.state == "EDITOR":
                self.editor.handle_events(event)

    def update(self):
        if self.state == "MENU":
            self.menu.update(self.dt)
        elif self.state == "SHOP":
            self.shop.update(self.dt)
        elif self.state == "LEVEL_SELECT":
            self.level_select.update(self.dt)
        elif self.state == "EDITOR":
            self.editor.update(self.dt)

    def draw(self):
        if self.state == "MENU":
            self.menu.draw()
        elif self.state == "SHOP":
            self.shop.draw()
        elif self.state == "LEVEL_SELECT":
            self.level_select.draw()
        elif self.state == "EDITOR":
            self.editor.draw()
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            self.dt = self.clock.tick(FPS) / 1000.0
