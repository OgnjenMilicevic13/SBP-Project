import pandas as pd
from pymongo import MongoClient

file_path = 'E:\\downloads\\sbp mma dataset\\masterMLpublic.csv'
df = pd.read_csv(file_path)

required_columns = [
    'date', 'result', 'fighter', 'opponent', 'division', 'method', 
    'total_comp_time', 'round', 'time', 'referee', 'time_format'
]
df = df[required_columns]

df['fight_id'] = df.apply(lambda row: '_'.join([row['fighter'], row['opponent'], row['date']]), axis=1)

fights_data = []
for _, row in df.iterrows():
    fight_document = {
        'fight_id': row['fight_id'],
        'date': row['date'],
        'result': row['result'],
        'fighter_name': row['fighter'],
        'opponent_name': row['opponent'],
        'division': row['division'],
        'method': row['method'],
        'total_comp_time': row['total_comp_time'],
        'round': row['round'],
        'time': row['time'],
        'referee': row['referee'],
        'time_format': row['time_format']
    }
    fights_data.append(fight_document)

client = MongoClient('mongodb://localhost:27018/') 
db = client['projekat']
fights_collection = db['fights']

fights_collection.insert_many(fights_data)

print("Data inserted successfully.")