#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Coffee Shop Management System
OOP Proje - Kahve Dükkanı Yönetim Sistemi
"""

import sys
from managers.cafe_manager import CafeManager
from models.customer import RegularCustomer, PremiumCustomer, VIPCustomer
from models.order import Order, OrderStatus
from utils.helpers import InputValidator, Formatter, MenuHelper, TablePrinter

class CoffeeShopApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        self.manager = CafeManager("☕ COFFEE HEAVEN ☕")
        self.current_customer = None
        self.running = True
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.show_welcome()
        
        while self.running:
            try:
                self.show_main_menu()
            except KeyboardInterrupt:
                print("\n\nÇıkış yapılıyor...")
                self.exit_app()
            except Exception as e:
                Formatter.print_error(f"Bir hata oluştu: {e}")
                MenuHelper.pause()
    
    def show_welcome(self):
        """Hoş geldin ekranı"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("☕ COFFEE HEAVEN ☕", 70, "═"))
        print("Kahve Dükkanı Yönetim Sistemine Hoş Geldiniz!".center(70))
        print("="*70)
        MenuHelper.pause()
    
    def show_main_menu(self):
        """Ana menü"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("☕ ANA MENÜ ☕", 60))
        
        print("1️⃣  Kafeyi Aç/Kapat")
        print("2️⃣  Müşteri İşlemleri")
        print("3️⃣  Sipariş Ver (Müşteri Olarak)")
        print("4️⃣  Barista Paneli")
        print("5️⃣  Yönetici Paneli")
        print("6️⃣  Menüyü Görüntüle")
        print("7️⃣  Raporlar ve İstatistikler")
        print("0️⃣  Çıkış")
        
        print("\n" + "="*60)
        
        # Durum bilgisi
        stats = self.manager.get_dashboard_statistics()
        status = "🟢 AÇIK" if stats['is_open'] else "🔴 KAPALI"
        print(f"\nDurum: {status} | Bekleyen Sipariş: {stats['pending_orders']} | Günlük Gelir: {stats['daily_revenue']:.2f}₺")
        
        choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4, 5, 6, 7])
        
        if choice == "1":
            self.cafe_operations()
        elif choice == "2":
            self.customer_operations()
        elif choice == "3":
            self.customer_order_flow()
        elif choice == "4":
            self.barista_panel()
        elif choice == "5":
            self.admin_panel()
        elif choice == "6":
            self.show_menu()
        elif choice == "7":
            self.show_reports()
        elif choice == "0":
            self.exit_app()
    
    # ============ KAFE İŞLEMLERİ ============
    
    def cafe_operations(self):
        """Kafe aç/kapat"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🏪 KAFE İŞLEMLERİ", 60))
        
        if self.manager.is_open:
            print("Kafe şu anda AÇIK.\n")
            if MenuHelper.confirm_action("Kafeyi kapatmak istiyor musunuz?"):
                try:
                    self.manager.close_cafe()
                    Formatter.print_success("Kafe kapatıldı!")
                except Exception as e:
                    Formatter.print_error(str(e))
        else:
            print("Kafe şu anda KAPALI.\n")
            if MenuHelper.confirm_action("Kafeyi açmak istiyor musunuz?"):
                self.manager.open_cafe()
                Formatter.print_success("Kafe açıldı!")
        
        MenuHelper.pause()
    
    # ============ MÜŞTERİ İŞLEMLERİ ============
    
    def customer_operations(self):
        """Müşteri işlemleri menüsü"""
        while True:
            MenuHelper.clear_screen()
            print(Formatter.format_header("👥 MÜŞTERİ İŞLEMLERİ", 60))
            
            print("1. Yeni Müşteri Kaydet")
            print("2. Müşteri Listesi")
            print("3. Müşteri Ara")
            print("4. Müşteri Bakiye Ekle")
            print("5. Müşteri Sil")
            print("0. Geri Dön")
            
            choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4, 5])
            
            if choice == "1":
                self.register_customer()
            elif choice == "2":
                self.list_customers()
            elif choice == "3":
                self.search_customer()
            elif choice == "4":
                self.add_customer_balance()
            elif choice == "5":
                self.remove_customer()
            elif choice == "0":
                break
    
    def register_customer(self):
        """Yeni müşteri kaydet"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📝 YENİ MÜŞTERİ KAYDI", 60))
        
        name = MenuHelper.get_user_input("Ad Soyad: ")
        
        email = MenuHelper.get_user_input(
            "Email: ",
            InputValidator.validate_email,
            "Geçersiz email formatı!"
        )
        
        phone = MenuHelper.get_user_input(
            "Telefon (5551234567): ",
            InputValidator.validate_phone,
            "Geçersiz telefon numarası!"
        )
        
        print("\nMüşteri Tipi:")
        print("1. Regular (İndirim yok)")
        print("2. Premium (%10 indirim)")
        print("3. VIP (%20 indirim)")
        
        type_choice = MenuHelper.get_user_choice("Seçim: ", [1, 2, 3])
        customer_types = {
            "1": "Regular",
            "2": "Premium",
            "3": "VIP"
        }
        customer_type = customer_types[type_choice]
        
        initial_balance = float(MenuHelper.get_user_input(
            "Başlangıç Bakiyesi (₺): ",
            InputValidator.validate_positive_number,
            "Pozitif bir sayı girin!"
        ))
        
        try:
            customer = self.manager.register_customer(
                name, email, phone, customer_type, initial_balance
            )
            Formatter.print_success(f"{customer_type} müşteri kaydedildi!")
            print(f"\n{customer}")
        except Exception as e:
            Formatter.print_error(str(e))
        
        MenuHelper.pause()
    
    def list_customers(self):
        """Müşteri listesi"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("👥 MÜŞTERİ LİSTESİ", 60))
        
        customers = self.manager.get_all_customers()
        
        if not customers:
            Formatter.print_warning("Kayıtlı müşteri yok!")
        else:
            headers = ["ID", "Ad", "Tip", "Bakiye", "Puan"]
            rows = []
            
            for customer in customers:
                rows.append([
                    customer.id,
                    customer.name,
                    customer.__class__.__name__.replace("Customer", ""),
                    f"{customer.balance:.2f}₺",
                    customer.loyalty_points
                ])
            
            TablePrinter.print_table(headers, rows)
        
        MenuHelper.pause()
    
    def search_customer(self):
        """Müşteri ara"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🔍 MÜŞTERİ ARA", 60))
        
        email = input("Email: ").strip()
        customer = self.manager.get_customer_by_email(email)
        
        if customer:
            print(f"\n{customer}")
            print(f"Email: {customer.email}")
            print(f"Sipariş Geçmişi: {len(customer.order_history)} sipariş")
        else:
            Formatter.print_error("Müşteri bulunamadı!")
        
        MenuHelper.pause()
    
    def add_customer_balance(self):
        """Müşteri bakiye ekle"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("💰 BAKİYE EKLE", 60))
        
        email = input("Müşteri Email: ").strip()
        customer = self.manager.get_customer_by_email(email)
        
        if not customer:
            Formatter.print_error("Müşteri bulunamadı!")
            MenuHelper.pause()
            return
        
        amount = float(MenuHelper.get_user_input(
            "Eklenecek Miktar (₺): ",
            InputValidator.validate_positive_number,
            "Pozitif bir sayı girin!"
        ))
        
        new_balance = customer.add_balance(amount)
        Formatter.print_success(f"{amount:.2f}₺ eklendi. Yeni bakiye: {new_balance:.2f}₺")
        
        MenuHelper.pause()
    
    def remove_customer(self):
        """Müşteri sil"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🗑️  MÜŞTERİ SİL", 60))
        
        email = input("Müşteri Email: ").strip()
        customer = self.manager.get_customer_by_email(email)
        
        if not customer:
            Formatter.print_error("Müşteri bulunamadı!")
            MenuHelper.pause()
            return
        
        print(f"\nSilinecek Müşteri: {customer}")
        
        if MenuHelper.confirm_action("Silmek istediğinizden emin misiniz?"):
            if self.manager.remove_customer(email):
                Formatter.print_success("Müşteri silindi!")
            else:
                Formatter.print_error("Silme işlemi başarısız!")
        
        MenuHelper.pause()
    
    # ============ SİPARİŞ VERME (MÜŞTERİ) ============
    
    def customer_order_flow(self):
        """Müşteri olarak sipariş verme akışı"""
        if not self.manager.is_open:
            Formatter.print_error("Kafe kapalı!")
            MenuHelper.pause()
            return
        
        MenuHelper.clear_screen()
        print(Formatter.format_header("🛒 SİPARİŞ VER", 60))
        
        # Müşteri seç veya kaydet
        email = input("Email adresiniz: ").strip()
        customer = self.manager.get_customer_by_email(email)
        
        if not customer:
            print("\n❓ Kayıtlı müşteri bulunamadı.")
            if MenuHelper.confirm_action("Yeni müşteri kaydı oluşturmak ister misiniz?"):
                self.register_customer()
                customer = self.manager.get_customer_by_email(email)
                if not customer:
                    return
            else:
                return
        
        print(f"\n✅ Hoş geldiniz, {customer.name}!")
        print(f"Bakiyeniz: {customer.balance:.2f}₺")
        
        if hasattr(customer, 'discount_rate'):
            print(f"İndirim Oranınız: %{int(customer.discount_rate * 100)}")
        
        MenuHelper.pause()
        
        # Sipariş oluştur
        order = self.manager.create_order(customer)
        
        while True:
            MenuHelper.clear_screen()
            print(Formatter.format_header("🛒 SİPARİŞİNİZ", 60))
            
            # Mevcut sepeti göster
            if len(order) > 0:
                print("Sepetiniz:")
                print("-"*60)
                for drink, qty in order.items:
                    print(f"  {qty}x {drink.name} ({drink.size}) - {drink.get_final_price() * qty:.2f}₺")
                print("-"*60)
                print(f"Ara Toplam: {order.calculate_subtotal():.2f}₺")
                if order.calculate_discount() > 0:
                    print(f"İndirim: -{order.calculate_discount():.2f}₺")
                print(f"TOPLAM: {order.total_price:.2f}₺")
                print("="*60 + "\n")
            else:
                print("Sepetiniz boş.\n")
            
            print("1. Ürün Ekle")
            print("2. Ürün Çıkar")
            print("3. Siparişi Tamamla")
            print("4. Sepeti Temizle")
            print("0. İptal Et")
            
            choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4])
            
            if choice == "1":
                self.add_item_to_order(order)
            elif choice == "2":
                self.remove_item_from_order(order)
            elif choice == "3":
                if self.complete_order(order):
                    break
            elif choice == "4":
                order.clear_items()
                Formatter.print_success("Sepet temizlendi!")
                MenuHelper.pause()
            elif choice == "0":
                break
    
    def add_item_to_order(self, order):
        """Siparişe ürün ekle"""
        MenuHelper.clear_screen()
        self.manager.menu.display_menu_simple()
        
        try:
            drink_index = int(input("Ürün numarası (0 = İptal): ")) - 1
            
            if drink_index == -1:
                return
            
            drink = self.manager.menu[drink_index]
            
            quantity = int(MenuHelper.get_user_input(
                "Adet: ",
                lambda x: InputValidator.validate_integer(x, 1, 10),
                "1-10 arasında bir sayı girin!"
            ))
            
            order.add_item(drink, quantity)
            Formatter.print_success(f"{quantity}x {drink.name} eklendi!")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        
        MenuHelper.pause()
    
    def remove_item_from_order(self, order):
        """Siparişten ürün çıkar"""
        if len(order) == 0:
            Formatter.print_warning("Sepet zaten boş!")
            MenuHelper.pause()
            return
        
        MenuHelper.clear_screen()
        print(Formatter.format_header("🗑️  ÜRÜN ÇIKAR", 60))
        
        print("Sepetinizdeki ürünler:")
        for i, (drink, qty) in enumerate(order.items, 1):
            print(f"{i}. {drink.name} ({drink.size}) - {qty} adet")
        
        try:
            item_index = int(input("\nÇıkarılacak ürün numarası (0 = İptal): ")) - 1
            
            if item_index == -1:
                return
            
            drink_to_remove = order.items[item_index][0]
            order.remove_item(drink_to_remove)
            Formatter.print_success("Ürün çıkarıldı!")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        
        MenuHelper.pause()
    
    def complete_order(self, order):
        """Siparişi tamamla"""
        if len(order) == 0:
            Formatter.print_error("Sepet boş!")
            MenuHelper.pause()
            return False
        
        MenuHelper.clear_screen()
        print(order.get_detailed_info())
        
        if order.customer.balance < order.total_price:
            Formatter.print_error(f"Yetersiz bakiye! Bakiyeniz: {order.customer.balance:.2f}₺")
            MenuHelper.pause()
            return False
        
        if MenuHelper.confirm_action("Siparişi onaylıyor musunuz?"):
            try:
                self.manager.submit_order(order)
                Formatter.print_success("Sipariş başarıyla alındı!")
                print(f"\nKalan bakiyeniz: {order.customer.balance:.2f}₺")
                
                # Otomatik atama dene
                self.manager.auto_assign_orders()
                
                MenuHelper.pause()
                return True
            except Exception as e:
                Formatter.print_error(str(e))
                MenuHelper.pause()
                return False
        
        return False
    
    # ============ BARISTA PANELİ ============
    
    def barista_panel(self):
        """Barista paneli"""
        while True:
            MenuHelper.clear_screen()
            print(Formatter.format_header("👨‍🍳 BARISTA PANELİ", 60))
            
            print("1. Vardiya Başlat/Bitir")
            print("2. Bekleyen Siparişler")
            print("3. Sipariş Al ve Hazırla")
            print("4. Siparişi Tamamla")
            print("5. Barista Listesi")
            print("6. Barista İstatistikleri")
            print("0. Geri Dön")
            
            choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4, 5, 6])
            
            if choice == "1":
                self.barista_shift_operations()
            elif choice == "2":
                self.show_pending_orders()
            elif choice == "3":
                self.barista_take_order()
            elif choice == "4":
                self.barista_complete_order()
            elif choice == "5":
                self.list_baristas()
            elif choice == "6":
                self.barista_statistics()
            elif choice == "0":
                break
    
    def barista_shift_operations(self):
        """Vardiya başlat/bitir"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("⏰ VARDİYA İŞLEMLERİ", 60))
        
        # Barista listesi
        baristas = self.manager.get_all_baristas()
        
        if not baristas:
            Formatter.print_error("Kayıtlı barista yok!")
            MenuHelper.pause()
            return
        
        print("Barista'lar:")
        for i, barista in enumerate(baristas, 1):
            status = "🟢 Vardiyada" if barista.is_on_duty else "⚫ Vardiya Dışı"
            print(f"{i}. {barista.name} - {status}")
        
        try:
            barista_index = int(input("\nBarista numarası: ")) - 1
            barista = baristas[barista_index]
            
            if barista.is_on_duty:
                if MenuHelper.confirm_action(f"{barista.name} vardiyasını bitirsin mi?"):
                    try:
                        earnings = barista.end_shift()
                        Formatter.print_success(f"Vardiya bitti! Kazanç: {earnings:.2f}₺")
                    except Exception as e:
                        Formatter.print_error(str(e))
            else:
                if MenuHelper.confirm_action(f"{barista.name} vardiyaya başlasın mı?"):
                    barista.start_shift()
                    Formatter.print_success("Vardiya başladı!")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        
        MenuHelper.pause()
    
    def show_pending_orders(self):
        """Bekleyen siparişleri göster"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📦 BEKLEYEN SİPARİŞLER", 60))
        
        pending = self.manager.get_pending_orders()
        
        if not pending:
            Formatter.print_success("Bekleyen sipariş yok! ✨")
        else:
            for order in pending:
                print(order)
                print("-"*60)
        
        MenuHelper.pause()
    
    def barista_take_order(self):
        """Barista sipariş al"""
        if not self.manager.get_pending_orders():
            Formatter.print_warning("Bekleyen sipariş yok!")
            MenuHelper.pause()
            return
        
        MenuHelper.clear_screen()
        print(Formatter.format_header("📥 SİPARİŞ AL", 60))
        
        # Müsait barista'lar
        available = self.manager.get_available_baristas()
        
        if not available:
            Formatter.print_error("Müsait barista yok!")
            MenuHelper.pause()
            return
        
        print("Müsait Barista'lar:")
        for i, barista in enumerate(available, 1):
            print(f"{i}. {barista.name}")
        
        try:
            barista_index = int(input("\nBarista numarası: ")) - 1
            barista = available[barista_index]
            
            # Bekleyen siparişler
            pending = self.manager.get_pending_orders()
            print(f"\nBekleyen Siparişler:")
            for i, order in enumerate(pending, 1):
                print(f"{i}. Sipariş #{order.id} - {order.customer.name} - {order.total_price:.2f}₺")
            
            order_index = int(input("\nSipariş numarası: ")) - 1
            order = pending[order_index]
            
            self.manager.assign_order_to_barista(order, barista)
            Formatter.print_success("Sipariş atandı!")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        
        MenuHelper.pause()
    
    def barista_complete_order(self):
        """Barista siparişi tamamla"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("✅ SİPARİŞ TAMAMLA", 60))
        
        # Hazırlanan siparişler
        preparing = self.manager.get_orders_by_status(OrderStatus.PREPARING)
        
        if not preparing:
            Formatter.print_warning("Hazırlanan sipariş yok!")
            MenuHelper.pause()
            return
        
        print("Hazırlanan Siparişler:")
        for i, order in enumerate(preparing, 1):
            print(f"{i}. Sipariş #{order.id} - {order.customer.name} - Barista: {order.barista.name}")
        
        try:
            order_index = int(input("\nTamamlanacak sipariş numarası: ")) - 1
            order = preparing[order_index]
            
            print(order.get_detailed_info())
            
            if MenuHelper.confirm_action("Siparişi tamamla?"):
                self.manager.complete_order(order.id)
                Formatter.print_success("Sipariş tamamlandı ve teslim edildi!")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        except Exception as e:
            Formatter.print_error(str(e))
        
        MenuHelper.pause()
    
    def list_baristas(self):
        """Barista listesi"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("👨‍🍳 BARISTA LİSTESİ", 60))
        
        baristas = self.manager.get_all_baristas()
        
        if not baristas:
            Formatter.print_warning("Kayıtlı barista yok!")
        else:
            headers = ["ID", "Ad", "Tecrübe", "Durum", "Sipariş"]
            rows = []
            
            for barista in baristas:
                status = "🟢 Vardiyada" if barista.is_on_duty else "⚫ Vardiya Dışı"
                rows.append([
                    barista.id,
                    barista.name,
                    f"{barista.experience_years} yıl",
                    status,
                    barista.total_orders_completed
                ])
            
            TablePrinter.print_table(headers, rows)
        
        MenuHelper.pause()
    
    def barista_statistics(self):
        """Barista istatistikleri"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📊 BARISTA İSTATİSTİKLERİ", 60))
        
        baristas = self.manager.get_all_baristas()
        
        if not baristas:
            Formatter.print_warning("Kayıtlı barista yok!")
            MenuHelper.pause()
            return
        
        for i, barista in enumerate(baristas, 1):
            print(f"{i}. {barista.name}")
        
        try:
            barista_index = int(input("\nBarista numarası: ")) - 1
            barista = baristas[barista_index]
            
            MenuHelper.clear_screen()
            print(Formatter.format_header(f"📊 {barista.name.upper()} İSTATİSTİKLERİ", 60))
            
            stats = barista.get_statistics()
            
            print(f"Toplam Sipariş: {stats['total_orders']}")
            print(f"Toplam Kazanç: {stats['total_earnings']:.2f}₺")
            print(f"Verimlilik: {stats['efficiency']:.2f} sipariş/saat")
            print(f"Performans Puanı: {stats['performance_rating']:.1f}/5.0")
            print(f"Tecrübe: {stats['experience_years']} yıl")
            print(f"Durum: {stats['current_status']}")
            print(f"Müsaitlik: {stats['availability']}")
            
            monthly_salary = barista.calculate_monthly_salary()
            print(f"\nTahmini Aylık Maaş: {monthly_salary:.2f}₺")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        
        MenuHelper.pause()
    
    # ============ YÖNETİCİ PANELİ ============
    
    def admin_panel(self):
        """Yönetici paneli"""
        while True:
            MenuHelper.clear_screen()
            print(Formatter.format_header("🔧 YÖNETİCİ PANELİ", 60))
            
            print("1. Menü Yönetimi")
            print("2. Barista İşe Al/Çıkar")
            print("3. Tüm Siparişler")
            print("4. Sipariş İptal Et")
            print("5. Dashboard")
            print("0. Geri Dön")
            
            choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4, 5])
            
            if choice == "1":
                self.menu_management()
            elif choice == "2":
                self.barista_management()
            elif choice == "3":
                self.show_all_orders()
            elif choice == "4":
                self.cancel_order_admin()
            elif choice == "5":
                self.show_dashboard()
            elif choice == "0":
                break
    
    def menu_management(self):
        """Menü yönetimi"""
        while True:
            MenuHelper.clear_screen()
            print(Formatter.format_header("📋 MENÜ YÖNETİMİ", 60))
            
            print("1. Menüyü Görüntüle")
            print("2. Ürün Ekle")
            print("3. Ürün Sil")
            print("4. Menü İstatistikleri")
            print("0. Geri Dön")
            
            choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4])
            
            if choice == "1":
                self.show_menu()
            elif choice == "2":
                self.add_menu_item()
            elif choice == "3":
                self.remove_menu_item()
            elif choice == "4":
                self.menu_statistics()
            elif choice == "0":
                break
    
    def add_menu_item(self):
        """Menüye ürün ekle"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("➕ ÜRÜN EKLE", 60))
        
        name = MenuHelper.get_user_input("Ürün Adı: ")
        
        price = float(MenuHelper.get_user_input(
            "Fiyat (₺): ",
            InputValidator.validate_positive_number,
            "Pozitif bir sayı girin!"
        ))
        
        print("\nKategori:")
        print("1. Hot")
        print("2. Cold")
        print("3. Dessert")
        print("4. Food")
        
        cat_choice = MenuHelper.get_user_choice("Seçim: ", [1, 2, 3, 4])
        categories = {"1": "Hot", "2": "Cold", "3": "Dessert", "4": "Food"}
        category = categories[cat_choice]
        
        print("\nMalzemeler (virgülle ayırın):")
        ingredients_str = input("> ")
        ingredients = [ing.strip() for ing in ingredients_str.split(",")]
        
        print("\nBoyut:")
        print("1. Small")
        print("2. Medium")
        print("3. Large")
        
        size_choice = MenuHelper.get_user_choice("Seçim: ", [1, 2, 3])
        sizes = {"1": "Small", "2": "Medium", "3": "Large"}
        size = sizes[size_choice]
        
        try:
            from models.drink import Drink
            drink = Drink(name, price, category, ingredients, size)
            self.manager.menu.add_drink(drink)
            Formatter.print_success("Ürün eklendi!")
        except Exception as e:
            Formatter.print_error(str(e))
        
        MenuHelper.pause()
    
    def remove_menu_item(self):
        """Menüden ürün sil"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🗑️  ÜRÜN SİL", 60))
        
        self.manager.menu.display_menu_simple()
        
        try:
            drink_id = int(input("Silinecek ürün ID'si (0 = İptal): "))
            
            if drink_id == 0:
                return
            
            drink = self.manager.menu.get_drink_by_id(drink_id)
            
            if not drink:
                Formatter.print_error("Ürün bulunamadı!")
                MenuHelper.pause()
                return
            
            print(f"\nSilinecek: {drink}")
            
            if MenuHelper.confirm_action("Silmek istediğinizden emin misiniz?"):
                self.manager.menu.remove_drink_by_id(drink_id)
                Formatter.print_success("Ürün silindi!")
            
        except ValueError:
            Formatter.print_error("Geçersiz ID!")
        
        MenuHelper.pause()
    
    def menu_statistics(self):
        """Menü istatistikleri"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📊 MENÜ İSTATİSTİKLERİ", 60))
        
        stats = self.manager.menu.get_menu_statistics()
        
        print(f"Toplam Ürün: {stats['total_items']}")
        print(f"Kategoriler: {', '.join(stats['categories'])}")
        print(f"Ortalama Fiyat: {stats['avg_price']:.2f}₺")
        print(f"En Düşük Fiyat: {stats['min_price']:.2f}₺")
        print(f"En Yüksek Fiyat: {stats['max_price']:.2f}₺")
        
        print("\nKategori Dağılımı:")
        for category, count in stats['items_per_category'].items():
            print(f"  {category}: {count} ürün")
        
        most_expensive = self.manager.menu.get_most_expensive_drink()
        cheapest = self.manager.menu.get_cheapest_drink()
        
        if most_expensive:
            print(f"\nEn Pahalı: {most_expensive}")
        if cheapest:
            print(f"En Ucuz: {cheapest}")
        
        MenuHelper.pause()
    
    def barista_management(self):
        """Barista yönetimi"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("👨‍🍳 BARISTA YÖNETİMİ", 60))
        
        print("1. Barista İşe Al")
        print("2. Barista İşten Çıkar")
        print("0. Geri Dön")
        
        choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2])
        
        if choice == "1":
            self.hire_barista()
        elif choice == "2":
            self.fire_barista()
    
    def hire_barista(self):
        """Barista işe al"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("➕ BARISTA İŞE AL", 60))
        
        name = MenuHelper.get_user_input("Ad Soyad: ")
        
        email = MenuHelper.get_user_input(
            "Email: ",
            InputValidator.validate_email,
            "Geçersiz email formatı!"
        )
        
        experience = int(MenuHelper.get_user_input(
            "Tecrübe (yıl): ",
            lambda x: InputValidator.validate_integer(x, 0, 50),
            "0-50 arasında bir sayı girin!"
        ))
        
        hourly_rate = float(MenuHelper.get_user_input(
            "Saatlik Ücret (₺): ",
            InputValidator.validate_positive_number,
            "Pozitif bir sayı girin!"
        ))
        
        try:
            barista = self.manager.hire_barista(name, email, experience, hourly_rate)
            Formatter.print_success(f"Barista işe alındı: {barista.name}")
        except Exception as e:
            Formatter.print_error(str(e))
        
        MenuHelper.pause()
    
    def fire_barista(self):
        """Barista işten çıkar"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🗑️  BARISTA İŞTEN ÇIKAR", 60))
        
        baristas = self.manager.get_all_baristas()
        
        if not baristas:
            Formatter.print_error("Kayıtlı barista yok!")
            MenuHelper.pause()
            return
        
        print("Barista'lar:")
        for i, barista in enumerate(baristas, 1):
            print(f"{i}. {barista.name} - {barista.email}")
        
        try:
            barista_index = int(input("\nİşten çıkarılacak barista numarası (0 = İptal): ")) - 1
            
            if barista_index == -1:
                return
            
            barista = baristas[barista_index]
            
            print(f"\nİşten çıkarılacak: {barista.name}")
            
            if MenuHelper.confirm_action("İşten çıkarmak istediğinizden emin misiniz?"):
                if self.manager.fire_barista(barista.email):
                    Formatter.print_success("Barista işten çıkarıldı!")
                else:
                    Formatter.print_error("İşlem başarısız!")
            
        except (IndexError, ValueError):
            Formatter.print_error("Geçersiz seçim!")
        except Exception as e:
            Formatter.print_error(str(e))
        
        MenuHelper.pause()
    
    def show_all_orders(self):
        """Tüm siparişleri göster"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📦 TÜM SİPARİŞLER", 60))
        
        print("1. Tüm Siparişler")
        print("2. Bekleyen Siparişler")
        print("3. Hazırlanan Siparişler")
        print("4. Hazır Siparişler")
        print("5. Teslim Edilen Siparişler")
        print("6. İptal Edilen Siparişler")
        print("0. Geri Dön")
        
        choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4, 5, 6])
        
        if choice == "0":
            return
        
        MenuHelper.clear_screen()
        
        if choice == "1":
            orders = self.manager._CafeManager__orders  # Access private attribute
            title = "TÜM SİPARİŞLER"
        elif choice == "2":
            orders = self.manager.get_orders_by_status(OrderStatus.PENDING)
            title = "BEKLEYEN SİPARİŞLER"
        elif choice == "3":
            orders = self.manager.get_orders_by_status(OrderStatus.PREPARING)
            title = "HAZIRLANAN SİPARİŞLER"
        elif choice == "4":
            orders = self.manager.get_orders_by_status(OrderStatus.READY)
            title = "HAZIR SİPARİŞLER"
        elif choice == "5":
            orders = self.manager.get_orders_by_status(OrderStatus.DELIVERED)
            title = "TESLİM EDİLEN SİPARİŞLER"
        elif choice == "6":
            orders = self.manager.get_orders_by_status(OrderStatus.CANCELLED)
            title = "İPTAL EDİLEN SİPARİŞLER"
        
        print(Formatter.format_header(f"📦 {title}", 60))
        
        if not orders:
            Formatter.print_warning("Sipariş yok!")
        else:
            for order in orders:
                print(order)
                print("-"*60)
        
        MenuHelper.pause()
    
    def cancel_order_admin(self):
        """Sipariş iptal et (admin)"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🗑️  SİPARİŞ İPTAL ET", 60))
        
        order_id = int(MenuHelper.get_user_input(
            "Sipariş ID: ",
            lambda x: InputValidator.validate_integer(x, 1),
            "Geçerli bir ID girin!"
        ))
        
        try:
            self.manager.cancel_order(order_id)
            Formatter.print_success("Sipariş iptal edildi!")
        except Exception as e:
            Formatter.print_error(str(e))
        
        MenuHelper.pause()
    
    def show_dashboard(self):
        """Dashboard göster"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📊 DASHBOARD", 60))
        
        stats = self.manager.get_dashboard_statistics()
        
        print(f"☕ Kafe: {stats['cafe_name']}")
        print(f"Durum: {'🟢 AÇIK' if stats['is_open'] else '🔴 KAPALI'}")
        print("\n" + "="*60 + "\n")
        
        print("👥 Müşteriler:")
        print(f"   Toplam: {stats['total_customers']}")
        
        print("\n👨‍🍳 Barista'lar:")
        print(f"   Toplam: {stats['total_baristas']}")
        print(f"   Müsait: {stats['available_baristas']}")
        
        print("\n📦 Siparişler:")
        print(f"   Bekleyen: {stats['pending_orders']}")
        print(f"   Toplam: {stats['total_orders']}")
        print(f"   Bugün Tamamlanan: {stats['completed_today']}")
        
        print("\n💰 Gelir:")
        print(f"   Günlük: {stats['daily_revenue']:.2f}₺")
        print(f"   Toplam: {stats['total_revenue']:.2f}₺")
        
        print("\n📋 Menü:")
        print(f"   Ürün Sayısı: {stats['menu_items']}")
        
        MenuHelper.pause()
    
    # ============ MENÜ ve RAPORLAR ============
    
    def show_menu(self):
        """Menüyü göster"""
        MenuHelper.clear_screen()
        self.manager.menu.display_menu()
        MenuHelper.pause()
    
    def show_reports(self):
        """Raporlar"""
        while True:
            MenuHelper.clear_screen()
            print(Formatter.format_header("📊 RAPORLAR VE İSTATİSTİKLER", 60))
            
            print("1. En Çok Satan Ürünler")
            print("2. En Çok Harcayan Müşteriler")
            print("3. Barista Performans Raporu")
            print("4. Dashboard")
            print("0. Geri Dön")
            
            choice = MenuHelper.get_user_choice("\nSeçiminiz: ", [0, 1, 2, 3, 4])
            
            if choice == "1":
                self.best_selling_report()
            elif choice == "2":
                self.top_customers_report()
            elif choice == "3":
                self.barista_performance_report()
            elif choice == "4":
                self.show_dashboard()
            elif choice == "0":
                break
    
    def best_selling_report(self):
        """En çok satan ürünler raporu"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("🏆 EN ÇOK SATAN ÜRÜNLER", 60))
        
        best_selling = self.manager.get_best_selling_drinks(10)
        
        if not best_selling:
            Formatter.print_warning("Henüz satış yok!")
        else:
            headers = ["Sıra", "Ürün", "Satış", "Gelir"]
            rows = []
            
            for i, drink in enumerate(best_selling, 1):
                rows.append([
                    i,
                    drink['name'],
                    f"{drink['quantity']} adet",
                    f"{drink['revenue']:.2f}₺"
                ])
            
            TablePrinter.print_table(headers, rows)
        
        MenuHelper.pause()
    
    def top_customers_report(self):
        """En çok harcayan müşteriler raporu"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("👑 EN ÇOK HARCAYAN MÜŞTERİLER", 60))
        
        top_customers = self.manager.get_top_customers(10)
        
        if not top_customers:
            Formatter.print_warning("Henüz müşteri yok!")
        else:
            headers = ["Sıra", "Müşteri", "Tip", "Harcama", "Sipariş", "Puan"]
            rows = []
            
            for i, customer in enumerate(top_customers, 1):
                rows.append([
                    i,
                    customer['name'],
                    customer['type'].replace("Customer", ""),
                    f"{customer['total_spent']:.2f}₺",
                    customer['order_count'],
                    customer['loyalty_points']
                ])
            
            TablePrinter.print_table(headers, rows)
        
        MenuHelper.pause()
    
    def barista_performance_report(self):
        """Barista performans raporu"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("📊 BARISTA PERFORMANS RAPORU", 60))
        
        baristas = self.manager.get_all_baristas()
        
        if not baristas:
            Formatter.print_warning("Kayıtlı barista yok!")
        else:
            # Performansa göre sırala
            sorted_baristas = sorted(baristas, key=lambda b: b.total_orders_completed, reverse=True)
            
            headers = ["Sıra", "Ad", "Sipariş", "Verimlilik", "Puan"]
            rows = []
            
            for i, barista in enumerate(sorted_baristas, 1):
                stats = barista.get_statistics()
                rows.append([
                    i,
                    barista.name,
                    stats['total_orders'],
                    f"{stats['efficiency']:.2f} /saat",
                    f"{stats['performance_rating']:.1f}/5.0"
                ])
            
            TablePrinter.print_table(headers, rows)
        
        MenuHelper.pause()
    
    # ============ ÇIKIŞ ============
    
    def exit_app(self):
        """Uygulamadan çık"""
        MenuHelper.clear_screen()
        print(Formatter.format_header("👋 GÜLE GÜLE!", 60))
        
        if self.manager.is_open:
            print("⚠️  Kafe hala açık!")
            if MenuHelper.confirm_action("Kafeyi kapatıp çıkmak istiyor musunuz?"):
                try:
                    self.manager.close_cafe()
                except:
                    pass
        
        print("\n☕ Coffee Heaven'ı kullandığınız için teşekkürler!")
        print("Tekrar görüşmek üzere!\n")
        
        self.running = False
        sys.exit(0)


# ============ PROGRAM BAŞLANGICI ============

if __name__ == "__main__":
    app = CoffeeShopApp()
    app.run()