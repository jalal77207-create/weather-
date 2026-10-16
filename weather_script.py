import csv
from datetime import datetime, timedelta, timezone
import os
import requests

# إعدادات الـ API
API_KEY = "3ae6ca1ee05345255e5b11f85b399698"
CITY = "Sana'a"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# تحديد المنطقة الزمنية لليمن (جرينتش + 3 ساعات)
yemen_timezone = timezone(timedelta(hours=3))


def get_weather_data():
  try:
    response = requests.get(URL)
    data = response.json()

    if response.status_code == 200:
      temp = data["main"]["temp"]
      humidity = data["main"]["humidity"]
      pressure = data["main"]["pressure"]
      cloud_cover = data["clouds"]["all"]
      rain = data.get("rain", {}).get("1h", 0)

      return {
          "temperature": temp,
          "humidity": humidity,
          "rain_chance": rain,
          "cloud_cover": cloud_cover,
          "pressure": pressure,
      }
    else:
      print(f"خطأ في جلب البيانات. كود الخطأ: {data.get('cod')}")
      return None
  except Exception as e:
    print(f"حدث خطأ في الاتصال: {e}")
    return None


# إعداد اسم ملف الـ CSV والعناوين
filename = f"weather_of_{CITY}.csv"
header = [
    "درجة الحرارة (C)",
    "الرطوبة (%)",
    "الأمطار (mm)",
    "الغطاء السحابي (%)",
    "الضغط الجوي (hPa)",
    "الوقت",
]

# التحقق هل الملف موجود؟ إذا لم يكن موجوداً ننشئه ونكتب العناوين
if not os.path.isfile(filename):
  with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(header)
  print(f"تم إنشاء ملف جديد: {filename}")

# جلب البيانات وإضافتها للملف
weather = get_weather_data()

if weather:
  current_time = datetime.now(yemen_timezone).strftime("%Y-%m-%d %H:%M:%S")

  with open(filename, mode="a", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow([
        weather["temperature"],
        weather["humidity"],
        weather["rain_chance"],
        weather["cloud_cover"],
        weather["pressure"],
        current_time,
    ])

  print(f"[{current_time}] تم الحفظ بنجاح: حرارة {weather['temperature']}°C")
else:
  print("فشل في جلب البيانات لهذه الدورة.")
