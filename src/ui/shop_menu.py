import pygame
from src.settings import *
from src.utils.resource_loader import ResourceLoader
from src.utils.data_manager import DataManager

class ShopMenu:
    def __init__(self, display_surface, player_data, back_callback):
        self.display_surface = display_surface
        self.player_data = player_data
        self.back_callback = back_callback
        
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 40, bold=True)
        self.small_font = pygame.font.SysFont('arial', 20, bold=True)
        self.name_font = pygame.font.SysFont('arial', 24, bold=True)
        
        self.heroes = DataManager.load_json('heroes.json')
        
        self.back_btn = pygame.Rect(20, 20, 150, 50)
        self.cards = []
        
        self._setup_grid()

    def _setup_grid(self):
        self.cards.clear()
        card_w = 220
        card_h = 180
        start_x = (SCREEN_WIDTH - (3 * card_w) - (2 * 50)) // 2
        start_y = 100
        
        row, col = 0, 0
        for hero_id, data in self.heroes.items():
            x = start_x + col * (card_w + 50)
            y = start_y + row * (card_h + 30)
            rect = pygame.Rect(x, y, card_w, card_h)
            
            img = ResourceLoader.load_image(f"heros/{hero_id}_Idle_1.png")
            img = pygame.transform.scale(img, (int(img.get_width() * 3.0), int(img.get_height() * 3.0)))
            
            self.cards.append({
                "id": hero_id,
                "rect": rect,
                "name": data["name"],
                "price": data["price"],
                "img": img
            })
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_btn.collidepoint(mouse_pos):
                    self.back_callback()
                
                for card in self.cards:
                    if card["rect"].collidepoint(mouse_pos):
                        self.player_data.buy_hero(card["id"], card["price"])

    def update(self, dt):
        pass

    def draw(self):
        self.display_surface.fill(BG_COLOR)
        
        mouse_pos = pygame.mouse.get_pos()
        
        back_color = (200, 100, 100) if self.back_btn.collidepoint(mouse_pos) else (150, 50, 50)
        pygame.draw.rect(self.display_surface, back_color, self.back_btn, border_radius=10)
        b_txt = self.small_font.render("Retour", True, (255, 255, 255))
        self.display_surface.blit(b_txt, b_txt.get_rect(center=self.back_btn.center))
        
        coins_txt = self.font.render(f"Pieces: {self.player_data.coins}", True, (255, 215, 0))
        self.display_surface.blit(coins_txt, (SCREEN_WIDTH - 250, 25))
        
        title_txt = self.font.render("Boutique de Heros", True, (255, 255, 255))
        self.display_surface.blit(title_txt, title_txt.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        
        for card in self.cards:
            rect = card["rect"]
            h_id = card["id"]
            price = card["price"]
            
            if h_id in self.player_data.owned_heroes:
                color = (80, 120, 200)
                status = "Possede"
            elif self.player_data.coins >= price:
                color = (100, 200, 100) if rect.collidepoint(mouse_pos) else (50, 150, 50)
                status = f"Acheter ({price})"
            else:
                color = (100, 100, 100)
                status = f"Trop cher ({price})"
                
            pygame.draw.rect(self.display_surface, color, rect, border_radius=10)
            pygame.draw.rect(self.display_surface, (255, 255, 255), rect, width=2, border_radius=10)
            
            name_txt = self.name_font.render(card["name"], True, (255, 255, 255))
            self.display_surface.blit(name_txt, name_txt.get_rect(midtop=(rect.centerx, rect.top + 10)))
            
            img_rect = card["img"].get_rect(center=(rect.centerx, rect.centery))
            self.display_surface.blit(card["img"], img_rect)
            
            stat_txt = self.small_font.render(status, True, (255, 255, 255))
            self.display_surface.blit(stat_txt, stat_txt.get_rect(midbottom=(rect.centerx, rect.bottom - 10)))
