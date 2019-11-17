import mysql

from app import applesinglefrom
from db_config import mysql
from flask import Flask, jsonify,
from flask_restful import Api, Resource, reqparse
from datetime import datetime


# Temperature API Endpoint
class Temperature(Resource):
    def get(self, sensor_id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            sql = "SELECT * FROM temperature WHERE sensor_id=%s".format(sensor_id)
            cursor.execute(sql)
            row = cursor.fetchall()
            response = jsonify(row)
            response.status_code = 200
            return response

        except Exception as e:
            return e, 404

        finally:
            cursor.close()
            conn.close()

    def post(self, sensor_id):
        parser = reqparse.RequestParser()
        parser.add_argument("temperature")
        args = parser.parse_args()

        if args["temperature"] == "":
            return "Enter Valid Temperature Value", 406

        # Get Current Time
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            sql = "INSERT INTO farm_sensors.temperature (sensor_id, timestamp, temperature)" \
                  "VALUES ({},{},{})".format(sensor_id, current_time, args['temperature'])
            cursor.execute(sql)
            conn.commit()
            message = "===> Added Temperature Record \t Sensor ID: {} \t Timestamp: {} \t" \
                      "Temperature: {}".format(sensor_id, current_time, args['temperature'])
            print(message)
            return 201

        except Exception as e:
            return e, 404

        finally:
            cursor.close()
            conn.close()


api = APi(app)
# Add API endpoints
api.add_resource(Temperature, "/temperature/<int:sensor_id>")

if __name__ == "__main__":
    app.run(debug=True, port=8080)











