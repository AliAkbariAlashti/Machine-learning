import pandas as pd
import ast

# def apriori_recommender(rules: pd.DataFrame, item_list: list, product_data: pd.DataFrame):
    
#     while True:
#         item_set = set(item_list)

#         # فیلتر کردن قوانین که antecedents شامل حداقل یکی از آیتم‌های ورودی باشند
#         filtered_rules = rules[rules['antecedents'].apply(lambda x: not x.isdisjoint(item_set))]
        
#         # فیلتر کردن مواردی که کانفیدنس کمتر از 0.4 دارند
#         filtered_rules = filtered_rules[filtered_rules['confidence'] > 0.1]
        
#         # استخراج و مرتب‌سازی بر اساس کانفیدنس
#         recommended_items = (filtered_rules[['consequents', 'confidence']]
#                              .explode('consequents')
#                              .sort_values(by='confidence', ascending=False))
        
#         # حذف مقادیر تکراری و آیتم‌های ورودی از پیشنهادات
#         recommended_items = recommended_items[~recommended_items['consequents'].isin(item_list)].drop_duplicates(subset=['consequents'])
        
#         # اضافه کردن نام کالاها از دیتافریم محصول
#         recommended_items = recommended_items.merge(product_data, left_on='consequents', right_on='ProductId', how='left')
#         recommended_items = recommended_items[['ProductId', 'ProductName', 'confidence']].drop_duplicates()

#         print(recommended_items)
        
#         # دریافت ورودی از کاربر برای اضافه کردن کالای جدید
#         new_item = input("کد کالای جدید را وارد کنید (یا 'exit' برای خروج): ")
#         if new_item.lower() == 'exit':
#             break
#         try:
#             new_item = int(new_item)
#             if new_item not in item_list:
#                 item_list.append(new_item)
#             else:
#                 print("کد کالا قبلا وارد شده است.")
#         except ValueError:
#             print("کد کالا نامعتبر است. لطفا عدد وارد کنید.")
    
#     return recommended_items

# خواندن داده‌ها از فایل CSV
rules_df = pd.read_csv("rules.csv")
# product_data = pd.read_csv("export-sales-report-20250202.csv")

# تبدیل رشته‌ها به لیست برای ستون‌های antecedents و consequents
def convert_to_frozenset(x):
    try:
        if isinstance(x, str):
            x = x.replace("frozenset(", "").replace(")", "")
            return frozenset(ast.literal_eval(x))
        return frozenset()
    except Exception as e:
        print(f"Error converting {x}: {e}")
        return frozenset()

rules_df['antecedents'] = rules_df['antecedents'].apply(convert_to_frozenset)
rules_df['consequents'] = rules_df['consequents'].apply(convert_to_frozenset)

# # دریافت ورودی اولیه از کاربر
# initial_item = int(input("کد کالای اولیه را وارد کنید: "))
# recommended = apriori_recommender(rules_df, [initial_item], product_data)

x = int(input("کد محصول را وارد کنید: "))
p_list = []
p_list.append(x)
def apriori_recommender(rules_df: pd.DataFrame, item_list: list):
    filtered_rules = pd.DataFrame()

    for item in item_list:
        filtered_rules = pd.concat([filtered_rules, rules_df[rules_df['antecedents'].apply(lambda x: item in x)]])

    filtered_rules = filtered_rules[filtered_rules['confidence'] > 0.1]

    recommended_items = (filtered_rules[['consequents', 'confidence']]
                         .explode('consequents')
                         .sort_values(by='confidence', ascending=False))

    return recommended_items['consequents'].tolist()
def drop (lsrecom):
    rlst = []
    for i in lsrecom:
        if i not in rlst:
            rlst.append(i)
    return rlst

while True:
    recommended = apriori_recommender(rules_df, p_list)
    recommended.pop(new_item)
    recommendeddf = pd.DataFrame(drop(recommended), columns=['ProductId'])
    print(recommendeddf.head(3))  # نمایش 3 محصول اول توصیه شده

    new_item = input("کد کالای جدید را وارد کنید (یا 'exit' برای خروج): ")
    if new_item.lower() == 'exit':
        break
    try:
        new_item = int(new_item)
        if new_item not in p_list:
            p_list.append(new_item)
        else:
            print("کد کالا قبلا وارد شده است.")
    except ValueError:
        print("کد کالا نامعتبر است. لطفا عدد وارد کنید.")