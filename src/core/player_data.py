import json
import os

class PlayerData:
    def __init__(self):
        self.save_path = "save.json"
        self.coins = 1000
        self.owned_heroes = ["Hero 02"]
        self.load_data()

    def load_data(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.coins = data.get('coins', 1000)
                    self.owned_heroes = data.get('owned_heroes', ["Hero 02"])
            except Exception:
                pass

    def save_data(self):
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump({'coins': self.coins, 'owned_heroes': self.owned_heroes}, f)
        except Exception:
            pass

    def buy_hero(self, hero_id, price):
        if hero_id not in self.owned_heroes and self.coins >= price:
            self.coins -= price
            self.owned_heroes.append(hero_id)
            self.save_data()
            return True
        return False
