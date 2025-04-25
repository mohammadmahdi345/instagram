#!/bin/bash

echo "✅ شروع سرور Django..."

while true; do
  python manage.py runserver 0.0.0.0:8003
  echo "❌ سرور کرش کرد. ۳ ثانیه صبر می‌کنیم و دوباره تلاش می‌کنیم..."
  sleep 3
done