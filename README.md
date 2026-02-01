# İngilizce Kelime Ezberleme Uygulaması (6 Sefer Tekrar Prensibi) 

Bu proje, **“6 Sefer Tekrar Prensibi”**ni temel alarak kullanıcıların İngilizce kelimeleri kalıcı biçimde öğrenmesini hedefleyen bir masaüstü uygulamasıdır. Yazılım Mühendisliği dersi dönem projesi kapsamında geliştirilmiştir.

---

### Amaçlar
- **Bilimsel Temel:** Unutma eğrisine karşı etkin öğrenme  
- **Aralıklı Tekrar:** 6 farklı zaman diliminde doğru yanıt zorunluluğu  
- **Kullanıcı Deneyimi:** Basit ve sezgisel arayüz
  
---

### Özellikler
1. **Kullanıcı Yönetimi** – Kayıt, giriş, şifre sıfırlama  
2. **Kelime Modülü** – İngilizce–Türkçe ekleme, örnek cümle, isteğe bağlı görsel  
3. **Quiz Sistemi** – 6 kez doğruysa “öğrenildi”, yanlışsa süreç başa döner  
4. **Günlük Hedef Ayarı** – Günlük ezberlenecek kelime sayısını belirleme  
5. **İstatistik & Rapor** – Toplam deneme, başarı oranı, ilerleme grafiği  
6. **Bonus: Wordle-Benzeri Oyun** – Eğlenceli kelime tahmin modu  

---

### Kullanılan Teknolojiler
- **Python 3**  
- **PyQt5** (grafik arayüz)  
- **SQLite** (veritabanı)  
- **pygame** (opsiyonel ses desteği)  

---

### Kurulum & Çalıştırma
1.   Gerekli paketleri yükleyin  

```bash
pip install pyqt5 pygame
```

2.   Proje dizinine geçip uygulamayı başlatın

```bash
cd kelimeEzberleme
python girisSayfasi.py
```

---

## 6 Sefer Tekrar Algoritması
Bir kelimenin “öğrenildi” sayılması için kullanıcı, aşağıdaki zaman aralıklarında o kelimeyi doğru bilmelidir:

Tekrar No	Zaman Aralığı
1. 	1 gün sonra
2.	1 hafta sonra
3.	1 ay sonra
4.	3 ay sonra
5.	6 ay sonra
6.	1 yıl sonra

Not: Herhangi bir tekrar adımında kelime yanlış cevaplanırsa, süreç o kelime için en başa döner.

---

## Proje Yapısı
```text
kelimeEzberleme/
├── girisSayfasi.py         # Uygulamayı başlatan dosya
├── database/
│   └── yazilimYapimi.db    # SQLite veritabanı
├── ui/
│   └── *.py                # PyQt5 arayüz ve kontrol dosyaları
├── assets/
│   └── resimler/           # Kelime görselleri
└── README.md               # Proje dökümanı
```

---

## Geliştiriciler
Büşra Tekdemir
Hasan Yiğit Akbulut
Ozan Korkmaz

Celal Bayar Üniversitesi – Yazılım Mühendisliği 2. Sınıf

Notlar
Bu proje eğitim amaçlı olarak geliştirilmiştir. Yeni özellikler ilerleyen sürümlerde eklenebilir. Geri bildirim ve katkılar için GitHub üzerinden iletişime geçebilirsiniz.
