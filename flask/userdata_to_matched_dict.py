# -*- coding: utf-8 -*-
import pandas as pd


wine_dict = {}
####tipo de vinho de acordo com o nível de taninos####
#muito tanico
wine_dict['tannin'] = ['tannic', 'tannin', 'herbal', 'oak', 'firm']
#acido
wine_dict['acid'] = ['acid', 'crisp', 'tart', 'citrus', 'lemon', 'lime']
#mineral
wine_dict['mineral'] = ['stainless', 'miner']
#frutado
wine_dict['fruit'] = ['fruiti', 'fruit']
####tipo de vinho de acordo com a cor####
#tinto
wine_dict['red'] = ['red', 'dark', 'black', 'soft', 'blend', 'cabernet', 'franc', 'malbec', 'merlot', 'pinot', 'sirah', 'syrah', 'cinsault', 'noir', 'petit', 'verdot']
#branco
wine_dict['white'] = ['white', 'soft', 'blend', 'chardonnay', 'grenach', 'sauvignon']
#rose
wine_dict['rose'] = ['red', 'pinot', 'sirah', 'syrah', 'cinsault', 'noir']
####tipo de vinho de acordo com o teor de acuçar####
#suave
wine_dict['sweet'] = ['candi', 'licoric', 'sweet', 'ripe']
#seco
wine_dict['dry'] = ['dri']
####tipo de vinho de acordo com o teor alcoolico####
#leve
wine_dict['light'] = ['ripe']
#medio
wine_dict['medium'] = ['medium']
#alto
wine_dict['high'] = ['licoric','dens', 'rich']
####tipo de vinho de acordo com as frutas####
#frutas vermelhas e negras
wine_dict['dark'] = ['dark', 'blackberri', 'berri', 'cranberri', 'raspberri', 'currant', 'plum', 'cherri']
#frutas amarelas e brancas
wine_dict['yellow'] = ['appl', 'peach', 'pear', 'pineappl', 'green', 'vanilla', 'apricot']
####tipo de vinho de acordo com o potencial de guarda####
#vinho para beber jovem
wine_dict['young'] = ['new', 'soft']
#vinho para guarda
wine_dict['old'] = ['age', 'barrel', 'oak', 'leather', 'spice', 'toast']
####tipo de vinho de acordo com a complexidade####
#complexo
wine_dict['complex'] = ['bodi', 'structur', 'oak', 'blend', 'butter', 'spice', 'silki']
#medio
wine_dict['intermediary'] = ['medium']
#simples
wine_dict['simple'] = ['simpl', 'light', 'fresh', 'soft', 'cinsault']


def create_nlp_string(data):
    user_dict_status =  data
    user_dict_list = [k for k in user_dict_status if user_dict_status.get(k) is True]
    
    string_list = []
    
    for item in user_dict_list:
        for s in wine_dict.get(item):
            string_list.append(s)
   
    # unique items
    string_list = list(set(string_list))
    
    return_string = ''
    
    for s in string_list:
        return_string = return_string + '{} '.format(s)
    
    return return_string


#print(create_nlp_string(data))
     

        
    
    
    
    
