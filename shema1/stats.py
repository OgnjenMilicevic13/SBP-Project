import pandas as pd
from pymongo import MongoClient

file_path = 'E:\\downloads\\sbp mma dataset\\masterMLpublic.csv' 
df = pd.read_csv(file_path)

exclude_columns = [
    'date', 'result', 'fighter', 'opponent', 'division', 'method', 
    'total_comp_time', 'round', 'time', 'referee', 'time_format', 
    'stance', 'dob', 'reach', 'height', 'age'
]

stat_columns = [col for col in df.columns if col not in exclude_columns]

stat_columns = stat_columns[:1000]

df['fight_id'] = df.apply(lambda row: '_'.join([row['fighter'], row['opponent'], row['date']]), axis=1)

statistics_data = []
for _, row in df.iterrows():
    stat_document = {
        'fight_id': row['fight_id'],
        'fighter_name': row['fighter'],
        'opponent_name': row['opponent']
    }
    for col in stat_columns:
        stat_document[col] = row[col]
    statistics_data.append(stat_document)

client = MongoClient('mongodb://localhost:27018/')
db = client['projekat']
stats_collection = db['stats']

stats_collection.insert_many(statistics_data)

print("Data inserted successfully.")
