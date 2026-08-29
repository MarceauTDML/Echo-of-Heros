import sys
import pygame
from src.core.game import Game

def main():
    pygame.init()
    pygame.mixer.init()
    
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"A critical error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
