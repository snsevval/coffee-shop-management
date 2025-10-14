from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    """Sipariş durumları (Enum kullanımı)"""
    PENDING = "Beklemede"
    PREPARING = "Hazırlanıyor"
    READY = "Hazır"
    DELIVERED = "Teslim Edildi"
    CANCELLED = "İptal Edildi"


class Order:
    """Sipariş sınıfı - Composition örneği (içinde Drink ve Customer var)"""
    
    _id_counter = 1
    
    def __init__(self, customer, barista=None):
        """
        Args:
            customer: Customer objesi
            barista: Barista objesi (opsiyonel)
        """
        self.__id = Order._id_counter
        Order._id_counter += 1
        
        self.__customer = customer  # Composition: Order "has-a" Customer
        self.__barista = barista
        self.__items = []  # List of (Drink, quantity) tuples
        self.__status = OrderStatus.PENDING
        self.__created_at = datetime.now()
        self.__prepared_at = None
        self.__delivered_at = None
        self.__notes = ""
        self.__discount_applied = 0.0
    
    # Properties
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def customer(self):
        return self.__customer
    
    @property
    def barista(self):
        return self.__barista
    
    @barista.setter
    def barista(self, barista):
        """Barista ata"""
        self.__barista = barista
    
    @property
    def items(self) -> List:
        return self.__items.copy()
    
    @property
    def status(self) -> OrderStatus:
        return self.__status
    
    @property
    def notes(self) -> str:
        return self.__notes
    
    @notes.setter
    def notes(self, value: str):
        self.__notes = value
    
    # Ürün ekleme/çıkarma
    def add_item(self, drink, quantity: int = 1):
        """Siparişe ürün ekle"""
        if quantity <= 0:
            raise ValueError("Miktar pozitif olmalı!")
        
        # Aynı ürün varsa miktarı artır
        for i, (existing_drink, qty) in enumerate(self.__items):
            if existing_drink == drink:
                self.__items[i] = (existing_drink, qty + quantity)
                return
        
        # Yoksa yeni ekle
        self.__items.append((drink, quantity))
    
    def remove_item(self, drink):
        """Siparişten ürün çıkar"""
        self.__items = [(d, q) for d, q in self.__items if d != drink]
    
    def clear_items(self):
        """Tüm ürünleri temizle"""
        self.__items.clear()
    
    # Fiyat hesaplamaları
    def calculate_subtotal(self) -> float:
        """Ara toplam (indirim öncesi)"""
        total = 0.0
        for drink, quantity in self.__items:
            total += drink.get_final_price() * quantity
        return total
    
    def calculate_discount(self) -> float:
        """İndirim miktarını hesapla"""
        subtotal = self.calculate_subtotal()
        discount = self.__customer.calculate_discount(subtotal)
        self.__discount_applied = discount
        return discount
    
    @property
    def total_price(self) -> float:
        """Toplam fiyat (indirim sonrası)"""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        return subtotal - discount
    
    # Sipariş durumu yönetimi
    def start_preparation(self, barista):
        """Hazırlamaya başla"""
        if self.__status != OrderStatus.PENDING:
            raise ValueError("Sadece bekleyen siparişler hazırlanabilir!")
        
        self.__barista = barista
        self.__status = OrderStatus.PREPARING
        return True
    
    def mark_as_ready(self):
        """Hazır olarak işaretle"""
        if self.__status != OrderStatus.PREPARING:
            raise ValueError("Sadece hazırlanan siparişler tamamlanabilir!")
        
        self.__status = OrderStatus.READY
        self.__prepared_at = datetime.now()
        return True
    
    def mark_as_delivered(self):
        """Teslim edildi olarak işaretle"""
        if self.__status != OrderStatus.READY:
            raise ValueError("Sadece hazır siparişler teslim edilebilir!")
        
        self.__status = OrderStatus.DELIVERED
        self.__delivered_at = datetime.now()
        
        # Müşteriye sadakat puanı ekle
        self.__customer.earn_loyalty_points(self.total_price)
        
        # Müşteri geçmişine ekle
        self.__customer.add_to_history(self)
        
        return True
    
    def cancel(self):
        """Siparişi iptal et"""
        if self.__status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise ValueError("Bu sipariş iptal edilemez!")
        
        self.__status = OrderStatus.CANCELLED
        return True
    
    # Ödeme işlemi
    def process_payment(self) -> bool:
        """Ödemeyi işle"""
        total = self.total_price
        
        try:
            self.__customer.deduct_balance(total)
            return True
        except ValueError as e:
            print(f"Ödeme hatası: {e}")
            return False
    
    # Süre hesaplamaları
    def get_preparation_time(self) -> Optional[int]:
        """Hazırlama süresi (dakika)"""
        if self.__prepared_at and self.__status != OrderStatus.PENDING:
            delta = self.__prepared_at - self.__created_at
            return int(delta.total_seconds() / 60)
        return None
    
    def get_waiting_time(self) -> int:
        """Bekleme süresi (dakika)"""
        delta = datetime.now() - self.__created_at
        return int(delta.total_seconds() / 60)
    
    # İstatistikler
    def get_item_count(self) -> int:
        """Toplam ürün sayısı"""
        return sum(quantity for _, quantity in self.__items)
    
    # Dunder methods
    def __str__(self) -> str:
        items_str = ", ".join([f"{q}x {d.name}" for d, q in self.__items])
        return (f"Sipariş #{self.__id} - {self.__customer.name} - "
                f"{self.__status.value} - {self.total_price:.2f}₺ [{items_str}]")
    
    def __repr__(self) -> str:
        return f"Order(id={self.__id}, customer={self.__customer.name}, status={self.__status.value})"
    
    def __len__(self) -> int:
        """len(order) -> ürün sayısı"""
        return self.get_item_count()
    
    def __bool__(self) -> bool:
        """bool(order) -> sipariş dolu mu?"""
        return len(self.__items) > 0
    
    # Detaylı görünüm
    def get_detailed_info(self) -> str:
        """Detaylı sipariş bilgisi"""
        info = f"\n{'='*50}\n"
        info += f"  Sipariş #{self.__id}\n"
        info += f"{'='*50}\n"
        info += f"Müşteri: {self.__customer.name}\n"
        info += f"Durum: {self.__status.value}\n"
        info += f"Sipariş Zamanı: {self.__created_at.strftime('%H:%M:%S')}\n"
        
        if self.__barista:
            info += f"Barista: {self.__barista.name}\n"
        
        info += f"\nÜrünler:\n"
        info += "-" * 50 + "\n"
        
        for drink, quantity in self.__items:
            price = drink.get_final_price() * quantity
            info += f"  {quantity}x {drink.name} ({drink.size})"
            info += f" - {price:.2f}₺\n"
        
        info += "-" * 50 + "\n"
        info += f"Ara Toplam: {self.calculate_subtotal():.2f}₺\n"
        
        if self.__discount_applied > 0:
            info += f"İndirim ({self.__customer.__class__.__name__}): -{self.__discount_applied:.2f}₺\n"
        
        info += f"TOPLAM: {self.total_price:.2f}₺\n"
        
        if self.__notes:
            info += f"\nNot: {self.__notes}\n"
        
        info += "=" * 50 + "\n"
        
        return info
    
    def to_dict(self) -> Dict:
        """JSON için dictionary'e çevir"""
        return {
            "id": self.__id,
            "customer_id": self.__customer.id,
            "customer_name": self.__customer.name,
            "barista_id": self.__barista.id if self.__barista else None,
            "barista_name": self.__barista.name if self.__barista else None,
            "items": [
                {
                    "drink_name": drink.name,
                    "drink_size": drink.size,
                    "quantity": qty,
                    "price": drink.get_final_price()
                }
                for drink, qty in self.__items
            ],
            "status": self.__status.value,
            "subtotal": self.calculate_subtotal(),
            "discount": self.__discount_applied,
            "total": self.total_price,
            "created_at": self.__created_at.isoformat(),
            "prepared_at": self.__prepared_at.isoformat() if self.__prepared_at else None,
            "delivered_at": self.__delivered_at.isoformat() if self.__delivered_at else None,
            "notes": self.__notes
        }