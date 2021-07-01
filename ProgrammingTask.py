#PUNTO1
#archivo Energy
import pandas as pd 
import numpy as np  

Energy = pd.read_excel(r"C:\Users\Ferreyra\Desktop\PYTHON\COURSERA\JUPITER FILES\assignments\assignment3\assests/Energy Indicators.xls")

Energy = Energy.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
Energy = Energy.rename(columns={"Unnamed: 1":"Country","Unnamed: 3":"Energy Supply","Unnamed: 4":"Energy Supply per Capita","Unnamed: 5":"% Renewable"})

Energy = Energy.drop(columns=["Unnamed: 0","Unnamed: 2"])





#reemplazo los valores de columnas que se pedian 
Energy =  Energy.replace({"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"})

#creo un indice nuevo 
Energy = Energy.reset_index()
Energy = Energy.drop(columns=["index"])

#vacio la energy
Energy = Energy.dropna()



#genero nan values en ... para las columnas de energy suply

njuan = np.empty((5,1))
contador=0
indcont=-1
for x in Energy["Energy Supply"]:
    indcont=indcont+1   
    if x =="...":
     
        contador=contador+1
        njuan[contador-1]= np.nan
        njuan
indcont2=-1
contador2=-1
for x in Energy["Energy Supply"]:
    indcont2=indcont2+1
    if x=="...":
        contador2=contador2+1
        Energy["Energy Supply"].loc[indcont2]=njuan[contador2]



njuan2 = np.empty((5,1))
contadora=0
indconta=-1
for xy in Energy["Energy Supply per Capita"]:
    indconta=indconta+1   
    if xy =="...":
    
        contadora=contadora+1
        njuan2[contadora-1]= np.nan
        njuan2
indcont2a=-1
contador2a=-1
for xy in Energy["Energy Supply per Capita"]:
    indcont2a=indcont2a+1
    if xy=="...":
        contador2a=contador2a+1
        Energy["Energy Supply per Capita"].loc[indcont2a]=njuan2[contador2a]


#paso las unidades
Energy["Energy Supply"]= Energy["Energy Supply"]*1000000


# condicion = energy["Energy Supply"] != "..."
# # energy["Energy Supply"] =  energy["Energy Supply"].where(condicion)



# condicion2 = energy["Energy Supply per Capita"] != "..."
# energy["Energy Supply per Capita"] =  energy["Energy Supply per Capita"].where(condicion2)






#hacer que no aparezcan parentesis ni numeros en la base de datos

Energy["Country"]= Energy["Country"].replace(to_replace="\(.*\)",value="",regex=True)
Energy["Country"]= Energy["Country"].replace(to_replace="Iran ",value="Iran",regex=True)
Energy["Country"]= Energy["Country"].replace(to_replace="Bolivia ",value="Bolivia",regex=True)
Energy["Country"]= Energy["Country"].replace(to_replace="Venezuela ",value="Venezuela",regex=True)
#archivo  GDP


GDP = pd.read_csv(r"C:\Users\Ferreyra\Desktop\PYTHON\COURSERA\JUPITER FILES\assignments\assignment3\assests/world_bank.csv",skiprows=4)

GDP = GDP.replace({"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong",
})

#ver si la saco
GDP = GDP.rename(columns={"Country Name":"Country"})


GDP = GDP[["Country","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015"]]
# GDP.loc[100:140]


#archivo ScimEn

ScimEn = pd.read_excel(r"C:\Users\Ferreyra\Desktop\PYTHON\COURSERA\JUPITER FILES\assignments\assignment3\assests/scimagojr-3.xlsx")

#JOINING

thefinaldf = pd.merge(pd.merge(ScimEn,Energy,on="Country"),GDP,on="Country")
#falta filtrar las filas y columnas para que queden 15,20 y adjudicar todo a una funcion. Con eso terminamos el punto 1


pruebaatierra = thefinaldf

#el caso de iran en 2015
valordeiran2015 = thefinaldf.iloc[12,20]
thefinaldf.iloc[12,20] = "JUAN FERREYRA"

condic = thefinaldf["Rank"]<16
thefinaldf = thefinaldf.where(condic)

thefinaldf = thefinaldf.dropna()

thefinaldf.iloc[12,20] = valordeiran2015

#seteamos el indice country
thefinaldf = thefinaldf.set_index("Country")
thefinaldf




#punto2
a = len(pruebaatierra)
b = len(thefinaldf)
perdida =a-b
perdida 





#punto3
import pandas as pd 
import numpy as np 

nuevo = thefinaldf[["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015"]]
def function(valor):
    variable = valor[["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015"]]
    
    return pd.Series({"Promedio":np.mean(variable)})
#caso de iran
ache = thefinaldf.reset_index()
ache2 = ache.loc[12]
casoiran = ache2.drop(["Country","Rank","Documents","Citable documents","Citations","Self-citations","Citations per document","H index","Energy Supply","Energy Supply per Capita","% Renewable","2015"],axis=0)
casoiran = casoiran.to_numpy()
casoiran = casoiran.mean()

