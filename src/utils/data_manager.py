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
