from pathlib import Path
import time
import datetime
from firebase import firebase
import numpy as np
from time import sleep
home = str(Path.home())
firebase = firebase.FirebaseApplication('https://proyecto-b2674.firebaseio.com/')

global errors
errors = 0


def read_csv(path):
    return np.genfromtxt(path, delimiter=";", skip_header=True).astype(float)

def check_if_equal(array_to_check, data):
    data = data.tolist()
    everything_is_ok = False
    for x in data:
        if array_to_check == x:
            everything_is_ok = True
            
    return everything_is_ok

def push_data(variables):
    date = datetime.datetime.now()
    variables.append(date)
    try:
        new_dict = {"% de Corriente a Plena Carga": variables[8],
                            "Presión de Aceite": variables[9],
                            "Presión del Evaporador": variables[3],
                            "Presión en Condesador": variables[2],
                            "Saturación en Condesador": variables[0],
                            "Saturación en Evaporador": variables[1],
                            "Temperatura de Agua Helada": {
                                "Introduciendo": variables[7],
                                "Salida": variables[5]},
                            "Temperatura de Agua de Condensación": {
                                "Introduciendo": variables[6],
                                "Salida": variables[4]},
                            "Temperatura de Descarga": variables[10],
                            "Temperatura del Déposito de Aceite": variables[11],
                            "Fecha de toma": variables[12]}
    except:
        new_dict = {"% de Corriente a Plena Carga": 0,
                            "Presión de Aceite": 0,
                            "Presión del Evaporador": 0,
                            "Presión en Condesador": 0,
                            "Saturación en Condesador": 0,
                            "Saturación en Evaporador": 0,
                            "Temperatura de Agua Helada": {
                                "Introduciendo": 0,
                                "Salida": 0},
                            "Temperatura de Agua de Condensación": {
                                "Introduciendo": 0,
                                "Salida": 0},
                            "Temperatura de Descarga": 0,
                            "Temperatura del Déposito de Aceite": 0,
                            "Fecha de toma": 0}            
    firebase.post('/sustentacion', new_dict)
    
def analyze(file_content):
    #file_content = open(home + '/Desktop/resultados1.txt', 'r')
    data = []
    error = False
    errors = 0
    for line in file_content:
        letter = 0
        # filters blank spaces
        if line is not "\n":
            # search for individual characters
            for i in range(len(line)):
                
                # search for numbers to filter noise
                if line[i].isdigit():
                    letter += 1
                    

            # if there are numbers
            if letter >= 2:
                # found characters in the string
                sub_coma = line.find(",")
                sub_space = line.find(" ")
                sub_wtf = line.find("§")
                
                
                # takes first x characters
                line = line[:sub_space]
                sub_bolita = line.find("°")
                if sub_wtf is not -1:
                    temp = line[:sub_wtf]
                    temp2 = line[sub_wtf+1]
                    line = temp+"5"+temp2
                    
                if sub_bolita is not -1:
                    line = line[:sub_bolita]
                # changes comas to dots
                if sub_coma is not -1:
                    temp = line[:sub_coma]
                    temp2 = line[sub_coma+1:]
                    line = temp+"."+temp2
                
                # Search for dots
                sub_dot = line.find(".")
                # If there are not dots well... we put one
                """if sub_dot is -1:
                    if sub_space is not -1:
                        print("CORRECCION: ESPACIO POR PUNTO")
                        temp = line[:sub_space]
                        temp2 = line[sub_space+1:]
                        line = temp+"."+temp2"""
                # Eliminate spaces
                if sub_space is not -1:
                    temp = line[:sub_space]
                    temp2 = line[sub_space+1:]
                    line = temp+temp2
                
                
                try:
                    line = float(line)
                except (Exception, ArithmeticError) as e:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(e).__name__, e.args)
                    error = True
                    line = 0
                    print(message)

                data.append(line)
    if error:
        errors = 1
    print(data)
    return data, errors


if __name__ == "__main__":

    start_time = time.time()
    while True:
        #analyze(errors)
        push_data(analyze(errors))
        print("--- {} seconds ---".format(time.time() - start_time))
        sleep(5)
