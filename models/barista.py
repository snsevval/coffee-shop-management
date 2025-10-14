from typing import List, Dict
from datetime import datetime, timedelta

class Barista:
    """Barista (çalışan) sınıfı"""
    
    _id_counter = 1
    
    def __init__(self, name: str, email: str, experience_years: int = 0, hourly_rate: float = 50.0):
        """
        Args:
            name: Barista adı
            email: Email
            experience_years: Tecrübe yılı
            hourly_rate: Saatlik ücret (₺)
        """
        self.__id = Barista._id_counter
        Barista._id_counter += 1
        
        self.__name = name
        self.__email = email
        self.__experience_years = experience_years
        self.__hourly_rate = hourly_rate
        self.__orders_completed = []  # Tamamlanan siparişler
        self.__current_order = None  # Şu an hazırladığı sipariş
        self.__total_earnings = 0.0
        self.__shift_start = None
        self.__shift_end = None
        self.__is_on_duty = False
        self.__performance_rating = 5.0  # 5 üzerinden
    
    # Properties
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def experience_years(self) -> int:
        return self.__experience_years
    
    @property
    def hourly_rate(self) -> float:
        return self.__hourly_rate
    
    @hourly_rate.setter
    def hourly_rate(self, value: float):
        if value < 0:
            raise ValueError("Saatlik ücret negatif olamaz!")
        self.__hourly_rate = value
    
    @property
    def current_order(self):
        return self.__current_order
    
    @property
    def is_on_duty(self) -> bool:
        return self.__is_on_duty
    
    @property
    def is_available(self) -> bool:
        """Barista müsait mi? (vardiyada ve sipariş hazırlamıyor)"""
        return self.__is_on_duty and self.__current_order is None
    
    @property
    def performance_rating(self) -> float:
        return self.__performance_rating
    
    @property
    def total_orders_completed(self) -> int:
        return len(self.__orders_completed)
    
    # Vardiya yönetimi
    def start_shift(self):
        """Vardiyaya başla"""
        if self.__is_on_duty:
            raise ValueError(f"{self.__name} zaten vardiyada!")
        
        self.__is_on_duty = True
        self.__shift_start = datetime.now()
        return True
    
    def end_shift(self):
        """Vardiyayı bitir"""
        if not self.__is_on_duty:
            raise ValueError(f"{self.__name} vardiyada değil!")
        
        if self.__current_order:
            raise ValueError("Devam eden sipariş var! Önce siparişi tamamlayın.")
        
        self.__is_on_duty = False
        self.__shift_end = datetime.now()
        
        # Vardiya süresine göre kazancı hesapla
        shift_hours = self.get_shift_hours()
        earnings = shift_hours * self.__hourly_rate
        self.__total_earnings += earnings
        
        return earnings
    
    def get_shift_hours(self) -> float:
        """Vardiya saati hesapla"""
        if self.__shift_start:
            end_time = self.__shift_end if self.__shift_end else datetime.now()
            delta = end_time - self.__shift_start
            return delta.total_seconds() / 3600
        return 0.0
    
    # Sipariş hazırlama
    def take_order(self, order):
        """Sipariş al ve hazırlamaya başla"""
        if not self.__is_on_duty:
            raise ValueError(f"{self.__name} vardiyada değil!")
        
        if self.__current_order:
            raise ValueError(f"{self.__name} zaten bir sipariş hazırlıyor!")
        
        if order.status.value != "Beklemede":
            raise ValueError("Bu sipariş hazırlanamaz!")
        
        self.__current_order = order
        order.start_preparation(self)
        return True
    
    def complete_order(self):
        """Mevcut siparişi tamamla"""
        if not self.__current_order:
            raise ValueError("Hazırlanan sipariş yok!")
        
        # Siparişi hazır olarak işaretle
        self.__current_order.mark_as_ready()
        
        # Tamamlanan siparişlere ekle
        self.__orders_completed.append({
            "order_id": self.__current_order.id,
            "customer": self.__current_order.customer.name,
            "completed_at": datetime.now().isoformat(),
            "total": self.__current_order.total_price
        })
        
        # Mevcut siparişi temizle
        self.__current_order = None
        
        return True
    
    def cancel_current_order(self):
        """Mevcut siparişi iptal et"""
        if not self.__current_order:
            raise ValueError("Hazırlanan sipariş yok!")
        
        self.__current_order = None
        return True
    
    # Performans hesaplama
    def calculate_efficiency(self) -> float:
        """Verimlilik hesapla (sipariş/saat)"""
        shift_hours = self.get_shift_hours()
        if shift_hours == 0:
            return 0.0
        return self.total_orders_completed / shift_hours
    
    def update_rating(self, new_rating: float):
        """Performans puanını güncelle"""
        if not 0 <= new_rating <= 5:
            raise ValueError("Puan 0-5 arasında olmalı!")
        
        # Ortalama al (mevcut ve yeni puanın ortalaması)
        self.__performance_rating = (self.__performance_rating + new_rating) / 2
    
    # İstatistikler
    def get_statistics(self) -> Dict:
        """Barista istatistikleri"""
        return {
            "total_orders": self.total_orders_completed,
            "total_earnings": self.__total_earnings,
            "efficiency": self.calculate_efficiency(),
            "performance_rating": self.__performance_rating,
            "experience_years": self.__experience_years,
            "current_status": "Vardiyada" if self.__is_on_duty else "Vardiya Dışı",
            "availability": "Müsait" if self.is_available else "Meşgul"
        }
    
    def get_today_orders(self) -> List[Dict]:
        """Bugün tamamlanan siparişler"""
        today = datetime.now().date()
        today_orders = []
        
        for order_info in self.__orders_completed:
            order_date = datetime.fromisoformat(order_info["completed_at"]).date()
            if order_date == today:
                today_orders.append(order_info)
        
        return today_orders
    
    # Tecrübeye göre bonus hesaplama
    def get_experience_bonus(self) -> float:
        """Tecrübeye göre bonus katsayısı"""
        if self.__experience_years >= 5:
            return 1.5  # %50 bonus
        elif self.__experience_years >= 3:
            return 1.3  # %30 bonus
        elif self.__experience_years >= 1:
            return 1.1  # %10 bonus
        return 1.0  # Bonus yok
    
    def calculate_monthly_salary(self, hours_per_month: float = 160) -> float:
        """Aylık maaş tahmini (tecrübe bonusu dahil)"""
        base_salary = self.__hourly_rate * hours_per_month
        bonus_multiplier = self.get_experience_bonus()
        return base_salary * bonus_multiplier
    
    # Dunder methods
    def __str__(self) -> str:
        status = "🟢 Müsait" if self.is_available else "🔴 Meşgul" if self.__is_on_duty else "⚫ Vardiya Dışı"
        return f"{self.__name} ({self.__experience_years} yıl tecrübe) - {status} - {self.total_orders_completed} sipariş"
    
    def __repr__(self) -> str:
        return f"Barista(id={self.__id}, name='{self.__name}', experience={self.__experience_years})"
    
    def __eq__(self, other) -> bool:
        """İki barista aynı mı?"""
        if not isinstance(other, Barista):
            return False
        return self.__id == other.__id
    
    def __lt__(self, other) -> bool:
        """Performansa göre karşılaştırma"""
        if not isinstance(other, Barista):
            return NotImplemented
        return self.__performance_rating < other.__performance_rating
    
    # JSON için
    def to_dict(self) -> Dict:
        return {
            "id": self.__id,
            "name": self.__name,
            "email": self.__email,
            "experience_years": self.__experience_years,
            "hourly_rate": self.__hourly_rate,
            "total_orders_completed": self.total_orders_completed,
            "total_earnings": self.__total_earnings,
            "is_on_duty": self.__is_on_duty,
            "performance_rating": self.__performance_rating,
            "statistics": self.get_statistics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Dictionary'den Barista oluştur"""
        return cls(
            name=data["name"],
            email=data["email"],
            experience_years=data["experience_years"],
            hourly_rate=data["hourly_rate"]
        )