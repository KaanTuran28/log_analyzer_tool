import re
import yaml
import os
from datetime import datetime

class LogAnalyzer:
    def __init__(self, ayar_dosyasi='config/rules.yaml'):
        # Kuralları yükle
        self.kurallar = []
        
        if os.path.exists(ayar_dosyasi):
            try:
                # Dosyayı oku
                f = open(ayar_dosyasi, 'r')
                data = yaml.safe_load(f)
                f.close()
                
                self.kurallar = data.get('rules', [])
                
                # Regex'leri derle (Daha hızlı çalışması için)
                for kural in self.kurallar:
                    pattern = kural['regex']
                    kural['desen'] = re.compile(pattern)
                    
            except Exception as e:
                print("Kurallar yüklenirken hata: " + str(e))
        else:
            print("Config dosyası bulunamadı!")

    def analyze_line(self, satir, filtre_turu=None):
        bulunanlar = []
        satir = satir.strip()
        
        # Boş satırsa geç
        if len(satir) == 0:
            return []

        for kural in self.kurallar:
            # Log türü filtresi varsa kontrol et
            if filtre_turu:
                if kural.get('log_type') != filtre_turu:
                    continue

            # Regex kontrolü
            if 'desen' in kural:
                eslesme = kural['desen'].search(satir)
                
                if eslesme:
                    # Alarm objesi oluştur
                    simdi = datetime.now()
                    zaman_damgasi = simdi.strftime("%Y-%m-%d %H:%M:%S")
                    
                    uyari = {}
                    uyari['timestamp'] = zaman_damgasi
                    uyari['rule_name'] = kural['name']
                    uyari['severity'] = kural['severity']
                    uyari['log_line'] = satir
                    uyari['description'] = kural['description']
                    
                    bulunanlar.append(uyari)
                    
        return bulunanlar

    def analyze_file(self, dosya_yolu, filtre_turu=None):
        sonuclar = []
        
        try:
            # Dosyayı aç (utf-8 hatası vermemesi için ignore eklendi)
            f = open(dosya_yolu, 'r', encoding='utf-8', errors='ignore')
            
            satir_sayisi = 0
            
            for satir in f:
                satir_sayisi = satir_sayisi + 1
                
                alarmlar = self.analyze_line(satir, filtre_turu)
                
                # Eğer alarm varsa listeye ekle
                for a in alarmlar:
                    a['line_number'] = satir_sayisi
                    sonuclar.append(a)
            
            f.close()
            
        except Exception as e:
            print("Dosya okunurken hata oluştu: " + str(e))
            
        return sonuclar