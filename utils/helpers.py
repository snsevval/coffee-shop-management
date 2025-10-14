from typing import Optional
import re

class InputValidator:
    """Kullanıcı girdilerini doğrulama sınıfı"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Email formatı kontrol et"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Telefon numarası kontrol et (Türkiye formatı)"""
        # 10 haneli numara veya başında 0 varsa 11 haneli
        phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if len(phone) == 10:
            return phone.isdigit()
        elif len(phone) == 11 and phone.startswith("0"):
            return phone.isdigit()
        
        return False
    
    @staticmethod
    def validate_positive_number(value: str) -> Optional[float]:
        """Pozitif sayı kontrol et"""
        try:
            num = float(value)
            if num > 0:
                return num
            return None
        except ValueError:
            return None
    
    @staticmethod
    def validate_integer(value: str, min_val: int = None, max_val: int = None) -> Optional[int]:
        """Integer kontrol et"""
        try:
            num = int(value)
            
            if min_val is not None and num < min_val:
                return None
            if max_val is not None and num > max_val:
                return None
            
            return num
        except ValueError:
            return None


class Formatter:
    """Çıktıları formatlama sınıfı"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Para formatı"""
        return f"{amount:.2f}₺"
    
    @staticmethod
    def format_header(text: str, width: int = 60, char: str = "=") -> str:
        """Başlık formatı"""
        return f"\n{char * width}\n{text.center(width)}\n{char * width}\n"
    
    @staticmethod
    def format_subheader(text: str, width: int = 60, char: str = "-") -> str:
        """Alt başlık formatı"""
        return f"\n{text}\n{char * width}"
    
    @staticmethod
    def format_box(text: str, width: int = 60) -> str:
        """Kutu içinde metin"""
        lines = text.split("\n")
        result = "┌" + "─" * (width - 2) + "┐\n"
        
        for line in lines:
            padding = width - len(line) - 4
            result += f"│ {line}{' ' * padding} │\n"
        
        result += "└" + "─" * (width - 2) + "┘"
        return result
    
    @staticmethod
    def print_success(message: str):
        """Başarı mesajı"""
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Hata mesajı"""
        print(f"❌ {message}")
    
    @staticmethod
    def print_warning(message: str):
        """Uyarı mesajı"""
        print(f"⚠️  {message}")
    
    @staticmethod
    def print_info(message: str):
        """Bilgi mesajı"""
        print(f"ℹ️  {message}")


class MenuHelper:
    """Menü işlemleri için yardımcı sınıf"""
    
    @staticmethod
    def get_user_choice(prompt: str, valid_choices: list) -> str:
        """Kullanıcıdan geçerli seçim al"""
        while True:
            choice = input(prompt).strip()
            
            if choice in [str(c) for c in valid_choices]:
                return choice
            
            Formatter.print_error(f"Geçersiz seçim! Lütfen {valid_choices} arasından seçin.")
    
    @staticmethod
    def get_user_input(prompt: str, validator=None, error_message: str = "Geçersiz giriş!") -> str:
        """Kullanıcıdan girdi al ve doğrula"""
        while True:
            user_input = input(prompt).strip()
            
            if not user_input:
                Formatter.print_error("Boş girilemez!")
                continue
            
            if validator is None:
                return user_input
            
            result = validator(user_input)
            if result is not None:
                return result if isinstance(result, str) else user_input
            
            Formatter.print_error(error_message)
    
    @staticmethod
    def confirm_action(message: str) -> bool:
        """Onay al"""
        choice = input(f"{message} (E/H): ").strip().upper()
        return choice == "E"
    
    @staticmethod
    def pause():
        """Devam etmek için bekle"""
        input("\nDevam etmek için Enter'a basın...")
    
    @staticmethod
    def clear_screen():
        """Ekranı temizle (cross-platform)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')


class TablePrinter:
    """Tablo yazdırma sınıfı"""
    
    @staticmethod
    def print_table(headers: list, rows: list, widths: list = None):
        """Tablo yazdır"""
        if widths is None:
            widths = [max(len(str(row[i])) for row in [headers] + rows) + 2 
                     for i in range(len(headers))]
        
        # Üst çizgi
        print("┌" + "┬".join("─" * w for w in widths) + "┐")
        
        # Başlık
        header_row = "│" + "│".join(f" {str(headers[i]):<{widths[i]-1}}" 
                                     for i in range(len(headers))) + "│"
        print(header_row)
        
        # Ayırıcı
        print("├" + "┼".join("─" * w for w in widths) + "┤")
        
        # Satırlar
        for row in rows:
            data_row = "│" + "│".join(f" {str(row[i]):<{widths[i]-1}}" 
                                       for i in range(len(row))) + "│"
            print(data_row)
        
        # Alt çizgi
        print("└" + "┴".join("─" * w for w in widths) + "┘")