import pandas as pd
import os
import glob

file_path = "/home/dnguyen/panel/data/input/IMMO_DE_*_07.csv"
name = "VO_IE_2019_07.csv"
input = os.path.join(file_path + name)


#df = pd.read_csv(input, sep=';', encoding='utf-8')


for file in glob.glob(file_path):

    df = pd.read_csv(file, sep=',', encoding='latin-1')

    df.to_csv(file, sep=';', index=False, encoding='utf-8')




# df = pd.read_csv(input, sep=',', encoding ='latin-1', iterator=True, chunksize=100000,engine='python')
# i = 1
# list =[]
# a_dict={}
# for chunk in df:
#     webs=chunk.SITE.value_counts().index.tolist()
#     for web in webs:
#         if web not in list:
#             list.append(web)
#         #outfile = df[df['SITE'] == web]
#         outfile=chunk[chunk['SITE']==web]
#         out_name= "VO_IE_" + str(web).upper() + "_" + str(i) + "_2019_07.csv"
#         #output=os.path.join(file_path + out_name)
#         #outfile.to_csv(output, sep=';', index=False, encoding = 'utf-8')
#         a_dict[out_name]=outfile
#     i += 1
# for web in list:
#     #small_path = "/home/dnguyen/panel/data/input/" + "VO_CA_" + str(web).upper() + "_" + "*07.csv"
#     out_name = "VO_IE_" + str(web).upper() + "_2019_07.csv"
#     out_file = pd.DataFrame()
#     for file in a_dict.keys():
#         if ("_" + str(web).upper() + "_") in file:
#             df = a_dict[file]
#             out_file = pd.concat([df, out_file])
#
#     # for file in glob.glob(small_path):
#     #     df = pd.read_csv(file, sep = ';',encoding='utf-8')
#     #     out_file = pd.concat([df, out_file])
#     out_file.to_csv(os.path.join(file_path + out_name), index=False, encoding='utf-8', sep=';')







# df = pd.read_csv(input, sep=',', encoding ='latin-1',error_bad_lines=False)
# webs=df.SITE.value_counts().index.tolist()
# for web in webs:
#     outfile = df[df['SITE'] == web]
#     out_name= "VO_AU_" + str(web).upper()  + "_2019_06.csv"
#     output=os.path.join(file_path + out_name)
#     outfile.to_csv(output, sep=';', index=False, encoding = 'utf-8')


#
# # #
# columns_lib=['ACHAT_LOC','ADRESSE','AGENCE_ADRESSE', 'AGENCE_CP','AGENCE_ID', 'AGENCE_NOM',
#              'AGENCE_TEL','AGENCE_VILLE','ANNONCE_DATE','ANNONCE_LINK','CATEGORIE','CP','DEPARTEMENT',
#              'ID_CLIENT','M2_TOTALE','M2','MAISON_APT','MINI_SITE_ID','NOM','PAYS_AD','PHOTO',
#              'PIECE','PRIX','PRO_IND','PRO_IND_2','REGION','SELLER_TYPE','SURFACE_TERRAIN','VILLE',
#              'ANNONCE_TEXT','ANNEE','TYPE','SITE','MARQUE','MODELE','CARROSSERIE','OPTIONS','CARBURANT','CYLINDRE',
#              'PORTE','KM','PLACE','PHOTO','LITRE','IMMAT','VN_IND','PROVINCE','TELEPHONE','TELEPHONE_2','TELEPHONE_3','TELEPHONE_4',
#              'GARAGE_ID','GARAGE_NAME','TYPE_2', 'MOIS']
# for file in glob.glob(file_path):
#     df= pd.read_csv(file, sep=',',escapechar=',', encoding='latin-1', iterator=True, chunksize=100000)
#     #df = pd.read_csv(file, sep=';', encoding='utf-8', iterator=True, chunksize=100000)
#     out_file=pd.DataFrame()
#     for chunk in df:
#         new_cols=[]
#         for column in columns_lib:
#             if column in chunk.columns.tolist():
#                 new_cols.append(column)
#         new_df=chunk[new_cols]
#         out_file = pd.concat([new_df, out_file])
#     out_file.to_csv(file, sep=';',encoding='utf-8',index=False)
# # # #
