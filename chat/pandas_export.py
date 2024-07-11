import pandas as pd
import json

df = pd.read_excel("test2.xlsx", sheet_name=0)

new_df = pd.DataFrame(columns=['name', 'env_name', 'key'])

for index, row in df.iterrows():
    vars_json_str = row['vars']

vars_dict = json.loads(vars_json_str)

if 'spring.datasource.username' in vars_dict:
    username = vars_dict['spring.datasource.username']
    new_df = new_df.append({'name': row['name'], 'env_name': row['env_name'], 'key': username}, ignore_index=True)

print(new_df)
