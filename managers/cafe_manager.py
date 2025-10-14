from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os
from models.drink import Drink
from models.customer import Customer, RegularCustomer, PremiumCustomer, VIPCustomer
from models.order import Order, OrderStatus
from models.barista import Barista
from models.menu import Menu

class CafeManager:
    """Kahve dükkanını yöneten ana sınıf (Singleton pattern)"""
    
    _instance = None
    
    def __new__(cls, cafe_name: str = "Coffee Heaven"):
        """Singleton pattern - tek instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, cafe_name: str = "Coffee Heaven"):
        """Initialize sadece bir kez çalışır"""
        if self._initialized:
            return
        
        self.__cafe_name = cafe_name
        self.__menu = Menu()
        self.__customers = []  # Tüm müşteriler
        self.__baristas = []  # Tüm barista'lar
        self.__orders = []  # Tüm siparişler
        self.__pending_orders = []  # Bekleyen siparişler (kuyruk)
        self.__daily_revenue = 0.0
        self.__total_revenue = 0.0
        self.__opening_time = None
        self.__is_open = False
        
        # Başlangıç verilerini yükle
        self._load_data()
        
        self._initialized = True
    
    # Properties
    @property
    def cafe_name(self) -> str:
        return self.__cafe_name
    
    @property
    def menu(self) -> Menu:
        return self.__menu
    
    @property
    def is_open(self) -> bool:
        return self.__is_open
    
    @property
    def daily_revenue(self) -> float:
        return self.__daily_revenue
    
    @property
    def total_revenue(self) -> float:
        return self.__total_revenue
    
    # Kafe yönetimi
    def open_cafe(self):
        """Kafeyi aç"""
        if self.__is_open:
            raise ValueError("Kafe zaten açık!")
        
        self.__is_open = True
        self.__opening_time = datetime.now()
        self.__daily_revenue = 0.0
        
        print(f"\n{'='*60}")
        print(f"☕ {self.__cafe_name} AÇILDI! ☕".center(60))
        print(f"Açılış Saati: {self.__opening_time.strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
        
        return True
    
    def close_cafe(self):
        """Kafeyi kapat"""
        if not self.__is_open:
            raise ValueError("Kafe zaten kapalı!")
        
        # Bekleyen sipariş varsa uyar
        if self.__pending_orders:
            print(f"⚠️  Uyarı: {len(self.__pending_orders)} bekleyen sipariş var!")
        
        # Vardiyada olan barista'ları kapat
        for barista in self.__baristas:
            if barista.is_on_duty:
                earnings = barista.end_shift()
                print(f"✅ {barista.name} vardiyasını bitirdi. Kazanç: {earnings:.2f}₺")
        
        self.__is_open = False
        self.__total_revenue += self.__daily_revenue
        
        # Günlük rapor
        self._print_daily_report()
        
        # Verileri kaydet
        self._save_data()
        
        return True
    
    # Müşteri yönetimi
    def register_customer(self, name: str, email: str, phone: str, 
                         customer_type: str = "Regular", initial_balance: float = 0.0) -> Customer:
        """Yeni müşteri kaydet"""
        # Email kontrolü
        if self.get_customer_by_email(email):
            raise ValueError(f"{email} zaten kayıtlı!")
        
        # Müşteri tipine göre oluştur
        if customer_type.lower() == "regular":
            customer = RegularCustomer(name, email, phone, initial_balance)
        elif customer_type.lower() == "premium":
            customer = PremiumCustomer(name, email, phone, initial_balance)
        elif customer_type.lower() == "vip":
            customer = VIPCustomer(name, email, phone, initial_balance)
        else:
            raise ValueError("Geçersiz müşteri tipi! (Regular/Premium/VIP)")
        
        self.__customers.append(customer)
        print(f"✅ {customer_type} müşteri kaydedildi: {name}")
        
        return customer
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Email'e göre müşteri bul"""
        for customer in self.__customers:
            if customer.email.lower() == email.lower():
                return customer
        return None
    
    def get_customer_by_name(self, name: str) -> Optional[Customer]:
        """İsme göre müşteri bul"""
        for customer in self.__customers:
            if customer.name.lower() == name.lower():
                return customer
        return None
    
    def get_all_customers(self) -> List[Customer]:
        """Tüm müşterileri getir"""
        return self.__customers.copy()
    
    def remove_customer(self, email: str) -> bool:
        """Müşteri sil"""
        customer = self.get_customer_by_email(email)
        if customer:
            self.__customers.remove(customer)
            return True
        return False
    
    # Barista yönetimi
    def hire_barista(self, name: str, email: str, experience_years: int = 0, 
                    hourly_rate: float = 50.0) -> Barista:
        """Yeni barista işe al"""
        # Email kontrolü
        for barista in self.__baristas:
            if barista.email.lower() == email.lower():
                raise ValueError(f"{email} zaten kayıtlı!")
        
        barista = Barista(name, email, experience_years, hourly_rate)
        self.__baristas.append(barista)
        
        print(f"✅ Barista işe alındı: {name} ({experience_years} yıl tecrübe)")
        
        return barista
    
    def fire_barista(self, email: str) -> bool:
        """Barista'yı işten çıkar"""
        for barista in self.__baristas:
            if barista.email.lower() == email.lower():
                if barista.is_on_duty:
                    raise ValueError(f"{barista.name} vardiyada! Önce vardiyayı bitirin.")
                
                self.__baristas.remove(barista)
                return True
        return False
    
    def get_barista_by_email(self, email: str) -> Optional[Barista]:
        """Email'e göre barista bul"""
        for barista in self.__baristas:
            if barista.email.lower() == email.lower():
                return barista
        return None
    
    def get_available_baristas(self) -> List[Barista]:
        """Müsait barista'ları getir"""
        return [b for b in self.__baristas if b.is_available]
    
    def get_all_baristas(self) -> List[Barista]:
        """Tüm barista'ları getir"""
        return self.__baristas.copy()
    
    # Sipariş yönetimi
    def create_order(self, customer: Customer) -> Order:
        """Yeni sipariş oluştur"""
        if not self.__is_open:
            raise ValueError("Kafe kapalı!")
        
        order = Order(customer)
        return order
    
    def submit_order(self, order: Order) -> bool:
        """Siparişi onayla ve kuyruğa ekle"""
        if not self.__is_open:
            raise ValueError("Kafe kapalı!")
        
        if not order or len(order) == 0:
            raise ValueError("Sipariş boş!")
        
        # Ödemeyi işle
        if not order.process_payment():
            raise ValueError("Ödeme başarısız!")
        
        # Siparişleri kaydet
        self.__orders.append(order)
        self.__pending_orders.append(order)
        
        print(f"\n✅ Sipariş #{order.id} alındı!")
        print(f"Müşteri: {order.customer.name}")
        print(f"Toplam: {order.total_price:.2f}₺")
        print(f"Kuyrukta {len(self.__pending_orders)} sipariş var.\n")
        
        return True
    
    def assign_order_to_barista(self, order: Order, barista: Barista) -> bool:
        """Siparişi barista'ya ata"""
        if order not in self.__pending_orders:
            raise ValueError("Bu sipariş bekleyen siparişlerde değil!")
        
        if not barista.is_available:
            raise ValueError(f"{barista.name} müsait değil!")
        
        barista.take_order(order)
        self.__pending_orders.remove(order)
        
        print(f"✅ Sipariş #{order.id}, {barista.name}'e atandı!")
        
        return True
    
    def auto_assign_orders(self):
        """Bekleyen siparişleri otomatik ata"""
        available_baristas = self.get_available_baristas()
        
        if not available_baristas:
            print("⚠️  Müsait barista yok!")
            return
        
        assigned_count = 0
        for barista in available_baristas:
            if not self.__pending_orders:
                break
            
            order = self.__pending_orders[0]
            self.assign_order_to_barista(order, barista)
            assigned_count += 1
        
        if assigned_count > 0:
            print(f"✅ {assigned_count} sipariş otomatik atandı!")
    
    def complete_order(self, order_id: int) -> bool:
        """Siparişi tamamla"""
        order = self.get_order_by_id(order_id)
        
        if not order:
            raise ValueError(f"Sipariş #{order_id} bulunamadı!")
        
        if not order.barista:
            raise ValueError("Bu siparişin barista'sı yok!")
        
        # Barista siparişi tamamlar
        order.barista.complete_order()
        
        # Siparişi teslim et
        order.mark_as_delivered()
        
        # Geliri ekle
        self.__daily_revenue += order.total_price
        
        print(f"✅ Sipariş #{order.id} tamamlandı ve teslim edildi!")
        print(f"Müşteri: {order.customer.name}")
        print(f"Kazanılan puan: +{int(order.total_price / 10)}")
        
        return True
    
    def cancel_order(self, order_id: int) -> bool:
        """Siparişi iptal et"""
        order = self.get_order_by_id(order_id)
        
        if not order:
            raise ValueError(f"Sipariş #{order_id} bulunamadı!")
        
        order.cancel()
        
        # Müşteriye para iade et
        order.customer.add_balance(order.total_price)
        
        # Bekleyen siparişlerden çıkar
        if order in self.__pending_orders:
            self.__pending_orders.remove(order)
        
        print(f"✅ Sipariş #{order.id} iptal edildi. Para iade edildi.")
        
        return True
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """ID'ye göre sipariş bul"""
        for order in self.__orders:
            if order.id == order_id:
                return order
        return None
    
    def get_pending_orders(self) -> List[Order]:
        """Bekleyen siparişleri getir"""
        return self.__pending_orders.copy()
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Duruma göre siparişleri filtrele"""
        return [order for order in self.__orders if order.status == status]
    
    def get_customer_orders(self, customer: Customer) -> List[Order]:
        """Müşterinin siparişlerini getir"""
        return [order for order in self.__orders if order.customer == customer]
    
    # İstatistikler ve raporlar
    def get_dashboard_statistics(self) -> Dict:
        """Dashboard istatistikleri"""
        today_orders = [o for o in self.__orders 
                       if o.status == OrderStatus.DELIVERED]
        
        return {
            "cafe_name": self.__cafe_name,
            "is_open": self.__is_open,
            "total_customers": len(self.__customers),
            "total_baristas": len(self.__baristas),
            "available_baristas": len(self.get_available_baristas()),
            "pending_orders": len(self.__pending_orders),
            "total_orders": len(self.__orders),
            "completed_today": len(today_orders),
            "daily_revenue": self.__daily_revenue,
            "total_revenue": self.__total_revenue,
            "menu_items": len(self.__menu)
        }
    
    def get_best_selling_drinks(self, limit: int = 5) -> List[Dict]:
        """En çok satan içecekler"""
        drink_sales = {}
        
        for order in self.__orders:
            if order.status == OrderStatus.DELIVERED:
                for drink, quantity in order.items:
                    key = drink.name
                    if key not in drink_sales:
                        drink_sales[key] = {"name": drink.name, "quantity": 0, "revenue": 0.0}
                    
                    drink_sales[key]["quantity"] += quantity
                    drink_sales[key]["revenue"] += drink.get_final_price() * quantity
        
        # Satış miktarına göre sırala
        sorted_drinks = sorted(drink_sales.values(), key=lambda x: x["quantity"], reverse=True)
        
        return sorted_drinks[:limit]
    
    def get_top_customers(self, limit: int = 5) -> List[Dict]:
        """En çok harcayan müşteriler"""
        customer_spending = {}
        
        for customer in self.__customers:
            total = sum(order.total_price for order in self.__orders 
                       if order.customer == customer and order.status == OrderStatus.DELIVERED)
            
            customer_spending[customer.name] = {
                "name": customer.name,
                "type": customer.__class__.__name__,
                "total_spent": total,
                "order_count": len([o for o in self.__orders if o.customer == customer]),
                "loyalty_points": customer.loyalty_points
            }
        
        sorted_customers = sorted(customer_spending.values(), 
                                 key=lambda x: x["total_spent"], reverse=True)
        
        return sorted_customers[:limit]
    
    def _print_daily_report(self):
        """Günlük rapor yazdır"""
        print("\n" + "="*60)
        print("📊 GÜNLÜK RAPOR 📊".center(60))
        print("="*60)
        
        stats = self.get_dashboard_statistics()
        
        print(f"\n💰 Gelir:")
        print(f"   Bugünkü Gelir: {self.__daily_revenue:.2f}₺")
        print(f"   Toplam Gelir: {self.__total_revenue:.2f}₺")
        
        print(f"\n📦 Siparişler:")
        print(f"   Tamamlanan: {stats['completed_today']}")
        print(f"   Bekleyen: {stats['pending_orders']}")
        print(f"   Toplam: {stats['total_orders']}")
        
        print(f"\n👥 Müşteriler:")
        print(f"   Toplam Müşteri: {stats['total_customers']}")
        
        print(f"\n👨‍🍳 Barista'lar:")
        print(f"   Toplam: {stats['total_baristas']}")
        
        # En çok satanlar
        best_selling = self.get_best_selling_drinks(3)
        if best_selling:
            print(f"\n🏆 En Çok Satanlar:")
            for i, drink in enumerate(best_selling, 1):
                print(f"   {i}. {drink['name']}: {drink['quantity']} adet ({drink['revenue']:.2f}₺)")
        
        print("\n" + "="*60 + "\n")
    
    # Veri kalıcılığı
    def _save_data(self):
        """Verileri JSON'a kaydet"""
        data = {
            "cafe_name": self.__cafe_name,
            "total_revenue": self.__total_revenue,
            "customers": [c.to_dict() for c in self.__customers],
            "baristas": [b.to_dict() for b in self.__baristas],
            "last_saved": datetime.now().isoformat()
        }
        
        try:
            with open("data/cafe_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("💾 Veriler kaydedildi!")
        except Exception as e:
            print(f"⚠️  Veri kaydetme hatası: {e}")
    
    def _load_data(self):
        """JSON'dan verileri yükle"""
        if not os.path.exists("data/cafe_data.json"):
            print("📝 İlk çalıştırma, varsayılan veriler yükleniyor...")
            self._initialize_default_data()
            return
        
        try:
            with open("data/cafe_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.__cafe_name = data.get("cafe_name", "Coffee Heaven")
            self.__total_revenue = data.get("total_revenue", 0.0)
            
            # Müşterileri yükle
            for customer_data in data.get("customers", []):
                customer_type = customer_data.get("type", "RegularCustomer")
                if customer_type == "PremiumCustomer":
                    customer = PremiumCustomer(
                        customer_data["name"],
                        customer_data["email"],
                        customer_data["phone"],
                        customer_data["balance"]
                    )
                elif customer_type == "VIPCustomer":
                    customer = VIPCustomer(
                        customer_data["name"],
                        customer_data["email"],
                        customer_data["phone"],
                        customer_data["balance"]
                    )
                else:
                    customer = RegularCustomer(
                        customer_data["name"],
                        customer_data["email"],
                        customer_data["phone"],
                        customer_data["balance"]
                    )
                
                self.__customers.append(customer)
            
            # Barista'ları yükle
            for barista_data in data.get("baristas", []):
                barista = Barista(
                    barista_data["name"],
                    barista_data["email"],
                    barista_data["experience_years"],
                    barista_data["hourly_rate"]
                )
                self.__baristas.append(barista)
            
            print("✅ Veriler yüklendi!")
            
        except Exception as e:
            print(f"⚠️  Veri yükleme hatası: {e}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Varsayılan verileri oluştur"""
        # Örnek barista'lar
        self.hire_barista("Ayşe Yılmaz", "ayse@cafe.com", 5, 60.0)
        self.hire_barista("Mehmet Demir", "mehmet@cafe.com", 3, 55.0)
        
        # Örnek müşteriler
        self.register_customer("Ali Veli", "ali@email.com", "5551234567", "Regular", 200.0)
        self.register_customer("Zeynep Kaya", "zeynep@email.com", "5559876543", "Premium", 500.0)
        self.register_customer("Can Öztürk", "can@email.com", "5556547890", "VIP", 1000.0)
    
    # Dunder methods
    def __str__(self) -> str:
        status = "🟢 AÇIK" if self.__is_open else "🔴 KAPALI"
        return f"{self.__cafe_name} - {status} - {len(self.__customers)} müşteri, {len(self.__baristas)} barista"
    
    def __repr__(self) -> str:
        return f"CafeManager(name='{self.__cafe_name}', open={self.__is_open})"