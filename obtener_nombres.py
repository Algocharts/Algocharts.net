import pickle
import requests
import json
import mysql.connector


dbpares = mysql.connector.connect(
	host="localhost",
	user="pablo",
	password="test1",
	database="pares"
	)

with open("lista_pares", "rb") as fp:
    lista_pares = pickle.load(fp)

cursor_pares = dbpares.cursor()
for elemento in lista_pares:
	for par in elemento:
		if par != 0:
			respuesta_algoexplorer = requests.get('https://algoexplorerapi.io/idx2/v2/assets?asset-id=' + str(par))
			respuesta_algoexplorer_p1 = respuesta_algoexplorer.text
			respuesta_algoexplorer_p2 = json.loads(respuesta_algoexplorer_p1)
			try:
				nombre = respuesta_algoexplorer_p2['assets'][0]['params']['name']
				sql = "INSERT IGNORE INTO nombres (asset_id, nombre) VALUES (%s, %s)"
				valores = (par, nombre)
				cursor_pares.execute(sql, valores)
				dbpares.commit()
			except:
				pass
for elemento in lista_pares:
        sql = ("SELECT * FROM pares WHERE assetin = %s AND assetout= %s")
        valores = (int(elemento[0]), int(elemento[1]))
        cursor_pares.execute(sql, valores)
        cursor_pares.fetchall()
        if not cursor_pares.rowcount:
                try:
                        sqln = ("SELECT nombre FROM nombres WHERE asset_id = %s")
                        valor = elemento[1]
                        cursor_pares.execute(sqln, (valor,))
                        resultado = cursor_pares.fetchone()
                        sql = ("INSERT INTO pares (assetin, assetout, nombre) VALUES (%s, %s, %s)")
                        valores = (elemento[0], elemento[1], resultado[0])
                        cursor_pares.execute(sql, valores)
                        dbpares.commit()
                except:
                        pass
for elemento in lista_pares:
        sql = ("SELECT * FROM pares WHERE assetin = %s AND assetout= %s")
        valores = (int(elemento[1]), int(elemento[0]))
        cursor_pares.execute(sql, valores)
        cursor_pares.fetchall()
        if not cursor_pares.rowcount:
                try:
                        sqln = ("SELECT nombre FROM nombres WHERE asset_id = %s")
                        valor = elemento[0]
                        cursor_pares.execute(sqln, (valor,))
                        resultado = cursor_pares.fetchone()
                        sql = ("INSERT INTO pares (assetin, assetout, nombre) VALUES (%s, %s, %s)")
                        valores = (elemento[1], elemento[0], resultado[0])
                        cursor_pares.execute(sql, valores)
                        dbpares.commit()
                except:
                        pass

cursor_pares.close()
dbpares.close()
