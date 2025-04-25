#!/bin/sh

echo "⏳ منتظر اتصال به دیتابیس هستیم..."

while ! nc -z db 3306; do
  sleep 1
done

echo "✅ دیتابیس در دسترسه. ادامه می‌دهیم..."

exec "$@"