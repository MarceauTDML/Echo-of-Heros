import os
import pygame

class ResourceLoader:
    _instance = None
    _images = {}
    
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceLoader, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_image(cls, path: str, alpha: bool = True) -> pygame.Surface:
        if path in cls._images:
            return cls._images[path]
            
        full_path = os.path.join(cls.BASE_PATH, path)
        try:
            image = pygame.image.load(full_path)
            if alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            cls._images[path] = image
            return image
        except Exception:
            surf = pygame.Surface((64, 64))
            surf.fill((255, 0, 255))
            return surf

    @classmethod
    def preload_world_1(cls):
        world1_path = os.path.join(cls.BASE_PATH, 'world1')
        if os.path.exists(world1_path):
            for filename in os.listdir(world1_path):
                if filename.endswith('.png'):
                    cls.load_image(os.path.join('world1', filename))
