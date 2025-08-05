# Telegram Qeydiyyat və Girişə Nəzarət Botu

Bu layihə Telegram kanalına giriş üçün qeydiyyat və ödəniş nəzarəti botudur. İstifadəçi məlumatlarını toplayır, ödəniş qəbzini adminə göndərir və təsdiqləndikdə unikal giriş linki yaradır.

## Xüsusiyyətlər

- Ad/Soyad, telefon nömrəsi və ödəniş qəbzi toplanır
- Məlumatlar SQLite verilənlər bazasında saxlanılır
- Admin təsdiqlədikdə istifadəçiyə 24 saatlıq unikal kanal linki göndərilir
- `/start`, `/get_channel_id`, `/ping` komandaları

## Quraşdırma

1. **Python 3.8+** quraşdırın.
2. Lazımi paketləri quraşdırın:
   ```
   pip install aiogram
   ```
3. `config.py` faylında aşağıdakı dəyişənləri doldurun:
   - `BOT_TOKEN`
   - `ADMIN_ID`
   - `CARD_NUMBER`
   - `DB_PATH`
   - `CHANNEL_ID`

## İstifadə

Terminalda layihə qovluğunda aşağıdakı əmri yazın:
```
python run.py
```

## Fayllar

- `run.py` — əsas bot kodu
- `config.py` — konfiqurasiya parametrləri
- `users` cədvəli — istifadəçi məlumatları üçün SQLite DB

## Əsas Komandalar

- `/start` — qeydiyyata başlamaq
- `/get_channel_id` — cari chat ID-ni göstərir (admin üçün)
- `/ping` — botun işlədiyini yoxlamaq

## Lisenziya

MIT

---

**Əlavə sualınız olarsa,