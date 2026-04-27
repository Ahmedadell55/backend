# 🚀 Darb SmartCity Backend

## الرفع على Railway

### الخطوة 1 — ارفع الملفات
- افتح railway.app
- New Project → Deploy from GitHub أو ارفع الـ zip

### الخطوة 2 — Variables في Railway
روح Settings → Variables وحط:

| اسم المتغير | القيمة |
|---|---|
| SUPABASE_URL | https://jgoizofoygoewtdrxatx.supabase.co |
| SUPABASE_KEY | (الموجود في ملف .env) |
| DEBUG | False |
| FRONTEND_URL | (رابط Netlify بعد ما ترفع الفرونت) |

### الخطوة 3 — بعد الرفع
Railway هيديك رابط زي:
`https://darb-backend.up.railway.app`

احتفظ بالرابط ده وحطه في Netlify كـ environment variable.

## تشغيل محلي
```bash
pip install -r requirements.txt
python main.py
```
الباك هيشتغل على: http://localhost:8000
الـ API Docs على: http://localhost:8000/docs
