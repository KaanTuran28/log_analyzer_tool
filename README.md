# Log Analysis & SOC Alert System

![Python](https://img.shields.io/badge/python-3.x-blue)
![Docker](https://img.shields.io/badge/Docker-2496ED)
![License](https://img.shields.io/badge/license-MIT-green)

<p align="center"><b><a href="#english">English</a></b> · <b><a href="#türkçe">Türkçe</a></b></p>

---

## English

A Python tool for detecting suspicious activity and attack attempts in server logs. Constantly watching logs by hand is hard in SOC (Security Operations Center) work, so this automates it: it can scan old log files and produce a report, or follow a server's logs live in real time.

### Project layout

- **src** — the main code (analysis engine, live-monitoring module, etc.).
- **config** — the rules file (`rules.yaml`). Edit attack signatures here.
- **logs** — put log files here for testing.
- **reports** — CSV reports are written here after analysis.
- **Dockerfile** — to run the project in a container.

### Setup and running

**Option 1 — Python (manual):**

```bash
pip install -r requirements.txt   # only a YAML-reading library, nothing heavy
python main.py
```

**Option 2 — Docker:**

```bash
docker-compose build
docker-compose run --rm log-analyzer
```

### How to use

When the program starts it shows a three-option menu:

1. **File analysis (static):** scans a saved log file from start to end. It asks for the file path (e.g. `logs/auth.log`), prints a summary (how many errors, how many attacks) and then offers to save a detailed CSV report into `reports/`.
2. **Live monitoring:** works like Linux `tail -f`. You give it a file path (e.g. `logs/live.log`) and it keeps listening; the moment a new line is added (e.g. an attack attempt) it catches it and prints a red ALARM. To test, append lines to that file from another terminal while it runs.
3. **Exit.**

### Detected attacks

The rules defined in `config/rules.yaml`:

- SSH brute force (failed password attempts)
- Root login
- SQL injection
- XSS (malicious script attempts)
- New user creation (suspicious account creation)
- Sudo privilege (privileged command execution)
- Critical system errors

### Notes

- File reads use UTF-8 to avoid Turkish-character issues.
- In live-monitoring mode, press `Ctrl` + `C` to quit.

### License

MIT — see [LICENSE](./LICENSE).

---

## Türkçe

Sunucu loglarında meydana gelen şüpheli durumları ve saldırı girişimlerini tespit etmek için geliştirilmiş bir Python aracı. SOC (Güvenlik Operasyon Merkezi) süreçlerinde sürekli loglara bakmak zor olduğu için bu işlem otomatikleştirildi: program hem eski log dosyalarını tarayıp rapor çıkarabiliyor hem de sunucuyu canlı (real-time) takip edebiliyor.

### Proje klasörleri

- **src** — programın ana kodları (analiz motoru, canlı takip modülü vb.).
- **config** — kuralların olduğu dosya (`rules.yaml`). Saldırı imzalarını buradan değiştirebilirsiniz.
- **logs** — test için log dosyalarını buraya koyuyoruz.
- **reports** — analiz bitince oluşan CSV raporları buraya kaydediliyor.
- **Dockerfile** — projeyi container'da çalıştırmak için.

### Kurulum ve çalıştırma

**Yöntem 1 — Python (manuel):**

```bash
pip install -r requirements.txt   # sadece YAML okumak için bir kütüphane, ağır bir şey yok
python main.py
```

**Yöntem 2 — Docker:**

```bash
docker-compose build
docker-compose run --rm log-analyzer
```

### Nasıl kullanılır?

Program açıldığında 3 seçenekli bir menü gelir:

1. **Dosya analizi (statik):** kaydedilmiş bir log dosyasını baştan sona tarar. Dosya yolunu ister (ör. `logs/auth.log`), bir özet çıkarır (kaç hata, kaç saldırı) ve ardından `reports/` klasörüne detaylı CSV rapor kaydetmeyi önerir.
2. **Canlı takip:** Linux'taki `tail -f` gibi çalışır. Dosya yolunu girersiniz (ör. `logs/canli.log`), program dosyayı sürekli dinler; yeni bir satır eklendiği an (ör. bir saldırı girişimi) bunu yakalar ve ekrana kırmızı bir ALARM basar. Test için program açıkken başka bir terminalden o dosyaya satır ekleyebilirsiniz.
3. **Çıkış.**

### Tespit edilebilen saldırılar

`config/rules.yaml` içinde tanımlı kurallar:

- SSH Brute Force (hatalı şifre denemeleri)
- Root Login
- SQL Injection
- XSS (zararlı script çalıştırma denemeleri)
- Yeni kullanıcı oluşturma (şüpheli hesap açılması)
- Sudo yetkisi (yetkili komut çalıştırılması)
- Kritik sistem hataları

### Notlar

- Türkçe karakter sorunu olmaması için dosya okuma işlemlerinde UTF-8 kullanıldı.
- Canlı takip modundan çıkmak için `Ctrl` + `C`.

### Lisans

MIT — bkz. [LICENSE](./LICENSE).
