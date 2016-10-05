from flask import Flask
from flask import request
from model import db
from model import User
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

@app.route('/')
def welcome():
	return " Hello. Enter the correct extensions for each request."

@app.route('/v1/expenses', methods=['GET'])
def get_expenses():
	try:
		users = User.query.all()
		expense_details = {}
		for user in users:
			expense_details[user.id] = {'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category, 'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': user.submit_date, 'status': user.status, 'decision_date': user.decision_date}

		return json.dumps(expense_details), 200

	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/v1/expenses/<expense_id>',methods =['GET'])
def get_expense_ID():
	try:
		user = User.query.filter_by(id=expense_id).first_or_404()
		return json.dumps({'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category, 'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': user.submit_date, 'status': user.status, 'decision_date': user.decision_date}), 200
	except IntegrityError:
		return json.dumps({'status':False})


@app.route('/v1/expenses', methods=['POST'])
def post_data():
    try:
        data = json.loads(request.data)
            if not data or not 'email' in data:
                abort(404)
                database = CreateDB(hostname = 'localhost')
                db.create()
                user = User(data['name'], data['email'], data['category'], data['description'], data['link'], data['estimated_costs'], data['submit_date'])
                db.session.add(expense)
                db.session.commit()
                
                added_expense = {'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category, 'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': user.submit_date, 'status': user.status, 'decision_date': user.decision_date}
                return json.dumps(added_expense), 201
        
        except IntegrityError:
            return json.dumps({'status':False})

@app.route('/v1/expenses/<expense_id>',methods=['PUT'])
def update_expense_ID():
	try:
		expense_data = json.loads(request.data)
		user = User.query.get(expense_id)
		user.estimated_costs = content['estimated_costs']
		db.session.commit()
		return json.dumps({'Accepted'}),202

	except IntegrityError:
		return json.dumps({'status':False})


@app.route('/v1/expenses/<int:expense_id>',methods=['DELETE'])
def delete_expense_ID(expense_id):
	try:
		db.session.delete(User.query.get(expense_id))
		db.session.commit()
		return json.dumps({'No Content'}),204

	except IntegrityError:
		return json.dumps({'status':False})
@app.route('/createdb')
def createDatabase():
	HOSTNAME = 'localhost'
	try:
		HOSTNAME = request.args['hostname']
	except:
		pass
	database = CreateDB(hostname = HOSTNAME)
	return json.dumps({'status':True})

@app.route('/info')
def app_status():
	return json.dumps({'server_info':application.config['SQLALCHEMY_DATABASE_URI']})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

