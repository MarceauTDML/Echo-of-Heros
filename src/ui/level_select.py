import pygame
from src.settings import *

class LevelSelectMenu:
    def __init__(self, display_surface, back_callback, edit_callback):
        self.display_surface = display_surface
        self.back_callback = back_callback
        self.edit_callback = edit_callback
        
        pygame.font.init()
        self.title_font = pygame.font.SysFont('arial', 60, bold=True)
        self.font = pygame.font.SysFont('arial', 30, bold=True)
        
        self.selected_world = 1
        
        self.back_btn = pygame.Rect(20, 20, 120, 50)
        
        self._setup_layout(SCREEN_WIDTH)
        
    def _setup_layout(self, sw):
        self.world_btns = []
        start_x = (sw - (5 * 120 + 4 * 30)) // 2
        start_y = 120
        for i in range(15):
            row = i // 5
            col = i % 5
            rect = pygame.Rect(start_x + col * 150, start_y + row * 80, 120, 50)
            self.world_btns.append(rect)
            
        self.level_btns = []
        l_start_x = (sw - (4 * 120 + 3 * 30)) // 2
        l_start_y = 420
        for i in range(8):
            row = i // 4
            col = i % 4
            rect = pygame.Rect(l_start_x + col * 150, l_start_y + row * 80, 120, 50)
            self.level_btns.append(rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.back_btn.collidepoint(mouse_pos):
                    self.back_callback()
                    return
                
                for i, rect in enumerate(self.world_btns):
                    if rect.collidepoint(mouse_pos):
                        self.selected_world = i + 1
                        return
                        
                for i, rect in enumerate(self.level_btns):
                    if rect.collidepoint(mouse_pos):
                        self.edit_callback(self.selected_world, i + 1)
                        return

    def update(self, dt):
        sw = self.display_surface.get_width()
        if not hasattr(self, '_last_sw') or self._last_sw != sw:
            self._setup_layout(sw)
            self._last_sw = sw

    def draw(self):
        self.display_surface.fill(BG_COLOR)
        
        mouse_pos = pygame.mouse.get_pos()
        
        b_color = (200, 100, 100) if self.back_btn.collidepoint(mouse_pos) else (150, 50, 50)
        pygame.draw.rect(self.display_surface, b_color, self.back_btn, border_radius=10)
        b_text = self.font.render("Retour", True, (255, 255, 255))
        self.display_surface.blit(b_text, b_text.get_rect(center=self.back_btn.center))
        
        t_text = self.title_font.render("Sélection du Niveau (Éditeur)", True, (255, 255, 255))
        self.display_surface.blit(t_text, (self.display_surface.get_width() // 2 - t_text.get_width() // 2, 20))
        
        w_t = self.font.render("Choix du Monde (1-15):", True, (255, 255, 255))
        w_start_x = (self.display_surface.get_width() - (5 * 120 + 4 * 30)) // 2
        self.display_surface.blit(w_t, (w_start_x, 80))
        
        for i, rect in enumerate(self.world_btns):
            world_num = i + 1
            color = (100, 200, 100) if self.selected_world == world_num else (50, 100, 150)
            if rect.collidepoint(mouse_pos) and self.selected_world != world_num:
                color = (75, 125, 175)
            pygame.draw.rect(self.display_surface, color, rect, border_radius=8)
            text = self.font.render(f"Monde {world_num}", True, (255, 255, 255))
            self.display_surface.blit(text, text.get_rect(center=rect.center))
            
        l_t = self.font.render(f"Niveaux du Monde {self.selected_world} (1-8):", True, (255, 255, 255))
        l_start_x = (self.display_surface.get_width() - (4 * 120 + 3 * 30)) // 2
        self.display_surface.blit(l_t, (l_start_x, 380))
        
        for i, rect in enumerate(self.level_btns):
            lvl_num = i + 1
            color = (150, 100, 200) if rect.collidepoint(mouse_pos) else (100, 50, 150)
            pygame.draw.rect(self.display_surface, color, rect, border_radius=8)
            text = self.font.render(f"Niveau {lvl_num}", True, (255, 255, 255))
            self.display_surface.blit(text, text.get_rect(center=rect.center))
