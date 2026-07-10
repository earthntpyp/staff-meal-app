# 🍳 Gin-Rai-Dee (กินไรดี??) — Staff Meal Randomizer

🌐 Live: https://gin-rai-dee.up.railway.app

เว็บแอปช่วยหัวหน้าครัว/เชฟ ที่นึกเมนูอาหารพนักงาน (staff meal) ไม่ออก

## ฟีเจอร์
- 🎰 **สุ่มเมนู** ตามโปรตีน (ไก่ / หมู / เนื้อ / ไข่-ผัก) พร้อมแอนิเมชัน slot machine
- 📖 **82 เมนู** พร้อมวัตถุดิบ + วิธีทำทีละขั้น (สัดส่วน ~5 คน) ครอบคลุม ไทยภาคกลาง / อีสาน / เหนือ / ไทย × ญี่ปุ่น
- 🟢🟡🔴 **ระดับความยาก** และ ⏱ เวลาปรุงโดยประมาณ ทุกเมนู
- 🔍 กรองตามภาค / ระดับความยาก และค้นหาจากชื่อเมนูหรือวัตถุดิบ
- ⭐ **เพิ่มสูตรแชร์ให้ทีม** — ทุกคนที่เข้าเว็บพิมพ์เพิ่มสูตรได้ เก็บไว้ที่ server แชร์กันทั้งร้าน

## รันในเครื่อง
ใช้ Python standard library ล้วน ไม่ต้องติดตั้งอะไรเพิ่ม:

```bash
python3 server.py
# เปิด http://localhost:3939
```

ให้ทีมในร้านเข้าผ่าน `http://<ไอพีเครื่องคุณ>:3939` บน WiFi เดียวกัน

## Deploy บน Railway
1. เชื่อม repo นี้กับ Railway (New Project → Deploy from GitHub repo)
2. Railway จะตรวจจับ Python + `Procfile` อัตโนมัติ และตั้งค่า `PORT` ให้เอง
3. (แนะนำ) เพิ่ม **Volume** ที่ mount path `/app/data` เพื่อให้สูตรที่ทีมเพิ่มไม่หายตอน redeploy

## โครงสร้าง
```
server.py            # HTTP server + API (GET/POST /api/recipes)
public/index.html    # หน้าเว็บทั้งหมด (UI + logic)
public/recipes.js    # ฐานข้อมูล 82 เมนู
data/community.json  # สูตรที่ทีมเพิ่ม (สร้างอัตโนมัติ)
```
