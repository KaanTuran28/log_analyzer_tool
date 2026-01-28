# LOG ANALİZ VE SOC UYARI SİSTEMİ

Merhaba,
Bu projeyi, sunucu loglarında meydana gelen şüpheli durumları ve saldırı girişimlerini tespit etmek için geliştirdim. SOC (Güvenlik Operasyon Merkezi) süreçlerinde sürekli loglara bakmak zor olduğu için, bu işlem Python ile otomatik hale getirildi. Program hem eski log dosyalarını tarayıp rapor çıkartabiliyor hem de sunucuyu canlı olarak (real-time) takip edebiliyor.

---

## PROJE KLASÖRLERİ VE DOSYALAR
Proje şu şekilde bir dosya yapısına sahip:

- **src**: Programın ana kodları burada (analiz motoru, takip modülü vs).
- **config**: Kuralların olduğu dosya burada (rules.yaml). Saldırı imzalarını buradan değiştirebilirsiniz.
- **logs**: Test yapmak için log dosyalarını buraya koyuyoruz.
- **reports**: Analiz bitince oluşan Excel (CSV) raporları buraya kaydediliyor.
- **Dockerfile**: Projeyi sanal ortamda (container) çalıştırmak için gerekli dosya.

---

## KURULUM VE ÇALIŞTIRMA
Programı çalıştırmak için iki yöntem var. Python yüklü ise direkt çalıştırabilirsiniz veya Docker kullanabilirsiniz.

Yöntem 1: Python ile Çalıştırma (Manuel)
Bilgisayarınızda Python varsa aşağıdaki adımları yapmanız yeterli.

1. Önce gerekli kütüphaneyi yükleyin. (Sadece yaml dosyasını okumak için bir kütüphane kullandım, başka ağır bir şey yok).
- pip install -r requirements.txt

2. Sonra programı başlatın:
- python main.py

Yöntem 2: Docker ile Çalıştırma
Eğer kütüphane kurulumuyla uğraşmak istemezseniz projeyi Dockerize ettim.

1. İmajı oluşturun:
- docker-compose build

2. Programı başlatın:
-  docker-compose run --rm log-analyzer


---

## PROGRAM NASIL KULLANILIR?
Programı açtığınızda karşınıza 3 seçenekli bir menü gelir:

1. Dosya Analizi (Statik)
Bu seçenek, daha önceden kaydedilmiş bir log dosyasını baştan sona taramak içindir.
- Seçimi yaptıktan sonra sizden dosya yolunu ister (Örneğin: logs/auth.log).
- Dosyayı tarar ve ekrana bir özet çıkarır (Kaç tane hata var, kaç tane saldırı var vs).
- İşlem bitince "CSV olarak kaydedilsin mi?" diye sorar. Evet derseniz reports klasörüne detaylı bir rapor dosyası oluşturur.

2. Canlı Takip (Live Monitoring)
Bu seçenek Linux sistemlerdeki "tail -f" komutu gibi çalışır.
- Dosya yolunu girersiniz (Örneğin: logs/canli.log).
- Program o dosyayı sürekli dinlemeye başlar.
- Dosyaya yeni bir satır eklendiği an (mesela bir saldırı girişimi olduğunda) program bunu yakalar ve ekrana kırmızı renkli bir ALARM basar.
- Test etmek için program açıkken başka bir terminalden o dosyaya yazı yazdırabilirsiniz.

3. Çıkış
Programı kapatır.

---

## TESPİT EDİLEBİLEN SALDIRILAR
Config klasöründeki rules.yaml dosyasına şu kuralları tanımladım, bunları tespit edebiliyor:

- SSH Brute Force (Hatalı şifre denemeleri)
- Root Login (Root kullanıcısı ile giriş yapılması)
- SQL Injection (Veritabanı saldırıları)
- XSS (Zararlı script çalıştırma denemeleri)
- Yeni Kullanıcı Oluşturma (Sistemde şüpheli kullanıcı açılması)
- Sudo Yetkisi (Yetkili komut çalıştırılması)
- Kritik Sistem Hataları

---

## NOTLAR
- Programda Türkçe karakter sorunu olmaması için dosya okuma işlemlerinde utf-8 kullandım.
- Canlı takip modundayken programdan çıkmak için klavyeden CTRL ve C tuşlarına aynı anda basmanız yeterlidir.
