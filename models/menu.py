from typing import List, Dict, Optional
from models.drink import Drink

class Menu:
    """Menü yönetim sınıfı"""
    
    def __init__(self):
        self.__drinks = []  # Menüdeki tüm içecekler
        self.__categories = set()  # Kategoriler
        self._initialize_default_menu()
    
    def _initialize_default_menu(self):
        """Varsayılan menüyü oluştur"""
        # Sıcak İçecekler
        self.add_drink(Drink("Espresso", 25.0, "Hot", ["Coffee Beans", "Water"], "Small"))
        self.add_drink(Drink("Americano", 30.0, "Hot", ["Espresso", "Water"], "Medium"))
        self.add_drink(Drink("Latte", 35.0, "Hot", ["Espresso", "Milk", "Foam"], "Medium"))
        self.add_drink(Drink("Cappuccino", 40.0, "Hot", ["Espresso", "Milk", "Foam"], "Medium"))
        self.add_drink(Drink("Mocha", 45.0, "Hot", ["Espresso", "Milk", "Chocolate", "Whipped Cream"], "Medium"))
        self.add_drink(Drink("Turkish Coffee", 28.0, "Hot", ["Turkish Coffee", "Water"], "Small"))
        self.add_drink(Drink("Hot Chocolate", 35.0, "Hot", ["Milk", "Chocolate", "Whipped Cream"], "Medium"))
        
        # Soğuk İçecekler
        self.add_drink(Drink("Iced Latte", 38.0, "Cold", ["Espresso", "Milk", "Ice"], "Large"))
        self.add_drink(Drink("Iced Americano", 32.0, "Cold", ["Espresso", "Water", "Ice"], "Large"))
        self.add_drink(Drink("Frappuccino", 48.0, "Cold", ["Espresso", "Milk", "Ice", "Whipped Cream"], "Large"))
        self.add_drink(Drink("Cold Brew", 42.0, "Cold", ["Cold Brew Coffee", "Ice"], "Large"))
        self.add_drink(Drink("Iced Tea", 25.0, "Cold", ["Tea", "Ice", "Lemon"], "Large"))
        
        # Tatlılar
        self.add_drink(Drink("Cheesecake", 55.0, "Dessert", ["Cream Cheese", "Graham Cracker"], "Medium"))
        self.add_drink(Drink("Brownie", 40.0, "Dessert", ["Chocolate", "Flour", "Eggs"], "Medium"))
        self.add_drink(Drink("Tiramisu", 60.0, "Dessert", ["Mascarpone", "Coffee", "Ladyfingers"], "Medium"))
        
        # Yiyecekler
        self.add_drink(Drink("Croissant", 30.0, "Food", ["Flour", "Butter"], "Medium"))
        self.add_drink(Drink("Muffin", 28.0, "Food", ["Flour", "Eggs", "Sugar"], "Medium"))
        self.add_drink(Drink("Sandwich", 45.0, "Food", ["Bread", "Cheese", "Vegetables"], "Medium"))
    
    # Menü yönetimi
    def add_drink(self, drink: Drink):
        """Menüye içecek ekle"""
        if not isinstance(drink, Drink):
            raise TypeError("Sadece Drink objesi eklenebilir!")
        
        # Aynı isim ve boyutta ürün varsa ekleme
        for existing_drink in self.__drinks:
            if existing_drink.name == drink.name and existing_drink.size == drink.size:
                raise ValueError(f"{drink.name} ({drink.size}) zaten menüde!")
        
        self.__drinks.append(drink)
        self.__categories.add(drink.category)
        return True
    
    def remove_drink(self, drink_name: str, size: str = "Medium") -> bool:
        """Menüden içecek çıkar"""
        for i, drink in enumerate(self.__drinks):
            if drink.name == drink_name and drink.size == size:
                self.__drinks.pop(i)
                return True
        return False
    
    def remove_drink_by_id(self, drink_id: int) -> bool:
        """ID'ye göre içecek çıkar"""
        for i, drink in enumerate(self.__drinks):
            if drink.id == drink_id:
                self.__drinks.pop(i)
                return True
        return False
    
    def clear_menu(self):
        """Menüyü temizle"""
        self.__drinks.clear()
        self.__categories.clear()
    
    # Arama ve filtreleme
    def get_drink_by_name(self, name: str, size: str = "Medium") -> Optional[Drink]:
        """İsme ve boyuta göre içecek bul"""
        for drink in self.__drinks:
            if drink.name.lower() == name.lower() and drink.size == size:
                return drink
        return None
    
    def get_drink_by_id(self, drink_id: int) -> Optional[Drink]:
        """ID'ye göre içecek bul"""
        for drink in self.__drinks:
            if drink.id == drink_id:
                return drink
        return None
    
    def search_drinks(self, keyword: str) -> List[Drink]:
        """Anahtar kelimeye göre ara"""
        keyword = keyword.lower()
        results = []
        
        for drink in self.__drinks:
            # İsimde veya malzemelerde ara
            if keyword in drink.name.lower():
                results.append(drink)
            else:
                for ingredient in drink.ingredients:
                    if keyword in ingredient.lower():
                        results.append(drink)
                        break
        
        return results
    
    def get_drinks_by_category(self, category: str) -> List[Drink]:
        """Kategoriye göre filtrele"""
        return [drink for drink in self.__drinks if drink.category == category]
    
    def get_drinks_by_price_range(self, min_price: float, max_price: float) -> List[Drink]:
        """Fiyat aralığına göre filtrele"""
        return [drink for drink in self.__drinks 
                if min_price <= drink.get_final_price() <= max_price]
    
    def get_all_drinks(self) -> List[Drink]:
        """Tüm içecekleri getir"""
        return self.__drinks.copy()
    
    def get_categories(self) -> List[str]:
        """Tüm kategorileri getir"""
        return sorted(list(self.__categories))
    
    # Sıralama
    def get_drinks_sorted_by_price(self, ascending: bool = True) -> List[Drink]:
        """Fiyata göre sırala"""
        return sorted(self.__drinks, key=lambda d: d.get_final_price(), reverse=not ascending)
    
    def get_drinks_sorted_by_name(self) -> List[Drink]:
        """İsme göre sırala"""
        return sorted(self.__drinks, key=lambda d: d.name)
    
    # İstatistikler
    def get_menu_statistics(self) -> Dict:
        """Menü istatistikleri"""
        if not self.__drinks:
            return {
                "total_items": 0,
                "categories": [],
                "avg_price": 0,
                "min_price": 0,
                "max_price": 0
            }
        
        prices = [drink.get_final_price() for drink in self.__drinks]
        
        return {
            "total_items": len(self.__drinks),
            "categories": self.get_categories(),
            "avg_price": sum(prices) / len(prices),
            "min_price": min(prices),
            "max_price": max(prices),
            "items_per_category": {
                category: len(self.get_drinks_by_category(category))
                for category in self.__categories
            }
        }
    
    def get_most_expensive_drink(self) -> Optional[Drink]:
        """En pahalı içecek"""
        if not self.__drinks:
            return None
        return max(self.__drinks, key=lambda d: d.get_final_price())
    
    def get_cheapest_drink(self) -> Optional[Drink]:
        """En ucuz içecek"""
        if not self.__drinks:
            return None
        return min(self.__drinks, key=lambda d: d.get_final_price())
    
    # Görsel gösterim
    def display_menu(self, category: Optional[str] = None):
        """Menüyü ekrana yazdır"""
        drinks = self.get_drinks_by_category(category) if category else self.__drinks
        
        if not drinks:
            print("Menüde ürün yok!")
            return
        
        print("\n" + "="*60)
        title = f"☕ {category.upper() if category else 'TÜM'} MENÜ ☕"
        print(f"{title:^60}")
        print("="*60)
        
        current_category = None
        for drink in sorted(drinks, key=lambda d: d.category):
            if drink.category != current_category:
                current_category = drink.category
                print(f"\n📋 {current_category}:")
                print("-"*60)
            
            # İkon seç
            icon = "☕" if drink.category == "Hot" else "🧊" if drink.category == "Cold" else "🍰" if drink.category == "Dessert" else "🥐"
            
            print(f"{icon} {drink.id}. {drink.name} ({drink.size})")
            print(f"   Fiyat: {drink.get_final_price():.2f}₺")
            print(f"   Malzemeler: {', '.join(drink.ingredients)}")
            print()
        
        print("="*60 + "\n")
    
    def display_menu_simple(self):
        """Basit menü gösterimi (sipariş için)"""
        if not self.__drinks:
            print("Menüde ürün yok!")
            return
        
        print("\n" + "="*60)
        print(f"{'☕ MENÜ ☕':^60}")
        print("="*60 + "\n")
        
        for i, drink in enumerate(self.__drinks, 1):
            icon = "☕" if drink.category == "Hot" else "🧊" if drink.category == "Cold" else "🍰" if drink.category == "Dessert" else "🥐"
            print(f"{i}. {icon} {drink.name:<20} ({drink.size:<6}) - {drink.get_final_price():>6.2f}₺")
        
        print("\n" + "="*60 + "\n")
    
    # Dunder methods
    def __len__(self) -> int:
        """len(menu) -> ürün sayısı"""
        return len(self.__drinks)
    
    def __contains__(self, item) -> bool:
        """'Latte' in menu kontrolü"""
        if isinstance(item, str):
            return any(drink.name.lower() == item.lower() for drink in self.__drinks)
        elif isinstance(item, Drink):
            return item in self.__drinks
        return False
    
    def __getitem__(self, index: int) -> Drink:
        """menu[0] erişimi"""
        return self.__drinks[index]
    
    def __iter__(self):
        """for drink in menu iterasyonu"""
        return iter(self.__drinks)
    
    def __str__(self) -> str:
        return f"Menu: {len(self.__drinks)} items in {len(self.__categories)} categories"
    
    def __repr__(self) -> str:
        return f"Menu(items={len(self.__drinks)}, categories={list(self.__categories)})"
    
    # JSON için
    def to_dict(self) -> Dict:
        return {
            "drinks": [drink.to_dict() for drink in self.__drinks],
            "categories": list(self.__categories),
            "statistics": self.get_menu_statistics()
        }