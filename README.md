# coffee-shop-management
#  Coffee Shop Management System

Nesne Yönelimli Programlama (OOP) prensipleriyle geliştirilmiş kapsamlı bir kahve dükkanı yönetim sistemi.

##  Proje Özellikleri

- **Müşteri Yönetimi**: Regular, Premium ve VIP müşteri tipleri
- **Sipariş Sistemi**: Sepet yönetimi, ödeme işlemleri
- **Barista Paneli**: Vardiya yönetimi, sipariş hazırlama
- **Menü Yönetimi**: Ürün ekleme/silme, kategori filtreleme
- **Raporlama**: Satış raporları, müşteri istatistikleri
- **Veri Kalıcılığı**: JSON ile veri kaydetme/yükleme

##  Kullanılan Teknolojiler

- **Python 3.x**
- Object-Oriented Programming (OOP)
- Design Patterns (Singleton, Facade, Composition)
- JSON (Veri kalıcılığı)

##  OOP Konseptleri

###  Encapsulation
- Private attributes (`__name`, `__balance`)
- Property decorators (`@property`, `@setter`)

###  Inheritance
- Customer → RegularCustomer, PremiumCustomer, VIPCustomer
- Abstract Base Class (ABC) kullanımı

###  Polymorphism
- Her müşteri tipi farklı `calculate_discount()` implementasyonu
- Method overriding

###  Abstraction
- Abstract methods (`@abstractmethod`)
- Interface benzeri yapılar

### Composition
- Order "has-a" Customer, Barista, Drinks
- CafeManager tüm sınıfları yönetir


