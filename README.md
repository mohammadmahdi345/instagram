# Instagram Clone – Backend with Django & DRF

این یک پروژه **کلون از اینستاگرام** است که با استفاده از **Django REST Framework** ساخته شده. هدف پروژه پیاده‌سازی قابلیت‌های شبکه اجتماعی مانند **پست**, **کامنت‌**, **لایک‌**, **فالو/آنفالو**, **استوری‌** و **نوتیفیکیشن‌** است. این پروژه همچنین از **jwt** برای احراز هویت استفاده میکند

## ویژگی‌ها:

- امکان ثبت‌نام و ورود با ایمیل,شماره تلفن,نام کاربری همراه رمز عبور
- سیستم فالو/آنفالو
- لایک و کامنت گذاشتن روی پست‌ها و رپیلای روی کامنت
- استوری‌های ۲۴ ساعته
- نوتیفیکیشن‌ها برای فالو کردن، لایک کردن و کامنت گذاشتن
-  مدیریت امنیت با JWTهمراه سیستم احراز هویت سفارشی
- تست خودکار با `pytest`
- صفحه ادمین سفارشی
- استفاده از دیتابیس postgres

## پیش‌نیازها:

برای راه‌اندازی این پروژه به موارد زیر نیاز دارید:

- Python 3.8+
- Django 3.2+
- Django REST Framework
- mysql
- pip (برای نصب بسته‌ها)

## نصب و راه‌اندازی:

1. پروژه را کلون کنید:
    ```bash
    git clone https://github.com/mohammadmahdi345/instagram.git
    cd instagram
    ```

   

اجرای پروژه در محیط توسعه (با Docker Compose)

docker-compose up -d --build برای اجرای کانتینرها
docker-compose down برای توقف کانتینرها
docker-compose exec web pytest   اجرای تست ها با پایتست

    


6. حالا می‌تونی به پروژه دسترسی پیدا کنی:
    - آدرس: [http://localhost:8000](http://localhost:8000)

## تست‌ها:

برای اجرای تست‌ها از `pytest` استفاده می‌کنیم:

1. نصب pytest:
    ```bash
    pip install pytest
    ```

2. اجرای تست‌ها:
    ```bash
    pytest
    ```

## ساختار پروژه:

instagram/ ├── api/ # شامل viewها و serializers ├── users/ # مدل‌ها و مدیریت کاربران ├── posts/ # پست‌ها و کامنت‌ها ├── requirements.txt # لیست وابستگی‌ها └── manage.py # مدیریت پروژه


## مشارکت در پروژه:

اگر مایل به مشارکت در این پروژه هستید، می‌توانید از مراحل زیر پیروی کنید:

1. فورک کنید پروژه رو.
2. یک شاخه جدید بسازید (`git checkout -b feature-name`).
3. تغییرات مورد نظر رو اعمال کنید.
4. تغییرات رو کامیت کنید (`git commit -am 'Add new feature'`).
5. شاخه‌تون رو به گیت‌هاب پوش کنید (`git push origin feature-name`).
6. درخواست کشش (Pull Request) بدید.

## لایسنس:

این پروژه تحت لایسنس MIT منتشر شده است. برای اطلاعات بیشتر به [LICENSE](LICENSE) مراجعه کنید.







# ✅ Backend Developer Checklist – Instagram Clone Project

این چک‌لیست برای توسعه‌دهنده‌ی بک‌اند طراحی شده تا پروژه را از نظر ویژگی، امنیت، کیفیت و مستندسازی کامل و حرفه‌ای کند.

---

## 📦 ساختار و معماری پروژه

- [ ] تقسیم اپلیکیشن‌ها: `users`, `posts`, `comments`, `likes`, `stories`, `friendships`, `bookmarks`,'comment_replay,'commentlike'
- 

---

## 🔑 احراز هویت و ثبت‌نام

- [ ] ثبت‌نام با تایید ایمیل (اختیاری)
- [ ] ورود با OAuth2 یا JWT (ترجیحاً با `django-oauth-toolkit` یا `SimpleJWT`)
- [ ] قابلیت تغییر رمز عبور و بازیابی رمز با ایمیل
- [ ] امکان غیرفعال‌سازی حساب کاربری

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
