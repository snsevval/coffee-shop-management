from typing import List, Dict
from datetime import datetime
from abc import ABC, abstractmethod

class Customer(ABC):
    """Müşteri base class (Abstract)"""
    
    _id_counter = 1
    
    def __init__(self, name: str, email: str, phone: str, balance: float = 0.0):
        self._id = Customer._id_counter
        Customer._id_counter += 1
        
        self._name = name
        self._email = email
        self._phone = phone
        self._balance = balance
        self._order_history = []  # Sipariş geçmişi
        self._created_at = datetime.now()
        self._loyalty_points = 0
    
    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def loyalty_points(self) -> int:
        return self._loyalty_points
    
    @property
    def order_history(self) -> List:
        return self._order_history.copy()
    
    # Balance yönetimi
    def add_balance(self, amount: float):
        """Bakiye ekle"""
        if amount <= 0:
            raise ValueError("Eklenecek miktar pozitif olmalı!")
        self._balance += amount
        return self._balance
    
    def deduct_balance(self, amount: float):
        """Bakiye düş"""
        if amount > self._balance:
            raise ValueError("Yetersiz bakiye!")
        self._balance -= amount
        return self._balance
    
    # Sipariş geçmişine ekle
    def add_to_history(self, order):
        """Siparişi geçmişe ekle"""
        self._order_history.append({
            "order_id": order.id,
            "date": datetime.now().isoformat(),
            "total": order.total_price
        })
    
    # Abstract method - Her müşteri tipi kendi indirimini belirler
    @abstractmethod
    def calculate_discount(self, amount: float) -> float:
        """İndirim hesapla (Her subclass implement etmeli)"""
        pass
    
    # Abstract method - Sadakat puanı hesaplama
    @abstractmethod
    def earn_loyalty_points(self, amount: float):
        """Sadakat puanı kazan"""
        pass
    
    def __str__(self) -> str:
        customer_type = self.__class__.__name__
        return f"{customer_type}: {self._name} (Bakiye: {self._balance:.2f}₺, Puan: {self._loyalty_points})"
    
    def __repr__(self) -> str:
        return f"Customer(id={self._id}, name='{self._name}', balance={self._balance})"
    
    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "balance": self._balance,
            "loyalty_points": self._loyalty_points,
            "order_history": self._order_history,
            "created_at": self._created_at.isoformat(),
            "type": self.__class__.__name__
        }


class RegularCustomer(Customer):
    """Normal müşteri - %0 indirim"""
    
    def __init__(self, name: str, email: str, phone: str, balance: float = 0.0):
        super().__init__(name, email, phone, balance)
        self._discount_rate = 0.0
    
    def calculate_discount(self, amount: float) -> float:
        """Normal müşteriye indirim yok"""
        return 0.0
    
    def earn_loyalty_points(self, amount: float):
        """Her 10₺'ye 1 puan"""
        points = int(amount / 10)
        self._loyalty_points += points


class PremiumCustomer(Customer):
    """Premium müşteri - %10 indirim"""
    
    def __init__(self, name: str, email: str, phone: str, balance: float = 0.0, membership_fee: float = 50.0):
        super().__init__(name, email, phone, balance)
        self._discount_rate = 0.10
        self._membership_fee = membership_fee
        self._free_drinks_count = 0  # Bedava içecek hakkı
    
    @property
    def discount_rate(self) -> float:
        return self._discount_rate
    
    def calculate_discount(self, amount: float) -> float:
        """Premium müşteriye %10 indirim"""
        return amount * self._discount_rate
    
    def earn_loyalty_points(self, amount: float):
        """Her 10₺'ye 2 puan (2x kazanır)"""
        points = int(amount / 10) * 2
        self._loyalty_points += points
    
    def add_free_drink(self):
        """Bedava içecek hakkı ekle"""
        self._free_drinks_count += 1
    
    def use_free_drink(self) -> bool:
        """Bedava içecek kullan"""
        if self._free_drinks_count > 0:
            self._free_drinks_count -= 1
            return True
        return False
    
    def __str__(self) -> str:
        return (f"Premium: {self._name} (Bakiye: {self._balance:.2f}₺, "
                f"Puan: {self._loyalty_points}, Bedava: {self._free_drinks_count})")


class VIPCustomer(Customer):
    """VIP müşteri - %20 indirim + özel avantajlar"""
    
    def __init__(self, name: str, email: str, phone: str, balance: float = 0.0):
        super().__init__(name, email, phone, balance)
        self._discount_rate = 0.20
        self._priority_service = True
    
    @property
    def discount_rate(self) -> float:
        return self._discount_rate
    
    @property
    def has_priority(self) -> bool:
        return self._priority_service
    
    def calculate_discount(self, amount: float) -> float:
        """VIP müşteriye %20 indirim"""
        return amount * self._discount_rate
    
    def earn_loyalty_points(self, amount: float):
        """Her 10₺'ye 3 puan (3x kazanır)"""
        points = int(amount / 10) * 3
        self._loyalty_points += points
    
    def __str__(self) -> str:
        return (f"⭐VIP⭐: {self._name} (Bakiye: {self._balance:.2f}₺, "
                f"Puan: {self._loyalty_points}, Öncelikli Servis)")