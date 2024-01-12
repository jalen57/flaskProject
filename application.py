from flask import Flask
from flask import render_template, jsonify, make_response
import urllib.request, json
import urllib.error
import pandas as pd
import pymysql


application = Flask(__name__)


  

@application.route('/data_json')
def data_json():
    db = pymysql.connect(host='database-6.crga42aec7fl.us-east-1.rds.amazonaws.com', user="admin",password="Jsoccer5",port=3306, database="database6")
    query = "SELECT * FROM data_bulk"
    try: 
        df = pd.read_sql(query, db)
        db.close()
        data_bulk = df.to_dict('records')
        table_dict = []
        for s in data_bulk:
            temp_dict = {
                'id': s['id'],
                'away': s['away'],
                'a_score': s['a_score'],
                'home': s['home'],
                'h_score': s['h_score'],
                'time': s['quarter'],
                'a_to': s['a_to'],
                'h_to': s['h_to'],
                'a_bonus': s['h_bonus'],
                'h_bonus': s['a_bonus'],
                'clock': s['g_clock'],
                'state': s['action'],
                'desc': s['sub'],
                'detail': s['desc'],
                'qual': s['quals'] 
            }
            table_dict.append(temp_dict)
        return(jsonify(table_dict))
    except:
         return(jsonify)








@application.route('/')
def index():
   dummy_data = data_json()
   response = make_response(render_template('index.html', matches=dummy_data.json))
   response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate, public, max-age=0"
   response.headers["Pragma"] = "no-cache"
   response.headers["Expires"] = "0"
   return(response)




if __name__ == "__main__":
        application.run()