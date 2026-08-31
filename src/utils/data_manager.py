import json
import os

class DataManager:
    _instance = None
    _data = {}
    
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'data'))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_json(cls, filename: str) -> dict:
        if filename in cls._data:
            return cls._data[filename]
            
        full_path = os.path.join(cls.BASE_PATH, filename)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cls._data[filename] = data
                return data
        except Exception:
            return {}

    @classmethod
    def save_json(cls, filename: str, data: dict) -> bool:
        full_path = os.path.join(cls.BASE_PATH, filename)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            cls._data[filename] = data
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de {filename} : {e}")
            return False
