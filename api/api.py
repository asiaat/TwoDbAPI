from flask import Flask
from flask_restful import Api, reqparse, Resource
import status
import logging as log
from EmployeeDb import find_both_db_employee, insert_employee
import configparser


class PostEmployee(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('LastName',     type=str, required=True, help='LastName cannot be blank!')
        parser.add_argument('FirstName',    type=str, required=True, help='FirstName cannot be blank!')
        parser.add_argument('BirthDate',    type=str, required=True, help='BirthDate cannot be blank!')
        parser.add_argument('Email',        type=str, required=True, help='Email cannot be blank!')
        args = parser.parse_args()

        employee_insert = {
            'LastName':     args['LastName'],
            'FirstName':    args['FirstName'],
            'BirthDate':    args['BirthDate'],
            'Email':        args['Email'],
        }


        insert_employee(employee_insert)

        return '', status.HTTP_201_CREATED


class Employee(Resource):


    def get(self, id):

        result = ""

        try:
            res    = find_both_db_employee(id)
            result = res['msg'], res['error']
            log.info(result)

        except:
            msg = "Not correct return of find_both_db_employee"
            log.warning(msg)

        return result



app = Flask(__name__)
api = Api(app)

api.add_resource(Employee,      '/api/employee/<int:id>')
api.add_resource(PostEmployee,  '/api/employee/')


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read("config.ini")

    log.basicConfig(filename=config['log']['file'], level=log.DEBUG)

    app.run(debug   = bool(config['flask']['debug']),
            host    = config['flask']['host'],
            port    = int(config['flask']['port'])
            )

    log.info("Flask Restful serevr is started ...")

