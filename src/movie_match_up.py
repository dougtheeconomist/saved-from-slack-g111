import numpy as np
import pandas as pd
import re
from fuzzywuzzy import process
from multiprocessing import Pool, cpu_count
#Nik and Darrel's code for translating movie titles that were ALMOST right

#Here's what we used to get about 3440-ish of the movies to match
#Used One Powerful AWS computer with 8 processors and took 10-ish minutes. (C52X Large)
pd.options.display.max_columns = None
trainingdf = pd.read_csv('data/training.csv')
moviedf = pd.read_csv('moviedf.csv')
userdf = pd.read_csv('userdf.csv')
metadf = pd.read_csv('data/movies_metadata.csv')
def extract_orig(string):
    regex = r"\((.+)\)"
    matches = re.search(regex,str(string))
    if matches:
        return str(matches.group(1))
    else:
        return reverse_the(string)
def extract_title(string):
    regex = r"(.+)\("
    matches = re.search(regex,str(string))
    if matches:
        return str(matches.group(1))
    else:
        return string
def reverse_the(string):
    regex = r"\, \S+$"
    matches = re.search(regex,str(string))
    if matches:
        pass
    else:
        return string
    string2 = string.rsplit(', ',1)
    return " ".join([string2[-1],string2[0]])
moviedf['title'].iloc[72] = 'Misérables, Les (1995)'
moviedf['title'].iloc[566] = 'Slingshot, The (Kådisbellan ) (1993)'
moviedf['title'].iloc[578] = 'Metisse (Café au Lait) (1993)'
moviedf['title'].iloc[643] = 'Cold Fever (Á köldum klaka) (1994)'
moviedf['title'].iloc[1101] = 'Eighth Day, The (Le Huitième jour ) (1996)'
moviedf['title'].iloc[1133] = 'JLG/JLG - autoportrait de décembre (1994)'
moviedf['title'].iloc[1160] = 'Double Life of Veronique, The (La Double Vie de Véronique) (1991)'
moviedf['title'].iloc[1193] = 'Wings of Desire (Der Himmel über Berlin) (1987)'
moviedf['title'].iloc[1300] = 'Alien³ (1992)'
moviedf['title'].iloc[1343] = 'Zero Kelvin (Kjærlighetens kjøtere) (1995)'
moviedf['title'].iloc[1383] = 'Cérémonie, La (1995)'
moviedf['title'].iloc[1532] = 'Contempt (Le Mépris) (1963)'
moviedf['title'].iloc[1618] = 'Nénette et Boni (1996)'
moviedf['title'].iloc[1690] = 'Midaq Alley (Callejón de los milagros, El) (1995)'
moviedf['title'].iloc[1735] = 'Callejón de los milagros, El (1995)'
moviedf['title'].iloc[1804] = 'Misérables, Les (1998)'
moviedf['title'].iloc[1864] = 'Life of Émile Zola, The (1937)'
moviedf['title'].iloc[1994] = 'Seventh Heaven (Le Septième ciel) (1997)'
moviedf['title'].iloc[2062] = 'Autumn Sonata (Höstsonaten ) (1978)'
moviedf['title'].iloc[2106] = 'Déjà Vu (1997)'
moviedf['title'].iloc[2255] = 'Life Is Beautiful (La Vita è bella) (1997)'
moviedf['title'].iloc[2411] = 'Dry Cleaning (Nettoyage à sec) (1997)'
moviedf['title'].iloc[2414] = 'Day of the Beast, The (El Día de la bestia) (1995)'
moviedf['title'].iloc[2426] = 'Fantastic Planet, The (La Planète sauvage) (1973)'
moviedf['title'].iloc[2475] = 'School of Flesh, The (L\' École de la chair) (1998)'
moviedf['title'].iloc[2506] = 'Dreamlife of Angels, The (La Vie rêvée des anges) (1998)'
moviedf['title'].iloc[2516] = 'Lovers of the Arctic Circle, The (Los Amantes del Círculo Polar) (1998)'
moviedf['title'].iloc[2522] = 'Jeanne and the Perfect Guy (Jeanne et le garçon formidable) (1998)'
moviedf['title'].iloc[2534] = 'Nô (1998)'
moviedf['title'].iloc[2627] = 'Dinner Game, The (Le Dîner de cons) (1998)'
moviedf['title'].iloc[2636] = 'Late August, Early September (Fin août, début septembre) (1998)'
moviedf['title'].iloc[2673] = 'Ménage (Tenue de soirée) (1986)'
moviedf['title'].iloc[2691] = 'Gambler, The (A Játékos) (1997)'
moviedf['title'].iloc[2800] = 'Separation, The (La Séparation) (1994)'
moviedf['title'].iloc[2985] = 'Pokémon: The First Movie (1998)'
moviedf['title'].iloc[3158] = 'Not Love, Just Frenzy (Más que amor, frenesí) (1996)'
moviedf['title'].iloc[3168] = 'Kestrel\'s Eye (Falkens öga) (1998)'
moviedf['title'].iloc[3172] = 'Cup, The (Phörpa) (1999)'
moviedf['title'].iloc[3197] = 'Man Bites Dog (C\'est arrivé près de chez vous) (1992)'
moviedf['title'].iloc[3300] = 'Any Number Can Win (Mélodie en sous-sol ) (1963)'
moviedf['title'].iloc[3347] = 'Trial, The (Le Procès) (1963)'
moviedf['title'].iloc[3463] = 'Freedom for Us (À nous la liberté ) (1931)'
moviedf['title'].iloc[3523] = 'Time Masters (Les Maîtres du Temps) (1982)'
moviedf['title'].iloc[3576] = 'Cleo From 5 to 7 (Cléo de 5 à 7) (1962)'
moviedf['title'].iloc[3583] = 'City of the Living Dead (Paura nella città dei morti viventi) (1980)'
moviedf['title'].iloc[3680] = 'Time Regained (Le Temps Retrouvé) (1999)'
moviedf['title'].iloc[3730] = 'Pokémon the Movie 2000 (2000)'
moviedf['title'].iloc[3747] = 'Other Side of Sunday, The (Søndagsengler) (1996)'
moviedf['title'].iloc[3775] = 'And God Created Woman (Et Dieu… créa la femme) (1956)'
moviedf['title'].iloc[3784] = 'Aimée & Jaguar (1999)'
moviedf['year'] = moviedf['title'].apply(lambda x: "".join([x[-5],x[-4],x[-3],x[-2]]))
moviedf['year'] = pd.to_datetime(moviedf['year']).dt.year
moviedf['titleshort'] = moviedf['title'].apply(lambda x: x[:-7])
moviedf['fulltitle'] = moviedf['title']
moviedf['original_title'] = moviedf['titleshort'].apply(lambda x: extract_orig(x))
moviedf['title'] = moviedf['titleshort'].apply(lambda x: reverse_the(extract_title(x).strip()))
metadf = metadf.drop([19729,19730,29502,29503,35587,35586,45461],axis=0)
metadf['year'] = pd.to_datetime(metadf['release_date']).dt.year
metadf['year'] = metadf['year'].astype(float)
moviedf['year'] = moviedf['year'].astype(float)
moviedf['AUGH'] = moviedf.apply(lambda x: " ".join([x.title,str(x.year)]),axis=1).astype(str)
metadf['AUGH'] = metadf.apply(lambda x: " ".join([x.title,str(x.year)]),axis=1).astype(str)
choices = metadf['AUGH'].values.tolist()
truemoviedf = pd.merge(moviedf, metadf,how='left',left_on=['AUGH'],right_on=['AUGH'])
indexlist = truemoviedf[truemoviedf['popularity'].isna()].index.tolist()
valuelist = moviedf['AUGH'].iloc[indexlist].to_list()
def get_match(a):
    return process.extractOne(a, choices)[0]
with Pool(cpu_count()) as p:
    replacementlist = p.map(get_match, valuelist)
for i,j in zip(indexlist,replacementlist):
    moviedf['AUGH'].iloc[i] = j
true_true_moviedf = pd.merge(moviedf,metadf,how='left',left_on=['AUGH'],right_on=['AUGH'])
true_true_moviedf.to_csv('MetaMovie.csv', index=False)