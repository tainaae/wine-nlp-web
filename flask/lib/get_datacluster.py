# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine

host='127.0.0.1' 
user='pfg2' 
password='Pfg2mysql*'
db='wine'

engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db)


clusters_df = pd.read_sql_table('clusters_df', con=engine, schema=None, index_col=None, coerce_float=False, parse_dates=None, columns=None, chunksize=None)


def get_top4(num_cluster): #recebe o cluster da função predict
    searchfor = num_cluster #vai pegar resultado do predict a entrada do usuário
    clusters_select = clusters_df.loc[clusters_df['cluster'] == searchfor]
    high_score_cluster_per_country = clusters_select.sort_values('points', ascending=False).drop_duplicates(['country'])
    clusters_df_top4_userselect = high_score_cluster_per_country.nlargest(4, ['points'])
    return clusters_df_top4_userselect

#só para montar dicionário dos clusters
#words_to_analyze = info_clusters.apply(pd.value_counts).count(axis=1)