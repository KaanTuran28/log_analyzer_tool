import sys
import os
import time
from src.analyzer import LogAnalyzer
from src.monitor import LogMonitor
from src.reporter import csv_olustur

# Giriş Ekranı Tasarımı
BANNER = """
-------------------------------------------
    CLI LOG ANALİZ VE UYARI SİSTEMİ
-------------------------------------------
"""

# Yardımcı Fonksiyonlar
def temizle():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def menu_goster():
    print(BANNER)
    print("1. Dosya Analizi (Statik)")
    print("2. Canlı Takip (Live)")
    print("3. Çıkış")
    print("-" * 40)
    
    secim = input("Seçiminiz (1-3): ")
    return secim

# Rapor Özetleme İşlemleri
def ozet_bas(sonuclar):
    if not sonuclar:
        print("\nTemiz: Herhangi bir tehdit bulunamadı.")
        return

    print("\n--- ANALİZ ÖZETİ ---")
    
    # Kural Sayacı
    kural_sayilari = {}
    for kayit in sonuclar:
        isim = kayit['rule_name']
        if isim in kural_sayilari:
            kural_sayilari[isim] = kural_sayilari[isim] + 1
        else:
            kural_sayilari[isim] = 1
    
    print("\nKategori Dağılımı:")
    for k, v in kural_sayilari.items():
        print(" - " + k + " : " + str(v) + " adet")

    # Risk Sayacı
    risk_sayilari = {}
    for kayit in sonuclar:
        risk = kayit['severity']
        if risk in risk_sayilari:
            risk_sayilari[risk] = risk_sayilari[risk] + 1
        else:
            risk_sayilari[risk] = 1
    
    print("\nRisk Dağılımı:")
    for k, v in risk_sayilari.items():
        print(" - " + k + " : " + str(v) + " adet")
        
    print("--------------------")

# Dosya Analiz Fonksiyonu
def dosya_analizi():
    yol = input("\nDosya yolunu giriniz (Örn: logs/auth.log): ")
    
    if os.path.exists(yol):
        print("\nAnaliz başlıyor...")
        app = LogAnalyzer()
        
        t1 = time.time()
        data = app.analyze_file(yol)
        t2 = time.time()
        
        print("Analiz bitti. Süre: " + str(round(t2 - t1, 2)) + " sn")
        
        ozet_bas(data)
        
        if len(data) > 0:
            soru = input("\nCSV olarak kaydedilsin mi? (e/h): ")
            if soru.lower() == 'e':
                dosya = csv_olustur(data)
                if dosya:
                    print("Dosya konumu: " + str(dosya))
    else:
        print("Hata: Belirtilen dosya bulunamadı.")
    
    input("\nMenüye dönmek için Enter'a basın...")

# Canlı Takip Fonksiyonu
def canli_takip():
    yol = input("\nİzlenecek dosya yolu: ")
    
    if os.path.exists(yol):
        print("\nCanlı takip başladı...")
        print("Çıkmak için CTRL+C tuşlarına basın.")
        time.sleep(1)
        
        mon = LogMonitor()
        mon.follow(yol)
    else:
        print("Hata: Dosya yok.")

# Ana Program Döngüsü
if __name__ == "__main__":
    while True:
        temizle()
        secim = menu_goster()
        
        if secim == '1':
            dosya_analizi()
        elif secim == '2':
            canli_takip()
        elif secim == '3':
            sys.exit()
        else:
            input("Geçersiz seçim. Enter'a basın.")