import pygame
import os
from src.settings import *
from src.utils.data_manager import DataManager

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
        self.sidebar_scroll = 0
        
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
        
        self.layers = [
            "Fonds (Parallaxe)",
            "Décors de fond",
            "Terrain & Objets",
            "Entités",
            "Premier plan"
        ]
        self.active_layer = "Terrain & Objets"
        self.layer_rects = []
        self.level_data = {layer: {} for layer in self.layers}
        self.selected_item = None
        self.item_rects = []
        
        self.tiles = []
        self.tiles_error_msg = ""
        self.hero_animations = {}
        self.enemy_animations = {}
        self.enemies_error_msg = ""
        self.enemy_anim_timer = 0
        
        self.decors = []
        self.decors_animations = {}
        self.decors_error_msg = ""
        
        self._load_tiles()
        self._load_entities()
        self._load_decors()
        
    def _scale_img(self, img):
        scale = self.grid_size / 16
        w, h = img.get_size()
        return pygame.transform.scale(img, (int(w * scale), int(h * scale)))

    def _load_tiles(self):
        self.tiles = []
        self.tiles_error_msg = ""
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', f'world{self.world}', 'tiles'))
        if not os.path.exists(base_path):
            self.tiles_error_msg = f"Le dossier 'assets/world{self.world}/tiles' n'existe pas encore."
            return
            
        try:
            for file in os.listdir(base_path):
                if file.endswith('.png'):
                    try:
                        img = pygame.image.load(os.path.join(base_path, file)).convert_alpha()
                        img_scaled = pygame.transform.scale(img, (self.grid_size, self.grid_size))
                        self.tiles.append((file, img_scaled))
                    except Exception:
                        pass
        except Exception as e:
            self.tiles_error_msg = f"Erreur de lecture: {e}"

    def _load_entities(self):
        self.hero_animations = {}
        self.enemy_animations = {}
        self.enemies_error_msg = ""
        
        hero_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'heros'))
        if os.path.exists(hero_path):
            heroes_data = DataManager().load_json('heroes.json')
            base_hero = None
            for h_id, h_info in heroes_data.items():
                if h_info.get('price') == 0:
                    base_hero = h_id
                    break
                    
            if base_hero:
                temp_dict = {base_hero: []}
                for file in os.listdir(hero_path):
                    if file.startswith(base_hero) and '_Idle_' in file and file.endswith('.png'):
                        temp_dict[base_hero].append(file)
                
                temp_dict[base_hero].sort()
                frames = []
                for file in temp_dict[base_hero]:
                    try:
                        img = pygame.image.load(os.path.join(hero_path, file)).convert_alpha()
                        img = self._scale_img(img)
                        frames.append(img)
                    except Exception:
                        pass
                if frames:
                    display_name = heroes_data[base_hero].get('name', base_hero)
                    self.hero_animations[display_name] = frames
                    
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', f'world{self.world}', 'enemies'))
        if not os.path.exists(base_path):
            self.enemies_error_msg = f"Le dossier 'assets/world{self.world}/enemies' n'existe pas encore."
            return
            
        try:
            temp_dict = {}
            for file in os.listdir(base_path):
                if file.endswith('.png') and '_Idle_' in file:
                    enemy_name = file.split('_Idle_')[0]
                    if enemy_name not in temp_dict:
                        temp_dict[enemy_name] = []
                    temp_dict[enemy_name].append(file)
            
            for name, files in temp_dict.items():
                files.sort()
                frames = []
                for file in files:
                    try:
                        img = pygame.image.load(os.path.join(base_path, file)).convert_alpha()
                        img = self._scale_img(img)
                        frames.append(img)
                    except Exception:
                        pass
                if frames:
                    self.enemy_animations[name] = frames
                    
        except Exception as e:
            self.enemies_error_msg = f"Erreur de lecture: {e}"

    def _load_decors(self):
        self.decors = []
        self.decors_animations = {}
        self.decors_error_msg = ""
        
        all_worlds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'all_worlds'))
        if os.path.exists(all_worlds_path):
            try:
                coin_files = []
                for file in os.listdir(all_worlds_path):
                    if file.startswith('Coins') and file.endswith('.png'):
                        coin_files.append(file)
                if coin_files:
                    coin_files.sort()
                    frames = []
                    for file in coin_files:
                        try:
                            img = pygame.image.load(os.path.join(all_worlds_path, file)).convert_alpha()
                            img = self._scale_img(img)
                            frames.append(img)
                        except Exception:
                            pass
                    if frames:
                        self.decors_animations["Coins"] = frames
            except Exception:
                pass
                
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', f'world{self.world}', 'decors'))
        if not os.path.exists(base_path):
            self.decors_error_msg = f"Le dossier 'assets/world{self.world}/decors' n'existe pas encore."
            return
            
        try:
            anim_temp = {}
            for file in os.listdir(base_path):
                if file.endswith('.png'):
                    name_without_ext = file[:-4]
                    if '_' in name_without_ext:
                        base_name, frame = name_without_ext.rsplit('_', 1)
                        if 'Crystal Blue' in base_name:
                            if base_name not in anim_temp:
                                anim_temp[base_name] = []
                            anim_temp[base_name].append(file)
                        else:
                            if frame == '1':
                                try:
                                    img = pygame.image.load(os.path.join(base_path, file)).convert_alpha()
                                    img = self._scale_img(img)
                                    self.decors.append((name_without_ext, img))
                                except Exception:
                                    pass
                    else:
                        try:
                            img = pygame.image.load(os.path.join(base_path, file)).convert_alpha()
                            img = self._scale_img(img)
                            self.decors.append((name_without_ext, img))
                        except Exception:
                            pass
                            
            for name, files in anim_temp.items():
                files.sort()
                frames = []
                for file in files:
                    try:
                        img = pygame.image.load(os.path.join(base_path, file)).convert_alpha()
                        img = self._scale_img(img)
                        frames.append(img)
                    except Exception:
                        pass
                if frames:
                    self.decors_animations[name] = frames
                    
        except Exception as e:
            self.decors_error_msg = f"Erreur de lecture: {e}"
            

        
    def load_level(self, world, level):
        self.world = world
        self.level = level
        self.camera_offset = pygame.math.Vector2(0, 0)
        self._load_tiles()
        self._load_entities()
        self._load_decors()
        
        filename = f"world{self.world}_level{self.level}.json"
        data = DataManager.load_json(filename)
        if data:
            self.map_width = data.get("width", 100)
            self.map_height = data.get("height", 50)
            self.map_w_str = str(self.map_width)
            self.map_h_str = str(self.map_height)
            layers_data = data.get("layers", {})
            for layer_name in self.layers:
                self.level_data[layer_name] = {}
                if layer_name in layers_data:
                    for item_data in layers_data[layer_name]:
                        x, y = item_data["x"], item_data["y"]
                        itype, iname = item_data["type"], item_data["name"]
                        
                        iimg = None
                        if itype == "Blocs":
                            for fn, img in self.tiles:
                                if fn == iname:
                                    iimg = img
                                    break
                        elif itype == "Décors":
                            for dn, img in self.decors:
                                if dn == iname:
                                    iimg = img
                                    break
                            if not iimg and iname in self.decors_animations:
                                iimg = self.decors_animations[iname]
                        elif itype == "Entités":
                            if iname in self.hero_animations:
                                iimg = self.hero_animations[iname]
                            elif iname in self.enemy_animations:
                                iimg = self.enemy_animations[iname]
                                
                        if iimg is not None:
                            self.level_data[layer_name][(x, y)] = (itype, iname, iimg)

    def _update_stats(self):
        self.placed_heroes = 0
        self.placed_enemies = 0
        self.placed_runes = 0
        self.placed_start_flags = 0
        self.placed_end_flags = 0
        self.placed_gems = 0
        
        for layer_name, layer_dict in self.level_data.items():
            for (gx, gy), item in layer_dict.items():
                if len(item) == 3:
                    itype, iname, _ = item
                    if itype == "Entités":
                        if iname in self.hero_animations:
                            self.placed_heroes += 1
                        elif iname in self.enemy_animations:
                            self.placed_enemies += 1
                    elif itype == "Décors":
                        name_lower = iname.lower()
                        if "rune" in name_lower:
                            self.placed_runes += 1
                        elif "gem" in name_lower or "crystal" in name_lower:
                            self.placed_gems += 1
                        elif "flag" in name_lower or "start" in name_lower:
                            if "end" in name_lower or "fin" in name_lower:
                                self.placed_end_flags += 1
                            else:
                                self.placed_start_flags += 1

    def _save_level(self):
        self._update_stats()
        is_valid = (
            self.placed_runes >= 3 and 
            self.placed_heroes == 1 and 
            self.placed_start_flags >= 1 and 
            self.placed_end_flags >= 1 and 
            self.placed_gems >= 3
        )
        
        serializable_data = {}
        for layer_name, layer_dict in self.level_data.items():
            serializable_data[layer_name] = []
            for (gx, gy), item in layer_dict.items():
                if len(item) == 3:
                    itype, iname, _ = item
                    serializable_data[layer_name].append({
                        "x": gx,
                        "y": gy,
                        "type": itype,
                        "name": iname
                    })
                    
        level_json = {
            "width": self.map_width,
            "height": self.map_height,
            "is_published": is_valid,
            "layers": serializable_data
        }
        
        filename = f"world{self.world}_level{self.level}.json"
        success = DataManager.save_json(filename, level_json)
        if success:
            status = "Publié" if is_valid else "Brouillon"
            print(f"Niveau sauvegardé avec succès ({status}) : {filename}")
        else:
            print("Erreur lors de la sauvegarde du niveau.")

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
                
        self.layer_rects = []
        if self.active_main_tab == "Calques":
            layer_h = 50
            for i, layer in enumerate(self.layers):
                rect = pygame.Rect(sw - self.sidebar_w + 10, 80 + i * (layer_h + 10), self.sidebar_w - 20, layer_h)
                self.layer_rects.append(rect)
            
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

        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.sidebar_rect.collidepoint(mouse_pos):
                self.sidebar_scroll -= event.y * 20
                if self.sidebar_scroll < 0: self.sidebar_scroll = 0

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
                    self._save_level()
                    return
                
                for i, rect in enumerate(self.main_tab_rects):
                    if rect.collidepoint(mouse_pos):
                        if self.active_main_tab != self.main_tabs[i]:
                            self.active_main_tab = self.main_tabs[i]
                            self.sidebar_scroll = 0
                        return
                        
                if self.active_main_tab == "Jeu":
                    for i, rect in enumerate(self.sub_tab_rects):
                        if rect.collidepoint(mouse_pos):
                            if self.active_sub_tab != self.sub_tabs[i]:
                                self.active_sub_tab = self.sub_tabs[i]
                                self.sidebar_scroll = 0
                            return
                            
                    clip_rect = pygame.Rect(self.display_surface.get_width() - self.sidebar_w, 80, self.sidebar_w, self.display_surface.get_height() - 80)
                    if clip_rect.collidepoint(mouse_pos):
                        for item_rect, item_data in self.item_rects:
                            if item_rect.collidepoint(mouse_pos):
                                self.selected_item = item_data
                                return
                                
                elif self.active_main_tab == "Calques":
                    for i, rect in enumerate(self.layer_rects):
                        if rect.collidepoint(mouse_pos):
                            self.active_layer = self.layers[i]
                            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back_callback()

    def update(self, dt):
        self.enemy_anim_timer += dt
        self._update_stats()
        
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
            
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        sw = self.display_surface.get_width()
        playable_w = sw - self.sidebar_w
        
        if mouse_pos[0] < playable_w and not self.show_settings:
            world_x = mouse_pos[0] - self.camera_offset.x
            world_y = mouse_pos[1] - self.camera_offset.y
            grid_x = int(world_x // self.grid_size)
            grid_y = int(world_y // self.grid_size)
            
            if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
                if mouse_pressed[0]:
                    if self.selected_item:
                        self.level_data[self.active_layer][(grid_x, grid_y)] = self.selected_item
                elif mouse_pressed[2]:
                    if (grid_x, grid_y) in self.level_data[self.active_layer]:
                        del self.level_data[self.active_layer][(grid_x, grid_y)]

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
                    
        for layer_name in self.layers:
            layer_dict = self.level_data[layer_name]
            for (gx, gy), item in layer_dict.items():
                screen_x = map_screen_x_start + gx * self.grid_size
                screen_y = map_screen_y_start + gy * self.grid_size
                if -self.grid_size <= screen_x <= playable_w and -self.grid_size <= screen_y <= sh:
                    if len(item) == 3:
                        itype, iname, iimg = item
                        if isinstance(iimg, list):
                            frame_idx = int(self.enemy_anim_timer / 0.1) % len(iimg)
                            img_to_draw = iimg[frame_idx]
                        else:
                            img_to_draw = iimg
                            
                        if itype == "Blocs":
                            self.display_surface.blit(img_to_draw, (screen_x, screen_y))
                        elif itype == "Décors" or itype == "Entités":
                            r = img_to_draw.get_rect(midbottom=(screen_x + self.grid_size // 2, screen_y + self.grid_size))
                            self.display_surface.blit(img_to_draw, r)
                    
        pygame.draw.rect(self.display_surface, (30, 30, 30), self.sidebar_rect)
        pygame.draw.line(self.display_surface, (100, 100, 100), (sw - self.sidebar_w, 0), (sw - self.sidebar_w, sh), 2)
        
        mouse_pos = pygame.mouse.get_pos()
        self.item_rects = []
        
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
                
            if self.active_sub_tab == "Blocs":
                if self.tiles_error_msg:
                    err_font = pygame.font.SysFont('arial', 14, bold=True)
                    words = self.tiles_error_msg.split(' ')
                    lines = []
                    current_line = []
                    for w in words:
                        current_line.append(w)
                        if err_font.size(' '.join(current_line))[0] > self.sidebar_w - 20:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [w]
                    if current_line: lines.append(' '.join(current_line))
                    
                    t_y = 100
                    for line in lines:
                        surf = err_font.render(line, True, (255, 100, 100))
                        self.display_surface.blit(surf, (sw - self.sidebar_w + 10, t_y))
                        t_y += 20
                else:
                    cols = (self.sidebar_w - 20) // (self.grid_size + 10)
                    if cols < 1: cols = 1
                    
                    if self.tiles:
                        total_rows = (len(self.tiles) - 1) // cols + 1
                        total_height = total_rows * (self.grid_size + 10)
                        max_scroll = max(0, total_height - (sh - 100))
                        if self.sidebar_scroll > max_scroll:
                            self.sidebar_scroll = max_scroll
                            
                    clip_rect = pygame.Rect(sw - self.sidebar_w, 80, self.sidebar_w, sh - 80)
                    old_clip = self.display_surface.get_clip()
                    self.display_surface.set_clip(clip_rect)
                    
                    x_start = sw - self.sidebar_w + 10
                    y_start = 100 - self.sidebar_scroll
                    
                    for idx, (filename, img) in enumerate(self.tiles):
                        r = idx // cols
                        c = idx % cols
                        tx = x_start + c * (self.grid_size + 10)
                        ty = y_start + r * (self.grid_size + 10)
                        
                        r_rect = pygame.Rect(tx, ty, self.grid_size, self.grid_size)
                        self.display_surface.blit(img, (tx, ty))
                        
                        if self.selected_item and self.selected_item[0] == "Blocs" and self.selected_item[1] == filename:
                            pygame.draw.rect(self.display_surface, (255, 255, 0), r_rect, 2)
                        else:
                            pygame.draw.rect(self.display_surface, (100, 100, 100), r_rect, 1)
                            
                        self.item_rects.append((r_rect, ("Blocs", filename, img)))
                        
                    self.display_surface.set_clip(old_clip)
                    
            elif self.active_sub_tab == "Décors":
                all_decors = list(self.decors) + [(name, frames) for name, frames in self.decors_animations.items()]
                cols = 3
                cell_size = (self.sidebar_w - 20) // cols
                
                total_height = 0
                if all_decors:
                    total_rows = (len(all_decors) - 1) // cols + 1
                    total_height = total_rows * cell_size
                    
                if self.decors_error_msg:
                    total_height += 60
                    
                max_scroll = max(0, total_height - (sh - 100))
                if self.sidebar_scroll > max_scroll:
                    self.sidebar_scroll = max_scroll
                    
                clip_rect = pygame.Rect(sw - self.sidebar_w, 80, self.sidebar_w, sh - 80)
                old_clip = self.display_surface.get_clip()
                self.display_surface.set_clip(clip_rect)
                
                x_start = sw - self.sidebar_w + 10
                y_start = 100 - self.sidebar_scroll
                
                for idx, item in enumerate(all_decors):
                    r = idx // cols
                    c = idx % cols
                    tx = x_start + c * cell_size
                    ty = y_start + r * cell_size
                    
                    box_rect = pygame.Rect(tx, ty, cell_size, cell_size)
                    pygame.draw.rect(self.display_surface, (50, 50, 50), box_rect)
                    pygame.draw.rect(self.display_surface, (100, 100, 100), box_rect, 1)
                    
                    name = item[0]
                    if isinstance(item[1], list):
                        frames = item[1]
                        frame_idx = int(self.enemy_anim_timer / 0.1) % len(frames)
                        img = frames[frame_idx]
                    else:
                        img = item[1]
                        
                    img_w, img_h = img.get_size()
                    max_dim = cell_size - 10
                    scale = min(max_dim / img_w, max_dim / img_h)
                    new_w, new_h = int(img_w * scale), int(img_h * scale)
                    img = pygame.transform.scale(img, (new_w, new_h))
                        
                    img_rect = img.get_rect(center=box_rect.center)
                    self.display_surface.blit(img, img_rect)
                    
                    if self.selected_item and self.selected_item[0] == "Décors" and self.selected_item[1] == name:
                        pygame.draw.rect(self.display_surface, (255, 255, 0), box_rect, 2)
                    
                    orig_data = item[1]
                    self.item_rects.append((box_rect, ("Décors", name, orig_data)))
                    
                if self.decors_error_msg:
                    err_font = pygame.font.SysFont('arial', 14, bold=True)
                    words = self.decors_error_msg.split(' ')
                    lines = []
                    current_line = []
                    for w in words:
                        current_line.append(w)
                        if err_font.size(' '.join(current_line))[0] > self.sidebar_w - 20:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [w]
                    if current_line: lines.append(' '.join(current_line))
                    
                    err_y = y_start + ((len(all_decors) - 1) // cols + 1) * cell_size if all_decors else y_start
                    
                    for line in lines:
                        surf = err_font.render(line, True, (255, 100, 100))
                        self.display_surface.blit(surf, (x_start, err_y))
                        err_y += 20
                        
                self.display_surface.set_clip(old_clip)
                    
            elif self.active_sub_tab == "Entités":
                all_entities = list(self.hero_animations.items()) + list(self.enemy_animations.items())
                
                total_height = len(all_entities) * 150
                if self.enemies_error_msg:
                    total_height += 60
                    
                max_scroll = max(0, total_height - (sh - 100))
                if self.sidebar_scroll > max_scroll:
                    self.sidebar_scroll = max_scroll
                    
                clip_rect = pygame.Rect(sw - self.sidebar_w, 80, self.sidebar_w, sh - 80)
                old_clip = self.display_surface.get_clip()
                self.display_surface.set_clip(clip_rect)
                
                x_start = sw - self.sidebar_w + 10
                y_start = 100 - self.sidebar_scroll
                
                for entity_name, frames in all_entities:
                    frame_idx = int(self.enemy_anim_timer / 0.1) % len(frames)
                    img = frames[frame_idx]
                    
                    box_rect = pygame.Rect(x_start, y_start, self.sidebar_w - 20, 140)
                    
                    pygame.draw.rect(self.display_surface, (50, 50, 50), box_rect)
                    if entity_name in self.hero_animations:
                        pygame.draw.rect(self.display_surface, (100, 200, 100), box_rect, 2)
                    else:
                        pygame.draw.rect(self.display_surface, (100, 100, 100), box_rect, 2)
                    
                    name_surf = self.tab_font.render(entity_name, True, (255, 255, 255))
                    self.display_surface.blit(name_surf, (x_start + 10, y_start + 10))
                    
                    img_w, img_h = img.get_size()
                    target_h = 90
                    scale = target_h / img_h
                    
                    new_w, new_h = int(img_w * scale), int(img_h * scale)
                    
                    max_w = box_rect.width - 20
                    if new_w > max_w:
                        scale_w = max_w / new_w
                        new_w, new_h = int(new_w * scale_w), int(new_h * scale_w)
                        
                    img = pygame.transform.scale(img, (new_w, new_h))
                        
                    img_rect = img.get_rect(center=(box_rect.centerx, box_rect.centery + 15))
                    self.display_surface.blit(img, img_rect)
                    
                    if self.selected_item and self.selected_item[0] == "Entités" and self.selected_item[1] == entity_name:
                        pygame.draw.rect(self.display_surface, (255, 255, 0), box_rect, 3)
                        
                    self.item_rects.append((box_rect, ("Entités", entity_name, frames)))
                    
                    y_start += 150
                    
                if self.enemies_error_msg:
                    err_font = pygame.font.SysFont('arial', 14, bold=True)
                    words = self.enemies_error_msg.split(' ')
                    lines = []
                    current_line = []
                    for w in words:
                        current_line.append(w)
                        if err_font.size(' '.join(current_line))[0] > self.sidebar_w - 20:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [w]
                    if current_line: lines.append(' '.join(current_line))
                    
                    for line in lines:
                        surf = err_font.render(line, True, (255, 100, 100))
                        self.display_surface.blit(surf, (x_start, y_start))
                        y_start += 20
                        
                self.display_surface.set_clip(old_clip)
                
        elif self.active_main_tab == "Calques":
            for i, rect in enumerate(self.layer_rects):
                layer = self.layers[i]
                
                is_active = (layer == self.active_layer)
                color = (70, 70, 120) if is_active else (50, 50, 50)
                if rect.collidepoint(mouse_pos) and not is_active:
                    color = (60, 60, 60)
                    
                pygame.draw.rect(self.display_surface, color, rect, border_radius=5)
                
                if is_active:
                    pygame.draw.rect(self.display_surface, (200, 200, 255), rect, 2, border_radius=5)
                else:
                    pygame.draw.rect(self.display_surface, (100, 100, 100), rect, 1, border_radius=5)
                    
                txt = self.tab_font.render(layer, True, (255, 255, 255))
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