#fin
result = nuevo.apply(function,axis="columns")
result = result.sort_values(by="Promedio",axis=0,ascending=False)
result = result["Promedio"]
result["Iran"]=casoiran
result = result.rename("avgGDP")





#punto4 el reino unido es
primertermino = thefinaldf.loc["United Kingdom"]["2015"] #es 2666333396477.129883
segundotermino = thefinaldf.loc["United Kingdom"]["2006"]#es 2419630700401.72998



resultado = primertermino - segundotermino
resultado







#punto5
a = thefinaldf["Energy Supply per Capita"]

media = np.array(a)
resultado = media.mean()
resultado




#punto6
punto6 = thefinaldf["% Renewable"]
punto6indice = thefinaldf["% Renewable"].index
anterior=0
porcentaje=0
country=0
count=-1
for x in punto6:
    count=count+1
    if x>anterior:
        porcentaje=x
        country = punto6indice[count]
        anterior=x


resultado = (country,porcentaje)

resultado








#punto7

import pandas as pd 
import numpy as np 

new = thefinaldf[["Self-citations","Citations"]]
def functionreplica(valorreplica):
    variablereplica = valorreplica["Self-citations"]
    variablereplica2= valorreplica["Citations"]
    
    return pd.Series({"Proporcion":np.array(variablereplica/variablereplica2)})

result = new.apply(functionreplica,axis="columns")


punto7 =  result["Proporcion"]
punto7indice = result["Proporcion"].index
anterior2=0
porcentaje2=0
country2=0
count2=-1
for x2 in punto7:
    count2=count2+1
    if x2>anterior2:
        porcentaje2=x2
        country2 = punto7indice[count2]
        anterior2=x2
        porcentaje2real = porcentaje2.tolist()


resultadopunto7 = (country2,porcentaje2real)
resultadopunto7





#punto8
import pandas as pd 
import numpy as np 

new8 = thefinaldf[["Energy Supply","Energy Supply per Capita"]]
def functionreplica8(valorreplica8):
    variablereplica8 = valorreplica8["Energy Supply"]
    variablereplica28= valorreplica8["Energy Supply per Capita"]
    
    return pd.Series({"Estimacion Pob":np.array(variablereplica8/variablereplica28)})

result8 = new8.apply(functionreplica8,axis="columns")

punto8 = result8.sort_values(by="Estimacion Pob",axis=0,ascending=False)

res9 = punto8.index.unique()
res9 = res9.to_list()
res9[2]
punto8





#punto9


import matplotlib as plt
import pandas as pd 
import scipy.stats as stats

Top15 =thefinaldf
Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']


    # here is some stub code to actually run the correlation
corr, pval=stats.pearsonr(Top15['Citable docs per Capita'],Top15['Energy Supply per Capita'])








#punto10
mediana = thefinaldf["% Renewable"]
mediana = mediana.sort_values(ascending=True)
mediana = mediana.median()
mediana
punto10 = thefinaldf["% Renewable"]
condicion = thefinaldf["% Renewable"] >=mediana
punto10 = punto10.where(condicion)
punto10 = punto10.fillna(0)
indices = punto10.index.unique()
contju=-1
for x in punto10:
    contju=contju+1
    if x!=0:
        punto10[indices[contju]] =1

punto10 = punto10.rename("HighRenew")
final=0
for x in punto10:
    final=final+1
    punto10[indices[contju]] = float(punto10[indices[contju]])








#punto11
punto11 = thefinaldf
auxiliar = punto11
diccionariojuan = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
auxiliar=auxiliar.reset_index()
punto11 = punto11.reset_index()
auxiliar= punto11.replace(diccionariojuan)
punto11["Continent"] = auxiliar["Country"]




punto11 = punto11.set_index("Continent")
punto11["Estimacion Poblacion"]=punto11["Energy Supply"]/punto11["Energy Supply per Capita"]
punto12 = punto11
punto11["Estimacion Poblacion"] =pd.to_numeric(punto11["Estimacion Poblacion"])
punto11nuevo = punto11.groupby("Continent").agg({"Estimacion Poblacion":(np.size,np.sum,np.mean,np.std)})
punto11nuevo














#punto12
punto12 = punto12.reset_index()
punto12["% Renewable"] = pd.cut(punto12["% Renewable"],bins=5)
punto12 = punto12.groupby(["Continent","% Renewable"]).agg({"Country":np.size})
punto12 = punto12.dropna()
punto12 = punto12["Country"]
punto12









#punto13
import pandas as pd 
import numpy as np 

ayuda = thefinaldf
ayuda['Nuevo'] = ayuda["PopEst"].map('{:,}'.format)

ayudafinal = ayuda["Nuevo"]
ayudafinal




