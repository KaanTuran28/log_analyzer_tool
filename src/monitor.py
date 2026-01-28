import time
import os
from src.analyzer import LogAnalyzer

class LogMonitor:
    def __init__(self, config_path='config/rules.yaml'):
        # Analiz motorunu başlat
        self.analyzer = LogAnalyzer(config_path)

    def follow(self, dosya_yolu, log_tipi=None):
        
        # Dosya kontrolü
        if not os.path.exists(dosya_yolu):
            print("Hata: İzlenecek dosya bulunamadı: " + str(dosya_yolu))
            return

        print(str(dosya_yolu) + " dosyası izleniyor... (Durdurmak için CTRL+C)")
        
        try:
            # Dosyayı açıyoruz
            with open(dosya_yolu, 'r', encoding='utf-8', errors='ignore') as f:
                
                # İmleci en sona getir (Eski logları okuma)
                f.seek(0, 2)
                
                while True:
                    satir = f.readline()
                    
                    # Satır boşsa bekle
                    if not satir:
                        time.sleep(0.5)
                        continue
                    
                    # Yeni satır geldiyse analiz et
                    alarmlar = self.analyzer.analyze_line(satir, log_tipi)
                    
                    # Alarm varsa ekrana bas
                    for a in alarmlar:
                        self.ekrana_yaz(a)
                        
        except KeyboardInterrupt:
            print("\nTakip işlemi durduruldu.")
        except Exception as e:
            print("\nBir hata oluştu: " + str(e))

    def ekrana_yaz(self, veri):
        seviye = veri['severity']
        
        # Renk kodları (Manuel if-else yapısı ile)
        renk_kodu = "\033[0m" # Sıfırla
        
        if seviye == 'CRITICAL':
            renk_kodu = "\033[91m" # Kırmızı
        elif seviye == 'HIGH':
            renk_kodu = "\033[93m" # Sarı
        elif seviye == 'MEDIUM':
            renk_kodu = "\033[94m" # Mavi
        elif seviye == 'LOW':
            renk_kodu = "\033[92m" # Yeşil
            
        zaman = veri['timestamp']
        kural = veri['rule_name']
        log_icerigi = veri['log_line'].strip()
        reset = "\033[0m"
        
        # String birleştirme ile yazdırma
        print(renk_kodu + "[ALARM] " + zaman + " | " + seviye + " | " + kural + reset)
        print("      Log Detayı: " + log_icerigi)
        print("-" * 40)