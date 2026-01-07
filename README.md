# 🗣️ Lokal Türkçe Metinden Sese (Piper + Python + Web)

Bu proje, **Windows 10 / 11** üzerinde **tamamen lokal** çalışan bir **Türkçe metinden sese (TTS)** sistemidir.

* 🌐 Tarayıcıdan çalışır (lokal web sayfası)
* 🧠 İnternet gerekmez (model indirildikten sonra)
* 🔊 Metni hoparlörden okur
* 💾 WAV olarak indirir
* ⚙️ Hız / sakinlik / canlılık / ses kısma seçenekleri vardır

---

## ✨ Özellikler

* ✅ Türkçe düzgün okuma (Piper neural TTS)
* ✅ Python ile çalışır
* ✅ Web arayüzü (metni yapıştır → dinle)
* ✅ Hızlı / yavaş okuma
* ✅ Sakin / canlı ton
* ✅ Ses azaltma
* ✅ Dosya adı + zaman damgası
* ❌ Ses klonlama yok (bilinçli olarak sade tutulmuştur)

---

## 🖥️ Gereksinimler

* Windows 10 veya Windows 11
* **Python 3.10+** (3.13 dahil)
* İnternet (sadece ilk model indirme için)

> ⚠️ Başka hiçbir şey gerekmez.
> Node, CUDA, ffmpeg vs. **gerekli değil**.

---

## 🚀 Kurulum (Adım Adım)

### 1️⃣ İstersen bu repoyu indir

* Yeşil **Code → Download ZIP**
* ZIP’i aç
* Örnek klasör:

```
C:\piper_tts\
```
veya verdiğimiz web_tts.py dosyasını "C:\piper_tts\" içine koy

---

### 2️⃣ Gerekli Python paketlerini kur

Klasör adresinde CMD yaz, komut satırı açılsın. Komut satırında (CMD):

```bat
pip install flask piper-tts soundfile numpy
```

---

### 3️⃣ Türkçe Piper ses modelini indir

Klasöre gir:

```bat
cd C:\piper_tts
```

Türkçe modeli "C:\piper_tts" içine indirmek için kullanılacak kod:

```bat
python -m piper.download_voices tr_TR-dfki-medium
```

Aşağıdaki dosyalar indirilmiş olacak:

```
tr_TR-dfki-medium.onnx
tr_TR-dfki-medium.onnx.json
```

---

### 4️⃣ Web uygulamasını çalıştır

```bat
python web_tts.py
```

Terminalde şunu görmelisin:

```
Running on http://127.0.0.1:5000
```

---

### 5️⃣ Tarayıcıdan aç 🎉

Tarayıcıya yaz:

```
http://127.0.0.1:5000
```

---

## 🌐 Web Arayüzü Kullanımı

1. Metni kutuya yapıştır
2. İstersen dosya adı yaz
3. Seçenekleri işaretle:

   * ⏩ Hızlı
   * 🐢 Yavaş
   * 😐 Sakin
   * 😃 Canlı
   * 🔉 Sesi azalt
4. **Üret + Çal** → tarayıcıdan dinle
5. **Üret + İndir** → WAV dosyası indir

Üretilen dosyalar:

```
outputs/
```

---

## 📂 Klasör Yapısı

```
piper_tts/
│
├─ web_tts.py
├─ tr_TR-dfki-medium.onnx
├─ tr_TR-dfki-medium.onnx.json
├─ outputs/
│   └─ tts_20240101_123456.wav
```

---

## ❓ Sık Sorulanlar

### 🔹 İnternet gerekiyor mu?

❌ Hayır.
Sadece **ilk model indirme** sırasında gerekir.

---

### 🔹 Kadın sesi var mı?

Şu an kullanılan Türkçe model **tek seslidir**.
Piper’da ses = modeldir. Yeni TR model çıkarsa eklenebilir.

---

### 🔹 Duygu / fısıltı / bağırma var mı?

Doğrudan yok.
Ancak:

* hız
* sakinlik / canlılık
* ses seviyesi

ile **pratik kontrol** sağlanır.

---

### 🔹 Ses çalmıyor ama dosya var?

Tarayıcı otomatik çalmayı engelleyebilir.
Bu durumda:

* Play tuşuna bas
* Veya **Üret + İndir** ile dosyayı aç

---

## 🛡️ Lisans & Notlar

* Piper: GPL lisanslıdır
* Bu proje **lokal kullanım** amaçlıdır
* Ses klonlama veya kimlik taklidi içermez

---

## 📌 Yol Haritası (Opsiyonel)

* 🎚️ Slider ile ince hız kontrolü
* 📜 Uzun metni otomatik bölme
* 🎭 “Dramatik / fısıltı” presetleri
* 🧩 API olarak dışarı açma

---

## 👋 Kapanış

Bu repo, **Windows + Python bilen herkesin**
“metni yaz → sesi duy” ihtiyacını **en sade ve güvenli** şekilde çözmek için hazırlandı.

> Yeni Türkçe ses modeli çıkarsa CMD penceresinde şu koddan görebilirsin:
```
python -m piper.download_voices
```
