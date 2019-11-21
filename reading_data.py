from pathlib import Path
import time
import datetime
from firebase import firebase
from time import sleep
home = str(Path.home())
firebase = firebase.FirebaseApplication('https://proyecto-b2674.firebaseio.com/')

global errors
errors = 0


def push_data(variables):
    date = datetime.datetime.now()
    variables.append(date)
    new_dict = {"% de Corriente a Plena Carga": variables[9],
                        "Presión de Aceite": variables[8],
                        "Presión del Evaporador": variables[2],
                        "Presión en Condesador": variables[3],
                        "Saturación en Condesador": variables[1],
                        "Saturación en Evaporador": variables[0],
                        "Temperatura de Agua Helada": {
                            "Introduciendo": variables[6],
                            "Salida": variables[5]},
                        "Temperatura de Agua de Condensación": {
                            "Introduciendo": variables[7],
                            "Salida": variables[4]},
                        "Temperatura de Descarga": variables[11],
                        "Temperatura del Déposito de Aceite": variables[10],
                        "Fecha de toma": variables[12]}
    firebase.post('/pruebas_2', new_dict)

def analyze(file_content):
    #file_content = open(home + '/Desktop/resultados1.txt', 'r')
    data = []
    errors = 0
    for line in file_content:
        letter = 0
        # filters blank spaces
        if line is not "\n":
            
            # takes first x characters
            line = line[:4]
            try:
                line = float(line)
            except (Exception, ArithmeticError) as e:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                errors += 1
                line = 0
                print(message)

            data.append(line)
    print(data)
    return data, errors


if __name__ == "__main__":

    start_time = time.time()
    while True:
        #analyze(errors)
        push_data(analyze(errors))
        print("--- {} seconds ---".format(time.time() - start_time))
        sleep(5)
