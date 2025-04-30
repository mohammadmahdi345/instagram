# ✅ Backend Developer Checklist – Instagram Clone Project

این چک‌لیست برای توسعه‌دهنده‌ی بک‌اند طراحی شده تا پروژه را از نظر ویژگی، امنیت، کیفیت و مستندسازی کامل و حرفه‌ای کند.

---

## 📦 ساختار و معماری پروژه

- [ ] تقسیم اپلیکیشن‌ها: `users`, `posts`, `comments`, `likes`, `stories`, `follows`, `notifications`, `bookmarks`
- [ ] اپ جداگانه برای اجزای مشترک: `core` (BaseModel, validators, file utils)
- [ ] استفاده از `apps.py` و تنظیمات سفارشی هر اپ

---

## 🔑 احراز هویت و ثبت‌نام

- [ ] ثبت‌نام با تایید ایمیل (اختیاری)
- [ ] ورود با OAuth2 یا JWT (ترجیحاً با `django-oauth-toolkit` یا `SimpleJWT`)
- [ ] قابلیت تغییر رمز عبور و بازیابی رمز با ایمیل
- [ ] امکان غیرفعال‌سازی حساب کاربری

---

## 📸 ماژول‌های اصلی

### Post
- [ ] ایجاد، حذف، ویرایش پست
- [ ] لایک، ذخیره (Bookmark)
- [ ] فید کاربر: پست‌های کاربران دنبال‌شده

### Comment
- [ ] کامنت و ریپلای (تو در تو)
- [ ] حذف و ویرایش فقط توسط صاحب

### Story
- [ ] آپلود استوری + انقضای ۲۴ ساعته
- [ ] بازدیدکنندگان استوری

### Follow
- [ ] فالو و آنفالو
- [ ] پیشنهاد فالو براساس mutual

### Notification
- [ ] نوتیف برای لایک/کامنت/فالو

### Chat (اختیاری)
- [ ] چت ساده با WebSocket (Django Channels)

---

## 🔐 امنیت

- [ ] فعال بودن HTTPS (`SECURE_SSL_REDIRECT = True`)
- [ ] جلوگیری از CSRF و XSS
- [ ] استفاده از `ALLOWED_HOSTS` و `DEBUG = False` در Production
- [ ] بررسی MIME type و حجم فایل‌های آپلودی
- [ ] محافظت در برابر brute-force (با `django-axes` یا rate limiting DRF)
- [ ] ذخیره مقادیر حساس در `.env` (با `django-environ`)
- [ ] CORS محدود فقط به دامنه‌ی فرانت‌اند (با `django-cors-headers`)
- [ ] محدودسازی دسترسی با `IsAuthenticated`, `IsOwner`, `IsAdminUser` و غیره

---

## 📄 مستندات و داکیومنت API

- [ ] Swagger UI با `drf-yasg` یا `drf-spectacular`
- [ ] توضیح ورودی و خروجی هر endpoint
- [ ] نمونه توکن احراز هویت برای تست در داکیومنت

---

## 🧪 تست و پوشش کد

- [ ] استفاده از `pytest` یا `unittest`
- [ ] تست: احراز هویت، ایجاد پست، لایک، کامنت، دنبال کردن
- [ ] پوشش تست بالای ۷۰٪

---

## ☁️ Docker و Deploy (اختیاری ولی حرفه‌ای)

- [ ] `Dockerfile` و `docker-compose.yml` برای backend + db
- [ ] استفاده از `Gunicorn` برای WSGI و `daphne` برای ASGI
- [ ] راه‌اندازی سیستم CI (مثل GitHub Actions) برای تست خودکار
- [ ] دستورالعمل deploy به سرور (مثلاً VPS یا Render)

---

## 📚 سایر موارد

- [ ] صفحه admin سفارشی با `list_display`, `search_fields`, `readonly_fields`
- [ ] pagination برای فید، کامنت، فالوورها
- [ ] فیلتر، سرچ و مرتب‌سازی برای لیست پست‌ها و کاربران
- [ ] ساخت endpointهای مناسب برای فرانت‌اند با JSON structure تمیز

---

> با تکمیل این چک‌لیست، پروژه شما آماده تبدیل‌شدن به یک نمونه واقعی و قابل عرضه از یک کلون شبکه اجتماعی مثل اینستاگرام خواهد بود.
