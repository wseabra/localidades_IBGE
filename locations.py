import requests
import sqlite3

conn = sqlite3.connect('ibge.db')


conn.execute('''CREATE TABLE ESTADO
                (ID  INT,
                NOME STRING);''')
  
conn.execute('''CREATE TABLE MUNICIPIO
                (ESTADO INT,
                COD     INT,
                NOME    STRING,
                FOREIGN KEY(ESTADO) REFERENCES ESTADO(ID));''')
r = requests.get(url='https://servicodados.ibge.gov.br/api/v1/localidades/estados')
for estado in r.json():
    UF_id = estado['id']
    UF_nome = estado['nome']
    conn.execute("INSERT INTO ESTADO (ID,NOME) \
      VALUES ("+str(UF_id)+",\""+UF_nome+"\")")
    g = requests.get(url='http://servicodados.ibge.gov.br/api/v1/localidades/estados/'+str(estado['id'])+'/municipios')
    for municipio in g.json():
        MU_id = municipio['id']
        MU_nome = municipio['nome']
        conn.execute("INSERT INTO MUNICIPIO (ESTADO,COD,NOME) \
            VALUES ("+str(UF_id)+","+str(MU_id)+",\""+MU_nome+"\")")

conn.commit()
conn.close()