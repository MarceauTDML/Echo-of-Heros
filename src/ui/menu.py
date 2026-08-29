import pygame
import sys
from src.settings import *

class MainMenu:
    def __init__(self, display_surface: pygame.Surface, shop_callback, editor_callback=None):
        self.display_surface = display_surface
        self.shop_callback = shop_callback
        self.editor_callback = editor_callback
        
        pygame.font.init()
        self.title_font = pygame.font.SysFont('arial', 80, bold=True)
        self.button_font = pygame.font.SysFont('arial', 40, bold=True)
        
        self.title_text = self.title_font.render(TITLE, True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        
        btn_width = 250
        btn_height = 70
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - btn_width // 2, SCREEN_HEIGHT // 2, btn_width, btn_height)
        self.shop_button = pygame.Rect(SCREEN_WIDTH // 2 - btn_width // 2, SCREEN_HEIGHT // 2 + 100, btn_width, btn_height)
        self.editor_button = pygame.Rect(SCREEN_WIDTH // 2 - btn_width // 2, SCREEN_HEIGHT // 2 + 200, btn_width, btn_height)
        self.quit_button = pygame.Rect(SCREEN_WIDTH // 2 - btn_width // 2, SCREEN_HEIGHT // 2 + 300, btn_width, btn_height)
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.shop_button.collidepoint(mouse_pos):
                    self.shop_callback()
                elif self.editor_button.collidepoint(mouse_pos) and self.editor_callback:
                    self.editor_callback()
                elif self.quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    def update(self, dt):
        pass

    def draw(self):
        self.display_surface.fill(BG_COLOR)
        
        self.display_surface.blit(self.title_text, self.title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        play_color = (100, 200, 100) if self.play_button.collidepoint(mouse_pos) else (50, 150, 50)
        pygame.draw.rect(self.display_surface, play_color, self.play_button, border_radius=15)
        play_text = self.button_font.render("Jouer", True, (255, 255, 255))
        self.display_surface.blit(play_text, play_text.get_rect(center=self.play_button.center))
        
        shop_color = (100, 150, 200) if self.shop_button.collidepoint(mouse_pos) else (50, 100, 150)
        pygame.draw.rect(self.display_surface, shop_color, self.shop_button, border_radius=15)
        shop_text = self.button_font.render("Boutique", True, (255, 255, 255))
        self.display_surface.blit(shop_text, shop_text.get_rect(center=self.shop_button.center))
        
        editor_color = (200, 150, 100) if self.editor_button.collidepoint(mouse_pos) else (150, 100, 50)
        pygame.draw.rect(self.display_surface, editor_color, self.editor_button, border_radius=15)
        editor_text = self.button_font.render("Éditeur", True, (255, 255, 255))
        self.display_surface.blit(editor_text, editor_text.get_rect(center=self.editor_button.center))
        
        quit_color = (200, 100, 100) if self.quit_button.collidepoint(mouse_pos) else (150, 50, 50)
        pygame.draw.rect(self.display_surface, quit_color, self.quit_button, border_radius=15)
        quit_text = self.button_font.render("Quitter", True, (255, 255, 255))
        self.display_surface.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
