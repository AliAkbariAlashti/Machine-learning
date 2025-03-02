import pandas as pd
import Levenshtein

# خواندن فایل CSV
df = pd.read_excel('p_id_name.xlsx')

# تبدیل مقادیر ستون name به رشته (برای جلوگیری از خطای تایپ)
df['Name'] = df['Name'].astype(str)

# لیست اسامی و شناسه‌ها
names = df['Name'].tolist()
product_ids = df['ID'].tolist()

# لیست برای ذخیره نتایج
results = []

# محاسبه تشابهات
for i, (id1, name1) in enumerate(zip(product_ids, names)):
    for j, (id2, name2) in enumerate(zip(product_ids, names)):
        if i < j:  # جلوگیری از مقایسه تکراری یا مقایسه با خودش
            # محاسبه فاصله Levenshtein و تبدیل به میزان تشابه
            distance = Levenshtein.distance(name1, name2)
            similarity = 1 - (distance / max(len(name1), len(name2)))
            
            # ذخیره فقط مواردی که شباهت بالای 80٪ دارند
            if similarity > 0.8:
                results.append([id1, name1, id2, name2, round(similarity * 100, 2)])

# تبدیل لیست نتایج به یک دیتافریم پانداس
similarity_df = pd.DataFrame(results, columns=['product_id_1', 'product_1', 'product_id_2', 'product_2', 'similarity'])

# تنظیم نمایش راست‌به‌چپ برای فارسی
pd.options.display.float_format = '{:,.2f}%'.format  # نمایش درصد
pd.options.display.unicode.east_asian_width = True  # اصلاح راست‌چین برای فارسی

# ذخیره در فایل CSV
similarity_df.to_csv('similar_products_with_id.csv', index=False, encoding='utf-8-sig')

# نمایش خروجی
print(similarity_df)
