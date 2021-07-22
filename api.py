from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify


def query_to_json(query):
    result = {'data': [dict(zip(tuple(query.keys()), i))
                       for i in query.cursor]}
    return jsonify(result)


engine = 'mysql+pymysql://root@127.0.0.1/igmava'
db_connect = create_engine(engine)
app = Flask(__name__)
api = Api(app)


@app.route('/reservas_mes/<y1>/<y2>', methods=['GET'])
def reservas_mes(y1, y2):
    conn = db_connect.connect()
    q = "select Year(Check_in) as year, Month(Check_in) as month, \
                count(*) as count from Reserva \
         where Year(Check_in) >= '{}' and Year(Check_in) <= '{}' \
         group by Year(Check_in), Month(Check_in)".format(y1, y2)
    query = conn.execute(q)
    return query_to_json(query)


@app.route('/reservas_region', methods=['GET'])
def reservas_region():
    conn = db_connect.connect()
    q = "SELECT Procedencia, COUNT(*) as count FROM Cliente \
         GROUP BY Procedencia;"
    query = conn.execute(q)
    return query_to_json(query)


if __name__ == '__main__':
    app.run(port='8007')
