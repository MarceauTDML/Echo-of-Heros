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
        self.cond_font = pygame.font.SysFont('arial', 18)
        
        self.back_btn = pygame.Rect(10, 10, 100, 40)
        self.save_btn = pygame.Rect(120, 10, 150, 40)
        
        self.held_arrow = None
        self.arrow_timer = 0
        
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.grid_size = 32
        
        self.main_tabs = ["Jeu", "Calques"]
        self.active_main_tab = "Jeu"
        self.main_tab_rects = []
        
        self.sub_tabs = ["Blocs", "Décors", "Entités"]
        self.active_sub_tab = "Blocs"
        self.sub_tab_rects = []
        
        self.sidebar_rect = pygame.Rect(0, 0, 0, 0)
        self.sidebar_w = 0
        
        self.settings_btn = pygame.Rect(10, 0, 140, 40)
        self.show_settings = False
        self.map_width = 100
        self.map_height = 50
        self.map_w_str = str(self.map_width)
        self.map_h_str = str(self.map_height)
        self.active_input = None
        self.popup_rect = pygame.Rect(0, 0, 450, 480)
        self.btn_w_rect = pygame.Rect(0, 0, 100, 30)
        self.btn_h_rect = pygame.Rect(0, 0, 100, 30)
        
        self.btn_w_up_rect = pygame.Rect(0, 0, 20, 15)
        self.btn_w_down_rect = pygame.Rect(0, 0, 20, 15)
        self.btn_h_up_rect = pygame.Rect(0, 0, 20, 15)
        self.btn_h_down_rect = pygame.Rect(0, 0, 20, 15)
        
        self.valider_btn = pygame.Rect(0, 0, 120, 40)
        self.fermer_btn = pygame.Rect(0, 0, 120, 40)
        
        self.placed_runes = 0
        self.placed_heroes = 0
        self.placed_start_flags = 0
        self.placed_end_flags = 0
        self.placed_gems = 0
        self.placed_enemies = 0
        
    def load_level(self, world, level):
        self.world = world
        self.level = level
        self.camera_offset = pygame.math.Vector2(0, 0)

    def _update_layout(self):
        sw = self.display_surface.get_width()
        sh = self.display_surface.get_height()
        
        self.sidebar_w = sw // 5
        self.sidebar_rect = pygame.Rect(sw - self.sidebar_w, 0, self.sidebar_w, sh)
        
        self.main_tab_rects = []
        main_tab_w = self.sidebar_w // 2
        for i, tab in enumerate(self.main_tabs):
            rect = pygame.Rect(sw - self.sidebar_w + i * main_tab_w, 0, main_tab_w, 40)
            self.main_tab_rects.append(rect)
            
        self.sub_tab_rects = []
        if self.active_main_tab == "Jeu":
            sub_tab_w = self.sidebar_w // 3
            for i, tab in enumerate(self.sub_tabs):
                rect = pygame.Rect(sw - self.sidebar_w + i * sub_tab_w, 40, sub_tab_w, 40)
                self.sub_tab_rects.append(rect)
            
        self.settings_btn.y = sh - 50
        self.popup_rect.center = (sw // 2, sh // 2)
        self.btn_w_rect.topleft = (self.popup_rect.x + 230, self.popup_rect.y + 80)
        self.btn_h_rect.topleft = (self.popup_rect.x + 230, self.popup_rect.y + 140)
        
        self.btn_w_up_rect.topleft = (self.btn_w_rect.right + 5, self.btn_w_rect.y)
        self.btn_w_down_rect.topleft = (self.btn_w_rect.right + 5, self.btn_w_rect.y + 15)
        self.btn_h_up_rect.topleft = (self.btn_h_rect.right + 5, self.btn_h_rect.y)
        self.btn_h_down_rect.topleft = (self.btn_h_rect.right + 5, self.btn_h_rect.y + 15)

        self.valider_btn.topleft = (self.popup_rect.x + 85, self.popup_rect.bottom - 60)
        self.fermer_btn.topleft = (self.popup_rect.x + 245, self.popup_rect.bottom - 60)

    def handle_events(self, event):
        self._update_layout()
        if self.show_settings:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.btn_w_rect.collidepoint(mouse_pos):
                        self.active_input = 'w'
                    elif self.btn_h_rect.collidepoint(mouse_pos):
                        self.active_input = 'h'
                    elif self.btn_w_up_rect.collidepoint(mouse_pos):
                        if self.map_w_str.isdigit(): self.map_width = max(50, int(self.map_w_str))
                        self.map_width += 1
                        self.map_w_str = str(self.map_width)
                        self.held_arrow = 'w_up'
                        self.arrow_timer = 0.4
                    elif self.btn_w_down_rect.collidepoint(mouse_pos):
                        if self.map_w_str.isdigit(): self.map_width = max(50, int(self.map_w_str))
                        if self.map_width > 50: self.map_width -= 1
                        self.map_w_str = str(self.map_width)
                        self.held_arrow = 'w_down'
                        self.arrow_timer = 0.4
                    elif self.btn_h_up_rect.collidepoint(mouse_pos):
                        if self.map_h_str.isdigit(): self.map_height = max(50, int(self.map_h_str))
                        self.map_height += 1
                        self.map_h_str = str(self.map_height)
                        self.held_arrow = 'h_up'
                        self.arrow_timer = 0.4
                    elif self.btn_h_down_rect.collidepoint(mouse_pos):
                        if self.map_h_str.isdigit(): self.map_height = max(50, int(self.map_h_str))
                        if self.map_height > 50: self.map_height -= 1
                        self.map_h_str = str(self.map_height)
                        self.held_arrow = 'h_down'
                        self.arrow_timer = 0.4
                    else:
                        self.active_input = None
                        
                    if self.valider_btn.collidepoint(mouse_pos):
                        if self.map_w_str.isdigit(): 
                            self.map_width = max(50, int(self.map_w_str))
                        if self.map_h_str.isdigit(): 
                            self.map_height = max(50, int(self.map_h_str))
                        self.map_w_str = str(self.map_width)
                        self.map_h_str = str(self.map_height)
                        self.show_settings = False
                    elif self.fermer_btn.collidepoint(mouse_pos):
                        self.map_w_str = str(self.map_width)
                        self.map_h_str = str(self.map_height)
                        self.show_settings = False
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.held_arrow = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_settings = False
                elif self.active_input:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_input == 'w': self.map_w_str = self.map_w_str[:-1]
                        else: self.map_h_str = self.map_h_str[:-1]
                    elif event.unicode.isdigit():
                        if self.active_input == 'w': self.map_w_str += event.unicode
                        else: self.map_h_str += event.unicode
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.settings_btn.collidepoint(mouse_pos):
                    self.show_settings = True
                    return
                if self.back_btn.collidepoint(mouse_pos):
                    self.back_callback()
                    return
                if self.save_btn.collidepoint(mouse_pos):
                    print("Sauvegarde du niveau...")
                    return
                
                for i, rect in enumerate(self.main_tab_rects):
                    if rect.collidepoint(mouse_pos):
                        self.active_main_tab = self.main_tabs[i]
                        return
                        
                if self.active_main_tab == "Jeu":
                    for i, rect in enumerate(self.sub_tab_rects):
                        if rect.collidepoint(mouse_pos):
                            self.active_sub_tab = self.sub_tabs[i]
                            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back_callback()

    def update(self, dt):
        if self.show_settings:
            if self.held_arrow:
                self.arrow_timer -= dt
                if self.arrow_timer <= 0:
                    self.arrow_timer = 0.05
                    if self.held_arrow == 'w_up':
                        self.map_width += 1
                        self.map_w_str = str(self.map_width)
                    elif self.held_arrow == 'w_down':
                        if self.map_width > 50: self.map_width -= 1
                        self.map_w_str = str(self.map_width)
                    elif self.held_arrow == 'h_up':
                        self.map_height += 1
                        self.map_h_str = str(self.map_height)
                    elif self.held_arrow == 'h_down':
                        if self.map_height > 50: self.map_height -= 1
                        self.map_h_str = str(self.map_height)
            return
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
        
        playable_w = sw - self.sidebar_w
        
        map_pixel_w = self.map_width * self.grid_size
        map_pixel_h = self.map_height * self.grid_size
        
        map_screen_x_start = int(self.camera_offset.x)
        map_screen_x_end = map_screen_x_start + map_pixel_w
        map_screen_y_start = int(self.camera_offset.y)
        map_screen_y_end = map_screen_y_start + map_pixel_h
        
        for i in range(self.map_width + 1):
            screen_x = map_screen_x_start + i * self.grid_size
            if 0 <= screen_x <= playable_w:
                y_start = max(0, map_screen_y_start)
                y_end = min(sh, map_screen_y_end)
                if y_start < y_end:
                    pygame.draw.line(self.display_surface, (60, 60, 60), (screen_x, y_start), (screen_x, y_end))
                    
        for j in range(self.map_height + 1):
            screen_y = map_screen_y_start + j * self.grid_size
            if 0 <= screen_y <= sh:
                x_start = max(0, map_screen_x_start)
                x_end = min(playable_w, map_screen_x_end)
                if x_start < x_end:
                    pygame.draw.line(self.display_surface, (60, 60, 60), (x_start, screen_y), (x_end, screen_y))
            
        pygame.draw.rect(self.display_surface, (30, 30, 30), self.sidebar_rect)
        pygame.draw.line(self.display_surface, (100, 100, 100), (sw - self.sidebar_w, 0), (sw - self.sidebar_w, sh), 2)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, rect in enumerate(self.main_tab_rects):
            tab = self.main_tabs[i]
            if tab == self.active_main_tab:
                color = (100, 100, 100)
            elif rect.collidepoint(mouse_pos):
                color = (70, 70, 70)
            else:
                color = (40, 40, 40)
                
            pygame.draw.rect(self.display_surface, color, rect)
            pygame.draw.rect(self.display_surface, (120, 120, 120), rect, 1)
            
            txt = self.font.render(tab, True, (255, 255, 255))
            self.display_surface.blit(txt, txt.get_rect(center=rect.center))
            
        if self.active_main_tab == "Jeu":
            for i, rect in enumerate(self.sub_tab_rects):
                tab = self.sub_tabs[i]
                if tab == self.active_sub_tab:
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
        
        sv_color = (100, 200, 100) if self.save_btn.collidepoint(mouse_pos) else (50, 150, 50)
        pygame.draw.rect(self.display_surface, sv_color, self.save_btn, border_radius=5)
        sv_text = self.font.render("Sauvegarder", True, (255, 255, 255))
        self.display_surface.blit(sv_text, sv_text.get_rect(center=self.save_btn.center))
        
        set_color = (100, 150, 200) if self.settings_btn.collidepoint(mouse_pos) and not self.show_settings else (50, 100, 150)
        pygame.draw.rect(self.display_surface, set_color, self.settings_btn, border_radius=5)
        set_txt = self.font.render("Paramètres", True, (255, 255, 255))
        self.display_surface.blit(set_txt, set_txt.get_rect(center=self.settings_btn.center))
        
        info_text = self.font.render(f"Éditeur - Monde {self.world} Niveau {self.level} | Taille: {self.map_width}x{self.map_height}", True, (255, 255, 255))
        self.display_surface.blit(info_text, (290, 15))
        
        if self.show_settings:
            overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.display_surface.blit(overlay, (0, 0))
            
            pygame.draw.rect(self.display_surface, (50, 50, 50), self.popup_rect, border_radius=10)
            pygame.draw.rect(self.display_surface, (200, 200, 200), self.popup_rect, 2, border_radius=10)
            
            titre = self.font.render("Paramètres de la Carte", True, (255, 255, 255))
            self.display_surface.blit(titre, titre.get_rect(midtop=(self.popup_rect.centerx, self.popup_rect.y + 20)))
            
            lbl_w = self.font.render("Largeur (blocs) :", True, (255, 255, 255))
            self.display_surface.blit(lbl_w, (self.popup_rect.x + 30, self.popup_rect.y + 80))
            w_color = (100, 100, 100) if self.active_input == 'w' else (30, 30, 30)
            pygame.draw.rect(self.display_surface, w_color, self.btn_w_rect)
            txt_w = self.font.render(self.map_w_str, True, (255, 255, 255))
            self.display_surface.blit(txt_w, (self.btn_w_rect.x + 5, self.btn_w_rect.y + 2))
            
            pygame.draw.rect(self.display_surface, (150, 150, 150), self.btn_w_up_rect)
            pygame.draw.polygon(self.display_surface, (0, 0, 0), [(self.btn_w_up_rect.centerx, self.btn_w_up_rect.top + 3), (self.btn_w_up_rect.left + 3, self.btn_w_up_rect.bottom - 3), (self.btn_w_up_rect.right - 3, self.btn_w_up_rect.bottom - 3)])
            pygame.draw.rect(self.display_surface, (150, 150, 150), self.btn_w_down_rect)
            pygame.draw.polygon(self.display_surface, (0, 0, 0), [(self.btn_w_down_rect.centerx, self.btn_w_down_rect.bottom - 3), (self.btn_w_down_rect.left + 3, self.btn_w_down_rect.top + 3), (self.btn_w_down_rect.right - 3, self.btn_w_down_rect.top + 3)])
            
            lbl_h = self.font.render("Hauteur (blocs) :", True, (255, 255, 255))
            self.display_surface.blit(lbl_h, (self.popup_rect.x + 30, self.popup_rect.y + 140))
            h_color = (100, 100, 100) if self.active_input == 'h' else (30, 30, 30)
            pygame.draw.rect(self.display_surface, h_color, self.btn_h_rect)
            txt_h = self.font.render(self.map_h_str, True, (255, 255, 255))
            self.display_surface.blit(txt_h, (self.btn_h_rect.x + 5, self.btn_h_rect.y + 2))

            pygame.draw.rect(self.display_surface, (150, 150, 150), self.btn_h_up_rect)
            pygame.draw.polygon(self.display_surface, (0, 0, 0), [(self.btn_h_up_rect.centerx, self.btn_h_up_rect.top + 3), (self.btn_h_up_rect.left + 3, self.btn_h_up_rect.bottom - 3), (self.btn_h_up_rect.right - 3, self.btn_h_up_rect.bottom - 3)])
            pygame.draw.rect(self.display_surface, (150, 150, 150), self.btn_h_down_rect)
            pygame.draw.polygon(self.display_surface, (0, 0, 0), [(self.btn_h_down_rect.centerx, self.btn_h_down_rect.bottom - 3), (self.btn_h_down_rect.left + 3, self.btn_h_down_rect.top + 3), (self.btn_h_down_rect.right - 3, self.btn_h_down_rect.top + 3)])
            
            start_y = self.popup_rect.y + 200
            cond_title = self.cond_font.render("Conditions de sauvegarde du niveau :", True, (255, 255, 255))
            self.display_surface.blit(cond_title, (self.popup_rect.x + 30, start_y))
            
            conditions = [
                (f"- 3 runes ({self.placed_runes}/3)", self.placed_runes == 3),
                (f"- 1 héros ({self.placed_heroes}/1)", self.placed_heroes == 1),
                (f"- 1 drapeau de début ({self.placed_start_flags}/1)", self.placed_start_flags == 1),
                (f"- 1 drapeau de fin ({self.placed_end_flags}/1)", self.placed_end_flags == 1),
                (f"- 3 gemmes ({self.placed_gems}/3)", self.placed_gems == 3),
            ]
            
            c_y = start_y + 30
            for text, is_ok in conditions:
                color = (100, 255, 100) if is_ok else (255, 100, 100)
                surf = self.cond_font.render(text, True, color)
                self.display_surface.blit(surf, (self.popup_rect.x + 40, c_y))
                c_y += 22
                
            enemy_text = f"- Ennemis présents ({self.placed_enemies})"
            enemy_color = (100, 255, 100) if self.placed_enemies > 0 else (255, 200, 100)
            enemy_surf = self.cond_font.render(enemy_text + (" (Optionnel)" if self.placed_enemies == 0 else ""), True, enemy_color)
            self.display_surface.blit(enemy_surf, (self.popup_rect.x + 40, c_y))

            val_col = (100, 200, 100) if self.valider_btn.collidepoint(mouse_pos) else (50, 150, 50)
            pygame.draw.rect(self.display_surface, val_col, self.valider_btn, border_radius=5)
            val_txt = self.font.render("Valider", True, (255, 255, 255))
            self.display_surface.blit(val_txt, val_txt.get_rect(center=self.valider_btn.center))
            
            fer_col = (200, 100, 100) if self.fermer_btn.collidepoint(mouse_pos) else (150, 50, 50)
            pygame.draw.rect(self.display_surface, fer_col, self.fermer_btn, border_radius=5)
            fer_txt = self.font.render("Fermer", True, (255, 255, 255))
            self.display_surface.blit(fer_txt, fer_txt.get_rect(center=self.fermer_btn.center))
