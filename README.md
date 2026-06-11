# 📚 School Print Queue Bot

**[English](#english) | [فارسی](#persian)**

---

## 🇬🇧 English

Telegram bot for managing the printing queue of educational files.

- Teachers upload files (PDF/Photos) with caption: file name, class, date (Solar Hijri), and period.
- Admin selects week, day, and period → views uploaded files → adds them to daily print queue.

### Features

- Teacher sign‑up & login
- Upload files with Solar Hijri date
- Files stored in date‑folders
- Admin panel: week / day / period selection
- Add files to daily print queue
- Profile management
- Add new admin via bot command
- English logs

### Installation

```bash
git clone https://github.com/kiarashkingdom/school_bot.git
cd school_bot
pip install -r requirements.txt
```

#### Database (MySQL)

1. Create a database  
2. Run table creation:

```bash
python DDL.py
```

#### Configuration

Edit `config.py`:

```python
database_name = 'your_database_name'

database_config = {
    'host': 'your_host',
    'user': 'your_user',
    'password': 'your_password'
}

API_TOKEN = 'your_bot_token'
```

#### Run

```bash
python main.py
```

### Usage

- **Teacher:** Sign up → use "Upload file" button → send file with required caption format.
- **Admin:** Log in → use "Weekly schedule" → select week, day, period → view files → add to print queue.

---
---

## 📁 Project Structure

```
school_bot/
├── main.py          # Main bot code
├── config.py           # Database configuration
├── DDL.py              # Create tables
├── DML.py              # Insert operations
├── DQL.py              # Query operations
├── Texts.py            # Text messages
├── requirements.txt    # Dependencies
└── Data/               # Uploaded files (date‑folders)
```

## 📄 License

MIT License – see [LICENSE](LICENSE) file.

## 👤 Author

**kiarashkingdom**  
GitHub: [@kiarashkingdom](https://github.com/kiarashkingdom)

---

## 🇮🇷 فارسی

ربات تلگرامی مدیریت صف تکثیر فایل‌های آموزشی.

- معلم فایل (عکس یا PDF) را با کپشن شامل نام فایل، کلاس، تاریخ شمسی و زنگ ارسال می‌کند.
- ادمین با انتخاب هفته، روز و زنگ، فایل‌ها را دیده و به صف چاپ روزانه اضافه می‌کند.

### امکانات

- ثبت‌نام و ورود معلم و ادمین
- آپلود فایل با کپشن تاریخ شمسی
- ذخیره فایل در پوشه‌های تاریخ‌بندی شده
- پنل ادمین: انتخاب هفته، روز، زنگ
- اضافه کردن فایل به صف تکثیر روزانه
- پروفایل کاربری
- اضافه کردن ادمین جدید با دستور ربات
- لاگ انگلیسی

### نصب و اجرا

```bash
git clone https://github.com/kiarashkingdom/school_bot.git
cd school_bot
pip install -r requirements.txt
```

#### دیتابیس (MySQL)

1. یک دیتابیس بسازید  
2. ایجاد جداول با دستور زیر:

```bash
python DDL.py
```

#### تنظیمات

در `config.py`:

```python
database_name = 'نام_دیتابیس'

database_config = {
    'host': 'آدرس_هاست',
    'user': 'نام_کاربری',
    'password': 'رمز_عبور'
}

API_TOKEN = 'توکن_ربات'
```

#### اجرا

```bash
python main.py
```

### نحوه استفاده

- **معلم:** ثبت‌نام → دکمه «آپلود فایل جدید» → ارسال فایل با کپشن فرمت مشخص‌شده
- **ادمین:** ورود → دکمه «برنامه هفتگی» → انتخاب هفته، روز، زنگ → مشاهده فایل‌ها → اضافه به صف تکثیر
---

### 📁 ساختار پروژه
```
school_bot/
├── main.py          # کد اصلی ربات
├── config.py        # تنظیمات دیتابیس
├── DDL.py           # ساخت جداول
├── DML.py           # عملیات درج اطلاعات
├── DQL.py           # عملیات دریافت اطلاعات
├── Texts.py         # متن‌های پیام‌ها
├── requirements.txt # کتابخانه‌های مورد نیاز
└── Data/            #فایل‌های آپلود شده (پوشه‌های تاریخ)
```
---

### 📄 مجوز
این پروژه تحت مجوز MIT منتشر شده است – برای جزئیات بیشتر فایل  [LICENSE](LICENSE) را ببینید.

---

### 👤 نویسنده
**kiarashkingdom** 
گیت‌هاب: [@kiarashkingdom](https://github.com/kiarashkingdom)
