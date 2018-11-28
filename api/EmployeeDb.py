from sqlalchemy import create_engine
import time
import logging as log
import status
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


db_connect  = create_engine(config['database']['db1'])
db_connect2 = create_engine(config['database']['db2'])

def compare_employees(q1,q2):
    """
    Compare both database query
    :return:
    """
    result = ""


    if q1['data'][0]['EmployeeId'] == q2['data'][0]['EmployeeId']:
        #print("Same d1 id: {0}".format(q1['data']))
        result = q1['data']

    return result



def find_both_db_employee(employee_id):
    result = ""

    r1 = query_employee_by_id(db_connect, employee_id)
    r2 = query_employee_by_id(db_connect2, employee_id)

    err1 = r1['error']
    err2 = r2['error']

    # both db queries are giving result
    if err1 == err2 == 0:
        res = compare_employees(r1, r2)
        result = {'error': status.HTTP_200_OK, 'msg': res, }

    # both db queries are not found
    elif err1 == err2 == 1:
        result = {'error': status.HTTP_404_NOT_FOUND,'msg':[r1['msg'], r2['msg']],}

    # cant't performe any db queries
    elif err1 == err2 == -1:
        result = {'error': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': [r1['msg'], r2['msg']], }

    # found one query
    elif err1 == 0 and err2 == 1:
        result = {'error': status.HTTP_200_OK, 'msg': r1['data'], }
    elif err2 == 0 and err1 == 1:
        result = {'error': status.HTTP_200_OK, 'msg': r2['data'], }

    # found one query other service unavailable
    elif err1 == 0 and err2 == -1:
        result = {'error': status.HTTP_206_PARTIAL_CONTENT, 'msg': [r1['data'],r2['msg']], }
    elif err2 == 0 and err1 == -1:
        result = {'error': status.HTTP_206_PARTIAL_CONTENT, 'msg': [r2['data'],r1['msg']], }

    # not found, other service unavailable
    elif err1 == 1 and err2 == -1:
        result = {'error': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': r1['msg'], }
    elif err2 == 1 and err1 == -1:
        result = {'error': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': r2['msg'], }

    else:
        log.error("Some unexpected data-query error")

    return result



def query_employee_by_id(db,employee_id):
    """
    Query Employee from database
    :param db:
    :param employee_lname:
    :param sleep:
    :return:
    """
    t = time.time()
    result = {'error':-1}

    try:
        conn   = db.connect()
        query  = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        #query = conn.execute("select * from employees where LastName LIKE '{0}%' ".format(str(employee_lname)))

        res = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        if len(res) > 0:
            result = {'error':0,'data':res}
            log.info(result)
        else:
            err_msg = str(db) + ": Query not found"
            result = {'error':1,'msg':err_msg}
            log.warning(result['msg']+" "+str(db))

    except Exception:
        err_msg = str(db) +": Unable to fetch items"
        log.error(err_msg)
        result = {'msg':err_msg,'error':-1}
    finally:
        conn.close()

    #return jsonify(result)
    return result


def insert_employee(inp_list):
    """
    Insert new employee into database
    :return:
    """

    try:
        conn = db_connect.connect()

        insert_data = """
        insert into employees(FirstName,LastName,Email,BirthDate) 
        values('{0}','{1}','{2}','{3}')
        """.format(inp_list['FirstName'],
                   inp_list['LastName'],
                   inp_list['Email'],
                   inp_list['BirthDate']
                   )

        conn.execute(insert_data)
        log.info("new entry inserted")

    except:
        result = {'error': 1, "msg": "Database error"}
        log.error(result)


if __name__ == "__main__":

    #res = find_both_db_employee(20)
    id = 20
    r1 = query_employee_by_id(db_connect, id, 0)
    r2 = query_employee_by_id(db_connect2, id, 0)

    print("r1: {0}".format(r1))
    print("r2: {0}".format(r2))
