import pandas as pd
import fuzzy


data = {'name': ['Jonathan', 'Johnathan', 'Joshua', 'Jessica', 'Catherine', 'Katherine', 'Katarina'],
        'bname': ['Johnathan', 'Joshua', 'Jessica', 'Catherine', 'Katherine', 'Katarina','Jonathan']}
df = pd.DataFrame(data, columns = ['name', 'bname'])
print(df)

def calc_soundex(n):
    sndx = fuzzy.Soundex(4)
    return sndx(n[0]) == sndx(n[1])

def calc_dmetaphone(n):
    dmeta = fuzzy.DMetaphone()
    return dmeta(n[0]) == dmeta(n[1])

def calc_nysiss(n):
    return fuzzy.nysiis(n[0]) == fuzzy.nysiis(n[1])

def calc_score(n):
    sndx = int(calc_soundex(n))
    dmeta = int(calc_dmetaphone(n))
    nysiis = int(calc_nysiss(n))
    return sndx+dmeta+nysiis

'''
df['soundex'] = df.apply (lambda row: calc_soundex(row[0])  ,axis=1)
df['nysiss'] = df.apply (lambda row: calc_nysiss(row[0])  ,axis=1)
df['dmetaphone'] = df.apply (lambda row: calc_dmetaphone(row[0])  ,axis=1)
'''
df['soundex'] = df.apply (lambda row: calc_soundex(row)  ,axis=1)
df['nysiss'] = df.apply (lambda row: calc_nysiss(row)  ,axis=1)
df['dmetaphone'] = df.apply (lambda row: calc_dmetaphone(row)  ,axis=1)
df['score'] = df.apply (lambda row: calc_score(row)  ,axis=1)

print(df)



