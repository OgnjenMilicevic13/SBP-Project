import pandas as pd
from pymongo import MongoClient

file_path = 'E:\\downloads\\sbp mma dataset\\masterMLpublic.csv'
df = pd.read_csv(file_path)

fighter_columns = ['fighter', 'stance', 'dob', 'reach', 'height']
fighters_df = df[fighter_columns].drop_duplicates(subset=['fighter']).reset_index(drop=True)

fighters_df['height'] = fighters_df['height'].apply(lambda x: x * 2.54 if pd.notnull(x) else x)
fighters_df['reach'] = fighters_df['reach'].apply(lambda x: x * 2.54 if pd.notnull(x) else x)

def remove_nulls(d):
    return {k: v for k, v in d.items() if pd.notnull(v)}

fighters_data = [remove_nulls(doc) for doc in fighters_df.to_dict(orient='records')]

client = MongoClient('mongodb://localhost:27018/') 
db = client['projekat']
fighters_collection = db['fighters']

fighters_collection.insert_many(fighters_data)

print("Data inserted successfully.")
