import json
import pandas as pd
import pprint as pp
from collections import defaultdict


def p2f(x):
    """http://stackoverflow.com/questions/25669588/convert-percent-string-to-float-in-pandas-read-csv"""
    if isinstance(x, float):
        return x
    x = x.encode('ascii', 'ignore')
    x = x.split('-')[0]
    x = x.strip('N')
    return float(x.strip('%'))/100

sage = pd.read_excel('SAGE2016.xlsx', sheetname="Overall School Results",
                     converters={'Percent Proficient': p2f})
alpine = sage[sage['LEA (District or Charter)']=="ALPINE DISTRICT"]

with open('output.json') as data_file:
    data = json.load(data_file)
output = defaultdict(dict)
for result in data:
    output[result['url']].update(result)

df = pd.DataFrame.from_dict(output, 'index')
df['sub-links-count'] = df['sub-links'].apply(lambda x: 0 if isinstance(x, float) else len(x) )
df['scc_links-count'] = df['scc_links'].apply(lambda x: 0 if isinstance(x, float) else len(x) )
df['total'] = df['sub-links-count'] + df['scc_links-count']
df = df.sort_values("total", ascending=False)
df['uname'] = df['name'].str.replace('Elementary', 'School').str.upper().str.replace('JUNIOR', 'JR HIGH')
df = df.set_index('uname')
alpine.join(df, on='School Name').to_csv('joined.csv')
df.to_csv("output.csv")
print df.head()
