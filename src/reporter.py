import csv
import os
from datetime import datetime

# Raporlama İşlemleri Burada Yapılıyor
def csv_olustur(veriler):
    
    # Rapor klasörü ayarı
    rapor_klasoru = 'reports'
    
    # Klasör yoksa oluştur
    if not os.path.exists(rapor_klasoru):
        os.makedirs(rapor_klasoru)

    # Eğer veri yoksa işlem yapma
    if not veriler:
        print("Raporlanacak veri yok.")
        return None

    # Dosya ismini tarihle oluştur
    zaman = datetime.now()
    tarih_str = zaman.strftime('%Y%m%d_%H%M%S')
    
    dosya_ismi = "log_rapor_" + tarih_str + ".csv"
    
    # Tam dosya yolu
    tam_yol = os.path.join(rapor_klasoru, dosya_ismi)

    # CSV Başlıkları
    basliklar = ['timestamp', 'severity', 'rule_name', 'description', 'line_number', 'log_line']

    try:
        # utf-8-sig Excel'de Türkçe karakterlerin düzgün görünmesi için gerekli
        with open(tam_yol, mode='w', newline='', encoding='utf-8-sig') as f:
            
            yazici = csv.DictWriter(f, fieldnames=basliklar)
            yazici.writeheader()
            
            for satir in veriler:
                # Canlı takipte satır numarası olmuyor, kontrol edelim
                if 'line_number' not in satir:
                    satir['line_number'] = 'Canlı-Takip'
                    
                yazici.writerow(satir)
        
        # print("Rapor oluştu: " + tam_yol)
        return tam_yol
        
    except Exception as e:
        print("Hata oldu: " + str(e))
        return None