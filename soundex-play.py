import pandas as pd
import fuzzy


data = {'name': ['Jonathan', 'Johnathan', 'Joshua', 'Jessica', 'Catherine', 'Katherine', 'Katarina']}
df = pd.DataFrame(data, columns = ['name'])
print(df)

def calc_soundex(n):
    return fuzzy.Soundex(4)(n)

def calc_dmetaphone(n):
    return fuzzy.DMetaphone()(n)

def calc_nysiss(n):
    return fuzzy.nysiis(n)


df['soundex'] = df.apply (lambda row: soundex(row.name),axis=1)
print(df)



