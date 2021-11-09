#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://zw2771:1787@35.196.73.133/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")


# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
    """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/index')
def index():
    """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

    # DEBUG: this is debugging code to see what request looks like
    # print(request.args)

    #
    # example of a database query
    #
    cursor = g.conn.execute("SELECT name FROM test")
    names = []
    for result in cursor:
        names.append(result['name'])  # can also be accessed using result[0]
    cursor.close()

    #
    # Flask uses Jinja templates, which is an extension to HTML where you can
    # pass data to a template and dynamically generate HTML based on the data
    # (you can think of it as simple PHP)
    # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
    #
    # You can see an example template in templates/index.html
    #
    # context are the variables that are passed to the template.
    # for example, "data" key in the context variable defined below will be
    # accessible as a variable in index.html:
    #
    #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
    #     <div>{{data}}</div>
    #
    #     # creates a <div> tag for each element in data
    #     # will print:
    #     #
    #     #   <div>grace hopper</div>
    #     #   <div>alan turing</div>
    #     #   <div>ada lovelace</div>
    #     #
    #     {% for n in data %}
    #     <div>{{n}}</div>
    #     {% endfor %}
    #
    context = dict(data=names)

    #
    # render_template looks in the templates/ folder for files.
    # for example, the below file reads template/index.html
    #
    return render_template("index.html", **context)


#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
    return render_template("another.html")


@app.route("/top-min-chart")
def top_min_chart():
    cursor = g.conn.execute("SELECT zip_code, avg(CAST(evaluation_price_per_sqft as decimal(9,2))) "
                            "FROM address, building where address.street = building.street "
                            "group by zip_code order by avg(CAST(evaluation_price_per_sqft as decimal(9,2))) LIMIT 6")
    zip_codes, prices = [], []
    for result in cursor:
        zip_codes.append(result[0])  # can also be accessed using result[0]
        prices.append(result[1])
    cursor.close()

    return render_template("top_min_chart.html", zipcode=zip_codes, price=prices)


@app.route("/top-max-chart")
def top_max_chart():
    cursor = g.conn.execute("SELECT zip_code, avg(CAST(evaluation_price_per_sqft as decimal(9,2))) "
                            "FROM address, building where address.street = building.street "
                            "group by zip_code order by avg(CAST(evaluation_price_per_sqft as decimal(9,2))) DESC LIMIT 6")
    zip_codes, prices = [], []
    for result in cursor:
        zip_codes.append(result[0])  # can also be accessed using result[0]
        prices.append(result[1])
    cursor.close()

    return render_template("top_max_chart.html", zipcode=zip_codes, price=prices)

@app.route('/agency')
def agency():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  # print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()


# Login
@app.route('/checkUser', methods=['POST'])
def login():
    ssn = request.form['ssn']
    identity = request.form['identity']

    if identity == "Tenant":
        cursor = g.conn.execute('SELECT ssn FROM tenant')
    elif identity == "Landlord":
        cursor = g.conn.execute('SELECT ssn FROM landlord')
    else:
        cursor = g.conn.execute('SELECT ssn FROM agency')

    for result in cursor:
        if result[0] == ssn:
            return redirect('/' + identity + '/' + ssn)

    return redirect('/')


@app.route('/pay', methods=['POST'])
def makePayment():
    bill_id = request.form['unpaid']
    cursor = g.conn.execute("SELECT pay_from,paid FROM bill "
                            "WHERE bill.bill_id='" + str(bill_id) + "'")
    for result in cursor:
        # update information about bill payment
        g.conn.execute("UPDATE bill SET paid=true "
                       "WHERE bill_id='" + str(bill_id) + "'")
        return redirect('/Tenant/' + result[0])


