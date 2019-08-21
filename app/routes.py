from flask import Flask, render_template, request
import sqlite3
import requests

 
app = Flask(__name__)  

def getEstadoId(estado):
  estado_ret = None
  conn = sqlite3.connect('../ibge.db')
  estado_cursor = conn.execute('SELECT ID FROM ESTADO WHERE NOME = \'' + estado+'\'')
  for i in estado_cursor:
    estado_ret = i[0]
  conn.close()
  if estado_ret == None:
    return None
  return estado_ret

def getMunicipioId(municipio, estado_id):
  municipio_ret = None
  conn = sqlite3.connect('../ibge.db')
  municipio_cursor = conn.execute('SELECT COD FROM MUNICIPIO WHERE ESTADO = '+str(estado_id)+' AND NOME = \''+municipio+'\'')
  for i in municipio_cursor:
    municipio_ret = i[0]
  conn.close()
  if municipio_ret == None:
    return None
  return municipio_ret

@app.route('/')
def home():
  return render_template('bolsa-familia.html')

@app.route('/consulta',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      print(result)
      ano = result['Ano']
      mes = result['Mes']
      estado = result['Estado']
      municipio = result['Municipio']
      print(ano + ' ' + mes + ' ' + estado + ' ' + municipio)

      estado_id = getEstadoId(estado)
      
      municipio_id = getMunicipioId(municipio, estado_id)

      r = requests.get(url='http://www.transparencia.gov.br/api-de-dados/bolsa-familia-por-municipio?mesAno='+str(ano)+str(mes)+'&codigoIbge='+str(municipio_id)+'&pagina=1')

      return render_template("result.html",result = r)
 
if __name__ == '__main__':
  app.run(debug=True)
