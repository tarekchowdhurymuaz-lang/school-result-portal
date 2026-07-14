# 📚 School Result Portal

একটি স্কুলের জন্য ফলাফল চেক করার আধুনিক ওয়েবএপস যেখানে শিক্ষার্থীরা সহজেই তাদের রেজাল্ট দেখতে পারবে।

## ✨ বৈশিষ্ট্য

- ✅ **সম্পূর্ণ Flexible**: যেকোনো ফরম্যাটের Excel সাপোর্ট করে
- ✅ **ধাপে ধাপে সার্চ**: ক্লাস → শিফট → পরীক্ষা → রোল/নাম
- ✅ **সুন্দর UI**: সাবজেক্টওয়াইজ ফলাফল প্রদর্শন
- ✅ **দ্রুত**: ৫০০+ একযোগে ইউজার সামলাতে পারে
- ✅ **স্কেলেবল**: Excel থেকে সবকিছু ম্যানেজ করুন

## 🛠️ প্রযুক্তি

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Data**: Excel (XLSX)
- **Hosting**: PythonAnywhere

## 📁 প্রজেক্ট স্ট্রাকচার

```
school-result-portal/
├── app.py                 # Flask main app
├── config.py             # Configuration
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Main styles
│   └── js/
│       └── script.js     # Frontend logic
├── templates/
│   ├── index.html        # Main page
│   └── result.html       # Result display page
├── utils/
│   ├── excel_parser.py   # Flexible Excel parser
│   └── data_handler.py   # Data processing
└── uploads/              # Excel files upload folder
```

## 🚀 দ্রুত শুরু

### প্রিরিকোয়ারমেন্ট
- Python 3.8+
- pip

### ইনস্টলেশন

```bash
# Clone করুন
git clone https://github.com/tarekchowdhurymuaz-lang/school-result-portal.git
cd school-result-portal

# ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies ইনস্টল করুন
pip install -r requirements.txt

# অ্যাপ চালান
python app.py
```

ব্রাউজারে খুলুন: `http://localhost:5000`

## 📊 Excel ফাইল ফরম্যাট

যেকোনো ফরম্যাটে কাজ করে! শুধু এই কলামগুলো থাকা দরকার:

| প্রয়োজনীয় | কলাম নাম (যেকোনো) | উদাহরণ |
|-----------|------------------|--------|
| ✅ | ক্লাস/Class/শ্রেণী | ৬, ৭, ৮ |
| ✅ | শিফট/Shift | সকাল, বিকাল |
| ✅ | পরীক্ষা/Exam | মাসিক ১, বার্ষিক |
| ✅ | রোল/Roll | ১, २, ३ |
| ✅ | নাম/Name | রহিম, সালমা |
| ✅ | বিষয়গুলো | বাংলা, ইংরেজি, গণিত... |

**উদাহরণ Excel:**
```
ক্লাস | শিফট | পরীক্ষা | রোল | নাম | বাংলা | ইংরেজি | গণিত | বিজ্ঞান | সামাজিক
६     | সকাল | মাসিক १ | १    | রহিম | ८५   | ७५     | ९०   | ८८     | ८२
```

## 📝 ব্যবহার

1. **Admin Panel**: Excel ফাইল আপলোড করুন
2. **শিক্ষার্থী**: 
   - ক্লাস বেছে নিন
   - শিফট বেছে নিন
   - পরীক্ষা বেছে নিন
   - রোল নম্বর বা নাম দিন
   - ফলাফল দেখুন! 📊

## 🔧 কনফিগারেশন

`config.py` এ সেটিংস পরিবর্তন করুন:
- Upload folder path
- Maximum file size
- Cache settings

## 🤝 অবদান

Issues এবং Pull Requests স্বাগত! 

## 📄 লাইসেন্স

MIT License

---

**তৈরি করেছেন**: Tarek Chowdhury  
**সংস্করণ**: 1.0.0  
**আপডেট**: জুলাই ২০২৬
