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
        
        self.back_btn = pygame.Rect(10, 10, 100, 40)
        
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.grid_size = 32
        
    def load_level(self, world, level):
        self.world = world
        self.level = level
        self.camera_offset = pygame.math.Vector2(0, 0)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.back_btn.collidepoint(pygame.mouse.get_pos()):
                    self.back_callback()
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
        self.display_surface.fill((40, 40, 40))
        
        start_x = int(self.camera_offset.x % self.grid_size) - self.grid_size
        start_y = int(self.camera_offset.y % self.grid_size) - self.grid_size
        
        for x in range(start_x, SCREEN_WIDTH + self.grid_size, self.grid_size):
            pygame.draw.line(self.display_surface, (60, 60, 60), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(start_y, SCREEN_HEIGHT + self.grid_size, self.grid_size):
            pygame.draw.line(self.display_surface, (60, 60, 60), (0, y), (SCREEN_WIDTH, y))
            
        mouse_pos = pygame.mouse.get_pos()
        b_color = (200, 100, 100) if self.back_btn.collidepoint(mouse_pos) else (150, 50, 50)
        pygame.draw.rect(self.display_surface, b_color, self.back_btn, border_radius=5)
        b_text = self.font.render("Retour", True, (255, 255, 255))
        self.display_surface.blit(b_text, b_text.get_rect(center=self.back_btn.center))
        
        info_text = self.font.render(f"Éditeur - Monde {self.world} Niveau {self.level} | Flèches/ZQSD pour bouger", True, (255, 255, 255))
        self.display_surface.blit(info_text, (130, 15))
