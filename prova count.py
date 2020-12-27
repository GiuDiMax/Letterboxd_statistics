import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv("output/database.csv", low_memory=False)
df = pd.DataFrame(df)

stringa = 'cast'
filter_col = [col for col in df if col.startswith(stringa)]
new_db2 = pd.DataFrame()
for col in filter_col:
    new_db = df[[col,'rate']]
    new_db.columns = [stringa,'rate']
    new_db2 = pd.concat([new_db2, new_db]).dropna()

db = new_db2.reset_index(drop=True)
db = (db.groupby(stringa).agg({stringa:'count', 'rate':'mean'}))
db.index.name = None
db.reset_index(level=0, inplace=True)
db.columns = [stringa,'sum','avg']
db = db[db['sum']>3].sort_values(by=['avg'], ascending=False)
print(db)
