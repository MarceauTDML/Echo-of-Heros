import pygame
from src.settings import *

class EditorState:
    def __init__(self, display_surface, back_callback):
        self.display_surface = display_surface
        self.back_callback = back_callback
        
        self.world = 1
        self.level = 1
        
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.tab_font = pygame.font.SysFont('arial', 18, bold=True)
        
        self.back_btn = pygame.Rect(10, 10, 100, 40)
        
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.grid_size = 32
        
        self.tabs = ["Blocs", "Décors", "Entités"]
        self.active_tab = "Blocs"
        self.sidebar_rect = pygame.Rect(0, 0, 0, 0)
        self.tab_rects = []
        self.sidebar_w = 0
        
    def load_level(self, world, level):
        self.world = world
        self.level = level
        self.camera_offset = pygame.math.Vector2(0, 0)

    def _update_layout(self):
        sw = self.display_surface.get_width()
        sh = self.display_surface.get_height()
        
        self.sidebar_w = sw // 5
        self.sidebar_rect = pygame.Rect(sw - self.sidebar_w, 0, self.sidebar_w, sh)
        
        self.tab_rects = []
        tab_w = self.sidebar_w // 3
        for i, tab in enumerate(self.tabs):
            rect = pygame.Rect(sw - self.sidebar_w + i * tab_w, 0, tab_w, 40)
            self.tab_rects.append(rect)

    def handle_events(self, event):
        self._update_layout()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_btn.collidepoint(mouse_pos):
                    self.back_callback()
                    return
                
                for i, rect in enumerate(self.tab_rects):
                    if rect.collidepoint(mouse_pos):
                        self.active_tab = self.tabs[i]
                        return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back_callback()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        speed = 400 * dt
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.camera_offset.x += speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera_offset.x -= speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.camera_offset.y += speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera_offset.y -= speed

    def draw(self):
        self._update_layout()
        self.display_surface.fill((40, 40, 40))
        
        sw = self.display_surface.get_width()
        sh = self.display_surface.get_height()
        
        start_x = int(self.camera_offset.x % self.grid_size) - self.grid_size
        start_y = int(self.camera_offset.y % self.grid_size) - self.grid_size
        
        playable_w = sw - self.sidebar_w
        
        for x in range(start_x, playable_w + self.grid_size, self.grid_size):
            if x <= playable_w:
                pygame.draw.line(self.display_surface, (60, 60, 60), (x, 0), (x, sh))
        for y in range(start_y, sh + self.grid_size, self.grid_size):
            pygame.draw.line(self.display_surface, (60, 60, 60), (0, y), (playable_w, y))
            
        pygame.draw.rect(self.display_surface, (30, 30, 30), self.sidebar_rect)
        pygame.draw.line(self.display_surface, (100, 100, 100), (sw - self.sidebar_w, 0), (sw - self.sidebar_w, sh), 2)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, rect in enumerate(self.tab_rects):
            tab = self.tabs[i]
            if tab == self.active_tab:
                color = (80, 80, 80)
            elif rect.collidepoint(mouse_pos):
                color = (60, 60, 60)
            else:
                color = (40, 40, 40)
                
            pygame.draw.rect(self.display_surface, color, rect)
            pygame.draw.rect(self.display_surface, (100, 100, 100), rect, 1)
            
            txt = self.tab_font.render(tab, True, (255, 255, 255))
            self.display_surface.blit(txt, txt.get_rect(center=rect.center))
            
        b_color = (200, 100, 100) if self.back_btn.collidepoint(mouse_pos) else (150, 50, 50)
        pygame.draw.rect(self.display_surface, b_color, self.back_btn, border_radius=5)
        b_text = self.font.render("Retour", True, (255, 255, 255))
        self.display_surface.blit(b_text, b_text.get_rect(center=self.back_btn.center))
        
        info_text = self.font.render(f"Éditeur - Monde {self.world} Niveau {self.level} | Flèches/ZQSD pour bouger", True, (255, 255, 255))
        self.display_surface.blit(info_text, (130, 15))
