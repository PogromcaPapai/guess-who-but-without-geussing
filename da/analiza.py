# %%
import pandas as pd
import sqlite3

osoby = 'Alex, Alfred, Anita, Anne, Bernard, Bill, Charles, Claire, David, Eric, Frans, George, Herman, Joe, Maria, Max, Paul, Peter, Philip, Richard, Robert, Sam, Susan, Tom'.split(', ')

def getdb():
   return sqlite3.connect('baza.sqlite')

df = pd.read_sql('select * from cechy', getdb())

# %%
df.drop(columns=['uwagi','id_cecha'], inplace=True)
df.drop_duplicates(subset=osoby, inplace=True)

df = df[df['nazwa'].apply(lambda x: x not in ['nwm gościu', 'asymetryczność twarzy/miny', 'imię'])]


# %%
t = df.set_index('nazwa').transpose()
df = df[df['nazwa'].apply(lambda x: len(t[x].unique())>1)]

df = df.set_index('nazwa')
# %%

df_imiona = pd.DataFrame(columns=['nazwa']+osoby)

df_imiona = df_imiona.append({'nazwa':'dlugosc'} | {i:len(i) for i in osoby}, ignore_index=True)

df_imiona = df_imiona.append({'nazwa':'imie'} | {j:i for i,j in enumerate(osoby)}, ignore_index=True)

for j in range(1,3):
   l = list({i[:j] for i in osoby})
   df_imiona = df_imiona.append({'nazwa':f'start{j}'} | {i:l.index(i[:j]) for i in osoby}, ignore_index=True)

for j in range(1,4):
   l = list({i[-j:] for i in osoby})
   df_imiona = df_imiona.append({'nazwa':f'end{j}'} | {i:l.index(i[-j:]) for i in osoby}, ignore_index=True)

df_imiona = df_imiona.set_index('nazwa')
df = pd.concat((df, df_imiona))

# %%
pytania = pd.DataFrame(columns=['nazwa', 'wartosc']+osoby)
pytania = pytania.astype({'nazwa':str, 'wartosc':int}|{i:bool for i in osoby})

pytania.convert_dtypes()
for i in df.index:
   for j in df.loc[i].unique():
      d = dict(df.loc[i].apply(lambda x: x==j))
      pytania = pytania.append({'nazwa':i, 'wartosc':j} | d, ignore_index=True)

pytania.drop_duplicates(subset=osoby, inplace=True)
pytania['nazwa'] = pytania['nazwa'].apply(lambda x: x.strip().replace(" ", "_"))

# %%
pytania['Nyes'] = pytania[osoby].sum(axis=1)
pytania['eff'] = pytania['Nyes'].apply(lambda x: min((x,24-x))/max((x,24-x)))
# %%
pytania.to_csv('pytania.csv')
# %%
