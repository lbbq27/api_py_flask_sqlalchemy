from flask import Flask
from flask_sqlalchemy import SQLAlchemy  ##----importamos sqlalchemy-----------2
from flask_restful import Resource, Api, reqparse, fields,marshal_with, abort ###----------importamos todas estas clases del modulo flask_restful------------3



app = Flask(__name__)  ## creamos la aplicacion---1
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db' ##-------------configuramos la DB --- SQLAlchemy tiene base de datos propia de python-------2.1
db = SQLAlchemy(app)## creamos DB y enlazamos la app con sqlalchemy-------2.2
api= Api(app) ##########creamos la variable api y enlazamos con la app----3.1



class UserModel(db.Model):  ##--------------creamos el modelo----------2.3 ---- IMPORTANTE Column con C mayuscula----2.3
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self): ##-------- hacemos la representacion de los valores que vamos a manipular en la db-----2.4
        return {

            "name" : self.name,
            "email" : self.email
        }
     ###------------creamos un nuevo archivo que se llamara create_db.py---------2.5------> seguimos alla   

user_args = reqparse.RequestParser() ###-----------parseamos la info que ingresa el usuario----------------3.2
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")



## creamos el objeto similar al JSON y lo envolvemos en la clase con maeshal_with(userFields)...3.5
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}


######-----------creamos la clase --------ES COMO EL CONTROLADOR EN EL MVC------ 3.3 

###################-----------------ALL USERS--------------------------------
class Users(Resource): 
    @marshal_with(userFields) ##--------------pendiente hacer esto----------------3.6----------ruta GET ---SHOW ALL---------
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields) ##--------------pendiente hacer esto----------------3.6----------ruta POST -- CREATES a new USER---------
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])   ##-----se crea un solo usuario----3.7
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users , 201

#####----------------------------ONE  USER---------------------------------------    
class User(Resource): ##------------pendiente hacer esto--------------3.8------ ruta GET---- READ  ONE USER
    @marshal_with(userFields)
    def get(self, id):
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user

    @marshal_with(userFields) ##---------pendiente hacer esto------------3.9-------PATCH---UPDATE USER---
    def patch(self, id):
        args = user_args.parse_args()
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args['name'] 
        user.email = args['email']  
        db.session.commit()
        return user , 201  
    
    @marshal_with(userFields) ##---------pendiente hacer esto------------3.10-------DELETE---DELETE USER---
    def delete(self, id):
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users  










###############----------------------routes-----------------------------

api.add_resource(Users, '/api/users/') ##------------------asi se crea el route de la API--------- 3.4
api.add_resource(User, '/api/users/<int:id>') ##------------------asi se crea el route de la API--------- 3.4










@app.route('/', methods= ["GET"]) ##------creamos ruta para verificar que se conecto e forma correcta----1.3
def home():
    return('Hello Home')









if __name__=='__main__': ##-----------creamos la conexion con el servidor en modo debug----1.2
    app.run(debug=True)