from app import app, db

with app.app_context(): ## ----esta funcion nos permite crear la base de datos en python-------2.6
    db.create_all()

##------ahora ejecutamos este archivo en la CLI para que finalice la creacion de la DB ---------->py create_db.py -----------2.7

###---------una vez ejecutado este comando debe generar un acarpeta llamada INSTANCE  con el archivo que representa la DB----
##-------ahora regresamos a  app para importar el modulo flask_retful y las librerias.........>