@app.route('/initialize', methods=['POST'])
def initializePayment():
    year = request.form['year']
    month = request.form['month']
    amount = request.form['amount']
    contract_id = request.form['contract']

    cursor = g.conn.execute("SELECT sign_by_landlord FROM contract "
                            "WHERE contract.contract_id='" + str(contract_id) + "'")
    for result in cursor:
        ssn = result[0]

    # check validity
    if year.isdigit() == false or month.isdigit() == false or amount.isdigit() == false:
        return redirect('/Landlord/' + ssn)

    if int(month) < 1 or int(month) > 12 or int(amount) <= 0:
        return redirect('/Landlord/' + ssn)

    date = year + '-' + month + '-' + '01'
    cursor=g.conn.execute("SELECT COUNT(*) FROM bill")
    for result in cursor:
        numberOfBills=result[0]
    cursor = g.conn.execute("SELECT sign_by_tenant FROM contract"
                            " WHERE contract.contract_id="+"'"+contract_id+"'")
    for result in cursor:
        payfrom=result[0]

    bill_id=100000+numberOfBills
    data={"bill_id":bill_id,"amount":amount,"date":date,"ssn":ssn,"payfrom":payfrom}
    statement=text("INSERT INTO bill VALUES (:bill_id,:amount,:date,:ssn,:payfrom,false)")
    g.conn.execute(statement,{"bill_id":bill_id,"amount":amount,"date":date,"ssn":ssn,"payfrom":payfrom})

    return redirect('/Landlord/' + ssn)


@app.route('/<identity>/<ssn>')
def users(identity, ssn):
    user_info = []
    user_info.append(identity)
    user_info.append(ssn)
    if identity == "Tenant":
        contracts = {}
        upBill = {}
        paidBill = {}
        cursor = g.conn.execute("SELECT contract_id, bo_block_lot,unit FROM contract "
                                "WHERE contract.sign_by_tenant='" + str(ssn) + "'")
        for result in cursor:
            contracts[result[0]] = [result[1], result[2]]
        cursor = g.conn.execute("SELECT bill_id, amount,bill_date,pay_to FROM bill "
                                "WHERE bill.pay_from='" + str(ssn) + "'AND bill.paid=false")
        for result in cursor:
            upBill[result[0]] = ['$' + str(result[1]), str(result[2]), "Landlord: " + str(result[3])]
        cursor = g.conn.execute("SELECT bill_id, amount,bill_date,pay_to FROM bill "
                                "WHERE bill.pay_from='" + str(ssn) + "'AND bill.paid=true")
        for result in cursor:
            paidBill[result[0]] = ['$' + str(result[1]), str(result[2]), "Landlord: " + str(result[3])]
        return render_template("tenant.html", userinfo=user_info, contractinfo=contracts,
                               upinfo=upBill, paidinfo=paidBill)
    elif identity == "Landlord":
        contracts = {}
        upBill = {}
        paidBill = {}
        cursor = g.conn.execute("SELECT contract_id, bo_block_lot,unit FROM contract "
                                "WHERE contract.sign_by_landlord='" + str(ssn) + "'")
        for result in cursor:
            contracts[result[0]] = [result[1], result[2]]
        cursor = g.conn.execute("SELECT bill_id, amount,bill_date,pay_from FROM bill "
                                "WHERE bill.pay_to='" + str(ssn) + "'AND bill.paid=false")
        for result in cursor:
            upBill[result[0]] = ['$' + str(result[1]), str(result[2]), "Tenant: " + str(result[3])]
        cursor = g.conn.execute("SELECT bill_id, amount,bill_date,pay_from FROM bill "
                                "WHERE bill.pay_to='" + str(ssn) + "'AND bill.paid=true")
        for result in cursor:
            paidBill[result[0]] = ['$' + str(result[1]), str(result[2]), "Tenant: " + str(result[3])]
        return render_template("landlord.html", userinfo=user_info, contractinfo=contracts,
                               upinfo=upBill, paidinfo=paidBill)
    else:
        return render_template("agency.html", userinfo=user_info)
    # design a html template
    # click the login button, access the database to see if the user is exist
    # return information


if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=true, threaded=threaded)


    run()
