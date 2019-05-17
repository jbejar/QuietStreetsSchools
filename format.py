import json
import pandas as pd
import pprint as pp
from collections import defaultdict

def load_sage(year):
    df = pd.read_excel('SAGE%s.xlsx' % year, sheetname="Overall School Results",
                         converters={'Percent Proficient': p2f},
                         names=['Year','LEA (District or Charter)','School Name','Subject Area',
                                'Percent Proficient' + str(year)]
                         )
    df['index'] = df.ix[:,1] + df.ix[:,2] + df.ix[:,3]
    return df.set_index('index')

def p2f(x):
    """http://stackoverflow.com/questions/25669588/convert-percent-string-to-float-in-pandas-read-csv"""
    if isinstance(x, float):
        return x
    x = x.encode('ascii', 'ignore')
    x = x.split('-')[0]
    x = x.strip('N')
    return float(x.strip('%'))/100

def load_data(filename):
    with open(filename + '.json') as data_file:
        data = json.load(data_file)
    output = defaultdict(dict)
    for result in data:
        output[result['url']].update(result)
    return pd.DataFrame.from_dict(output, 'index')

sage = load_sage(2016)
sage15 = load_sage(2015)
sage14 = load_sage(2014)
sage = sage.join(sage15.ix[:,4]).join(sage14.ix[:,4])
sage['total improvment'] = (sage['Percent Proficient2016'] -
                      sage['Percent Proficient2014'])
sage['continuous factor'] = ((sage['Percent Proficient2016'] - sage['Percent Proficient2015']) *
                    (sage['Percent Proficient2015'] - sage['Percent Proficient2014'])
                    * sage['total improvment']
                    )


info = load_data('gateway')
info['index'] = info['lea'].str.strip() + info['school_name'].str.strip()
info['addr1'] = info['addr1'].str.strip()
info['addr2'] = info['addr2'].str.strip()
info.rename(index=str, columns={"url": "data-url"}, inplace=True)
info.drop('lea', axis=1, inplace=True)
info.drop('school_name', axis=1, inplace=True)
info = info.set_index('index')
sage['idx2'] = sage['LEA (District or Charter)'] + sage['School Name']

sage = sage.join(info, on='idx2')
sage.reset_index(inplace=True)
sage.drop('index', axis=1, inplace=True)
sage.drop('idx2', axis=1, inplace=True)
sage.drop('Year', axis=1, inplace=True)
sage.to_csv('sage.csv')
clusters = pd.read_csv('clusters.csv', index_col=0)
alpine = sage[sage['LEA (District or Charter)']=="ALPINE DISTRICT"]
alpine = alpine.join(clusters, on='School Name')
df = load_data('output')
df['sub-links-count'] = df['sub-links'].apply(lambda x: 0 if isinstance(x, float) else len(x) )
df['scc_links-count'] = df['scc_links'].apply(lambda x: 0 if isinstance(x, float) else len(x) )
df['total'] = df['sub-links-count'] + df['scc_links-count']
df = df.sort_values("total", ascending=False)
df['uname'] = df['name'].str.replace('Elementary', 'School').str.upper().str.replace('JUNIOR', 'JR HIGH').str.replace('HIGH HIGH', 'HIGH')

df.to_csv("output.csv")

# df = df.set_index('uname')
# joined = alpine.join(df, on='School Name')
# joined.drop('LEA (District or Charter)', axis=1, inplace=True)
# joined.drop('name', axis=1, inplace=True)
# joined.drop('sub-links', axis=1, inplace=True)
# joined.to_csv('joined.csv')
# df.to_csv("output.csv")
# print df.head()
