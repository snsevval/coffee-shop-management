from typing import List, Dict
from datetime import datetime

class Drink:
    """Kahve dükkanındaki içecekleri temsil eden sınıf"""
    
    # Class variable - tüm içecekler için ortak
    _id_counter = 1
    
    def __init__(self, name: str, price: float, category: str, ingredients: List[str], size: str = "Medium"):
        """
        Args:
            name: İçeceğin adı
            price: Fiyat (TL)
            category: Kategori (Hot/Cold/Dessert)
            ingredients: Malzeme listesi
            size: Boyut (Small/Medium/Large)
        """
        self.__id = Drink._id_counter
        Drink._id_counter += 1
        
        self.__name = name
        self.__price = price
        self.__category = category
        self.__ingredients = ingredients
        self.__size = size
        self.__created_at = datetime.now()
    
    # Property decorators - Encapsulation için
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Fiyat negatif olamaz!")
        self.__price = value
    
    @property
    def category(self) -> str:
        return self.__category
    
    @property
    def ingredients(self) -> List[str]:
        return self.__ingredients.copy()  # Kopya döndür (encapsulation)
    
    @property
    def size(self) -> str:
        return self.__size
    
    @size.setter
    def size(self, value: str):
        valid_sizes = ["Small", "Medium", "Large"]
        if value not in valid_sizes:
            raise ValueError(f"Boyut sadece {valid_sizes} olabilir!")
        self.__size = value
    
    # Boyuta göre fiyat hesaplama (business logic)
    def get_final_price(self) -> float:
        """Boyuta göre fiyat hesapla"""
        size_multipliers = {
            "Small": 0.8,
            "Medium": 1.0,
            "Large": 1.3
        }
        return self.__price * size_multipliers[self.__size]
    
    # Static method - utility function
    @staticmethod
    def is_valid_category(category: str) -> bool:
        """Kategori geçerli mi kontrol et"""
        valid_categories = ["Hot", "Cold", "Dessert", "Food"]
        return category in valid_categories
    
    # Class method - alternatif constructor
    @classmethod
    def create_espresso(cls):
        """Hazır espresso oluştur"""
        return cls("Espresso", 25.0, "Hot", ["Coffee Beans", "Water"], "Small")
    
    @classmethod
    def create_latte(cls):
        """Hazır latte oluştur"""
        return cls("Latte", 35.0, "Hot", ["Espresso", "Milk", "Foam"], "Medium")
    
    # Dunder methods
    def __str__(self) -> str:
        """Kullanıcı dostu gösterim"""
        return f"{self.__name} ({self.__size}) - {self.get_final_price():.2f}₺"
    
    def __repr__(self) -> str:
        """Developer dostu gösterim"""
        return f"Drink(id={self.__id}, name='{self.__name}', price={self.__price}, size='{self.__size}')"
    
    def __eq__(self, other) -> bool:
        """İki içecek eşit mi?"""
        if not isinstance(other, Drink):
            return False
        return self.__name == other.__name and self.__size == other.__size
    
    def __lt__(self, other) -> bool:
        """Fiyat karşılaştırması için"""
        if not isinstance(other, Drink):
            return NotImplemented
        return self.get_final_price() < other.get_final_price()
    
    # JSON'a dönüştürme için
    def to_dict(self) -> Dict:
        """Sınıfı dictionary'e çevir (JSON için)"""
        return {
            "id": self.__id,
            "name": self.__name,
            "price": self.__price,
            "category": self.__category,
            "ingredients": self.__ingredients,
            "size": self.__size,
            "created_at": self.__created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Dictionary'den Drink objesi oluştur"""
        drink = cls(
            name=data["name"],
            price=data["price"],
            category=data["category"],
            ingredients=data["ingredients"],
            size=data["size"]
        )
        return drink