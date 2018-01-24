import pandas as pd
import fuzzy


def calc_soundex(val):
    return fuzzy.Soundex(4)(val)

def calc_dmetaphone(val):
    return fuzzy.DMetaphone()(val)

def calc_nysiss(val):
    return fuzzy.nysiis(val)

def calc_score(n):
    sndx = int(calc_soundex(n[0])== calc_soundex(n[1]))
    dmeta = int(calc_dmetaphone(n[0]) == calc_dmetaphone(n[1]))
    nysiis = int(calc_nysiss(n[0]) == calc_nysiss(n[1]))
    return (sndx + dmeta + nysiis)


def calc_match(val):
    sndx = fuzzy.Soundex(4)
    dmeta = fuzzy.DMetaphone()
    return calc_soundex(val), calc_dmetaphone(val), calc_nysiss(val)
    

data = {'name': ['Jonathan', 'Johnathan', 'Joshua', 'Jessica', 'Catherine', 'Katherine', 'Katarina'],
        'bname': ['Johnathan', 'Joshua', 'Jessica', 'Catherine', 'Katherine', 'Katarina','Jonathan']}
df = pd.DataFrame(data, columns = ['name', 'bname'])
print(df)

'''
df['soundex'] = df.apply (lambda row: calc_soundex(row[0])  ,axis=1)
df['nysiss'] = df.apply (lambda row: calc_nysiss(row[0])  ,axis=1)
df['dmetaphone'] = df.apply (lambda row: calc_dmetaphone(row[0])  ,axis=1)
'''
#df['soundex'] = df.apply (lambda row: calc_soundex(row)  ,axis=1)
#df['nysiss'] = df.apply (lambda row: calc_nysiss(row)  ,axis=1)
#df['dmetaphone'] = df.apply (lambda row: calc_dmetaphone(row)  ,axis=1)
df['score'] = df.apply (lambda row: calc_score(row)  ,axis=1)
df['match_0'] = df.apply (lambda row: calc_match(row[0])  ,axis=1)
df['match_1'] = df.apply (lambda row: calc_match(row[0])  ,axis=1)

print(df)



data = {'Address': ['6 Hillside Ave', '6 Hillside Ave', '6 Hillside Ave', '6 Hillside Ave', '6 Hillside Ave'],
        'Owner': ['6 Hill side Av', '6 Hill side Avenue', '6 Hill side Ave.', '6 Hill side Av.', '6 Hill side Avenue.']}
df = pd.DataFrame(data, columns = ['Address', 'Owner'])
df['score'] = df.apply (lambda row: calc_score(row)  ,axis=1)
df['match_0'] = df.apply (lambda row: calc_match(row[0])  ,axis=1)
df['match_1'] = df.apply (lambda row: calc_match(row[0])  ,axis=1)

print(df)

