import csv

def backtest(data_file, starting_balance, operations):
    # Tarih ve fiyat bilgilerini saklayacak sözlük
    price_data = {}
    
    # Data dosyasından tarih ve fiyat bilgilerini al
    with open(data_file, 'r') as file: #okuma operatörü ile veri dosyasını okur
        reader = csv.reader(file)
        next(reader)  # Başlık satırını atla
        for row in reader: #Data dosyasında bulunan tarih ve fiyat verisini ayıran döngü
            date, price = row
            price_data[date] = float(price) #ayrılan tarihi price_data adlı değişkene atar diğer ayrılan float değeride price adlı değişkene atar böylelikle tarih ve fiyat tanımlanmış olur
    
    balance = starting_balance  # Bakiyeyi başlangıç bakiyesine eşitler
    
    for operation in operations:
        start_date, end_date, leverage, position = operation #yapılan işlemler adlı demetten sırası ile verileri alıp değişkenleri tanımlayan döngü
        
        # Başlangıç ve bitiş tarihleri arasındaki fiyatları kullanarak işlem yap
        for date in price_data: #Price_data adlı sözlük içinde tarihleri alan döngü
            if start_date <= date <= end_date: #başlangıç tarihi ve bitiş tarihi arasındaki tarihleri alıyor.
                
                price = price_data[date] # İşlem yapılacak günün fiyatını al
                
               
                previous_date = next((d for d in price_data if d < date), None) # Önceki günün fiyatını al (işlem yapılacak gün öncesi)
                if previous_date:
                    previous_price = price_data[previous_date] #önceki günün fiyatını alır
                else:
                    previous_price = price  # İlk gün için fiyat bilgisi olmadığından önceki günün fiyatı aynı alınır
                
                # Lot sayısını hesapla (başlangıç bakiyesi / önceki günün fiyatı)
                lot_size = balance / previous_price #bakiye bölü önceki günün fiyatı lotun değerini gösterir
                
                # Kâr veya zarar hesapla
                if position == "Long":
                    profit = (price - previous_price) * lot_size * leverage #long pozisyon olması halinde çalışıcak fonksiyon
                elif position == "Short":
                    profit = (previous_price - price) * lot_size * leverage #short pozisyon olması halinde çalışacak fonksiyon
                
                
                balance += profit #Bakiyeye kar veya zararı ekler
                
                print(f"Tarih: {date}, Pozisyon: {position}, Kar ve Zarar: {profit}, Yeni bakiye: {balance}") #terminale günlük kar, zarar, bakiye ve tarih bilgisini yazdırır.


data_file = r"C:\Users\ByGho\OneDrive\Masaüstü\data.csv" # Veri dosyasının olduğu uzantı

# Başlangıç bakiyesi
starting_balance = 1000

# Yapılan işlemler
operations = [
    ("2020-01-02", "2020-02-01", 3, "Long"),
    ("2020-02-01", "2020-03-01", 5, "Short"),
    ("2020-03-01", "2020-04-01", 7, "Long"),
    ("2020-04-01", "2020-06-01", 10, "Short"),
    ("2020-06-01", "2020-08-01", 3, "Long"),
    ("2020-08-01", "2020-10-01", 5, "Short"),
    ("2020-10-01", "2020-12-01", 7, "Long"),
    ("2020-12-01", "2020-12-31", 10, "Short")
]

# Backtest fonksiyonunu çağır
backtest(data_file, starting_balance, operations)
