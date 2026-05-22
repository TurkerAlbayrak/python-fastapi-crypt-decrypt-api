# CryptApp 

CryptApp, kullanıcı bazlı şifreleme (encryption) ve şifre çözme (decryption) işlemlerini gerçekleştiren, FastAPI tabanlı modern bir REST API servisidir. Yanında kolay test ve otomasyon için komut satırı aracı (CLI) içeren bir Python istemcisi ile birlikte gelir.

## Özellikler

- **FastAPI Backend**: Hızlı, asenkron destekli ve otomatik interaktif API dokümantasyonu (Swagger UI).
- **Güvenli Şifreleme**: `cryptography` kütüphanesindeki `Fernet` (AES-128 tabanlı simetrik şifreleme) standardını kullanır.
- **Kullanıcı Yetkilendirme**: Özel `x-api-key` başlığı (header) üzerinden yetkilendirme kontrolü yapılır.
- **İstemci CLI**: Komut satırından şifreleme, şifre çözme ve performans testleri (stres testi) yapabilen hazır istemci programı.
- **Performans Ölçümü**: Sunucu kapasitesini ölçmek için saniye başına istek sayısını (RPS) gösteren entegre stres testi.

---

## Gereksinimler

Projenin çalıştırılması için Python 3.8+ gereklidir. Gerekli kütüphaneler:

- `fastapi`
- `uvicorn`
- `cryptography`
- `requests`
- `pydantic`

### Kurulum

Gerekli paketleri pip yardımıyla kurabilirsiniz:

```bash
pip install fastapi uvicorn cryptography requests pydantic
```

---

## Proje Yapısı

```text
cryptapp/
├── crypt.py       # FastAPI web sunucusu (şifreleme/şifre çözme mantığı ve kullanıcı veritabanı)
└── client.py      # Sunucuya istek atan ve CLI arayüzü sunan istemci betiği
```

---

## Sunucuyu Başlatma

FastAPI sunucusunu (Uvicorn ile) başlatmak için projenin kök dizininde şu komutu çalıştırın:

```bash
uvicorn crypt:app --reload
```

Sunucu varsayılan olarak `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.
- **Swagger UI (Dokümantasyon):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresinden API uç noktalarını görsel olarak inceleyip test edebilirsiniz.

---

## İstemci (Client CLI) Kullanımı

Sunucu arka planda çalışırken, `client.py` üzerinden terminalden doğrudan işlemler gerçekleştirebilirsiniz.

### Kullanıcı Bilgileri
API'de örnek olarak tanımlanmış iki kullanıcı bulunmaktadır:
- **user1** (API Key: `key-user-1`)
- **user2** (API Key: `key-user-2`)

*(Her kullanıcının şifreleme anahtarı, sunucu her başlatıldığında arka planda rastgele olarak yeniden üretilir).*

### 1. Şifreleme (Encrypt)
Belirli bir kullanıcı adıyla metin şifrelemek için:

```bash
python client.py encrypt <kullanici_adi> "<sifrelenecek_metin>"
```

**Örnek:**
```bash
python client.py encrypt user1 "Merhaba Dunya"
```
**Çıktı:**
```json
RESULT: {'user': 'user1', 'encrypted': 'gAAAAAB...'}
```

### 2. Şifre Çözme (Decrypt)
Şifrelenmiş bir metnin (cipher text) orijinal halini elde etmek için:

```bash
python client.py decrypt <kullanici_adi> "<sifreli_metin>"
```

**Örnek:**
```bash
python client.py decrypt user1 "gAAAAAB..."
```
**Çıktı:**
```json
RESULT: {'user': 'user1', 'decrypted': 'Merhaba Dunya'}
```

### 3. Stres Testi (Stress Test)
Sunucunun performansını ve hızını ölçmek için belirlenen miktarda ardışık şifreleme isteği gönderebilirsiniz:

```bash
python client.py stress <kullanici_adi> <istek_sayisi>
```

**Örnek:**
```bash
python client.py stress user1 1000
```
**Çıktı:**
```text
Stress test başlıyor (1000 request)...
Bitti!
Süre: 1.45 saniye
RPS: 689.66 request/s
```

---

## Güvenlik & Çalışma Mantığı

1. **Simetrik Anahtar Üretimi**: Uygulama ayağa kalktığında `Fernet.generate_key()` ile her kullanıcı için bellek üzerinde (In-Memory) eşsiz bir 32-byte anahtar (key) oluşturulur.
2. **Kimlik Doğrulama**: Sunucuya atılan her istekte `x-api-key` başlığı aranır. Gönderilen API anahtarı `users_db` içindeki değerle eşleşiyorsa işlem onaylanır, aksi takdirde `401 Unauthorized` hatası fırlatılır.
3. **Kullanıcı Ayrımı**: Her kullanıcı sadece kendi anahtarı ile şifrelenmiş veriyi çözebilir. `user1` anahtarı ile şifrelenen bir veri `user2` API anahtarı kullanılarak çözülmeye çalışılırsa şifre çözme hatası oluşur.
4. **Kalıcılık**: Veritabanı ve anahtarlar bellek üzerinde (In-Memory) tutulduğu için sunucu her yeniden başlatıldığında anahtarlar değişir ve eski şifrelenmiş metinler çözülemez hale gelir.
