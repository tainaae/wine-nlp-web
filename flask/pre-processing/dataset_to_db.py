# -*- coding: utf-8 -*-
import pandas as pd

from sqlalchemy import create_engine

#tratamento de dataset
######################################################
data = pd.read_csv('wine_description.csv', sep=',', index_col=0, low_memory=False)

data = data.drop(columns=["designation", "region_2", "Unnamed: 12", "Unnamed: 13", "Unnamed: 14", "Unnamed: 15"])

#remoção de rows com descrição e título duplicados
data = data.drop_duplicates('description')
data = data.drop_duplicates('title')
#remoção de rows com elementos null
data = data.dropna()

#agrupa rows do dataframe por variety e considera os com mais de 1000 ocorrencias
variety_df = data.groupby('variety').filter(lambda x: len(x) > 1000)
variety_df = variety_df.reset_index(drop=True)
#variety_df.loc[variety_df['country'] == 'US', 'country'] = 'United States of America'

varieties = variety_df['variety'].value_counts().index.tolist()
countries = variety_df['country'].value_counts().index.tolist()

#envia dataset para o banco de dados mysql
######################################################
host='127.0.0.1' 
user='pfg2' 
password='Pfg2mysql*'
db='wine'

engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db, encoding='utf8')


#sql = "CREATE TABLE variety_df(
#            id INT NOT NULL,
#            country VARCHAR(50) NOT NULL,
#            description TEXT NOT NULL,
#            points INT NOT NULL,
#            price DECIMAL(10,2) NOT NULL,
#            province TEXT NOT NULL,
#            region_1 TEXT NOT NULL,
#            title TEXT NOT NULL,
#            variety TEXT NOT NULL,
#            winery TEXT NOT NULL,
#            PRIMARY KEY (id) 
#        )
#        CHARACTER SET utf8 COLLATE utf8_unicode_ci;
#        charset utf8;"
#
#
#pd.read_sql_query(sql, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)


variety_df.to_sql(name='variety_df', con=engine, if_exists = 'replace', index=True, index_label='id')