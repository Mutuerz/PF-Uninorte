import datetime
import random
from tkinter.ttk import Combobox

from firebase import firebase
import matplotlib.pyplot as p
import numpy as np
from tkinter import *

variables = []
values = []
dictionary = []
corr_mat = np.zeros((12, 12), int)
corr_p, p_oil, p_ev, p_con, s_con, s_ev, temph_i, temph_s, tempc_i, tempc_s, temp_d, temp_a = [], [], [], [], [], [], \
                                                                                              [], [], [], [], [], []
firebase = firebase.FirebaseApplication('https://proyecto-b2674.firebaseio.com/')


def pushed():
    date = datetime.datetime.now()

    data_dict = {"Temperatura del Déposito de Aceite": "1",
                 "Presión de Aceite": "2",
                 "Presión en Condesador": "3",
                 "Saturación en Condesador": "4",
                 "Presión del Evaporador": "5",
                 "Saturación en Evaporador": "6"}
    firebase.post('/RPi', data_dict)
    #firebase.put('RPi', "NombreX", data_dict)

    lbl_1.configure(text="you clicked")


def get_data(corrp, poil, pev, pcon, scon, sev, temphi, temphs, tempci, tempcs, tempd, tempa):
    # Here we clear the array
    variables.clear()
    data_dict = firebase.get("/data", None)

    if combo1.get() == "Ultimas 24 horas":
        length = 10  # value of the radio button for time lapse
    elif combo1.get() == 'Ultimas 72 horas':
        length = 50
    else:
        length = 100

    count = 0  # This counter indicates how much variables we are gonna get
    for i, j in data_dict.items():
        count += 1
        if count > length:
            break
        for x, y in j.items():
            if x == "% de Corriente a Plena Carga":
                corrp.append(y)
            elif x == "Presión de Aceite":
                poil.append(y)
            elif x == "Presión del Evaporador":
                pev.append(y)
            elif x == "Presión en Condesador":
                pcon.append(y)
            elif x == "Saturación en Condesador":
                scon.append(y)
            elif x == "Saturación en Evaporador":
                sev.append(y)
            elif x == "Temperatura de Agua Helada":
                for z, w in y.items():
                    if z == "Introduciendo":
                        temphi.append(w)
                    else:
                        temphs.append(w)
            elif x == "Temperatura de Agua de Condensación":
                for z, w in y.items():
                    if z == "Introduciendo":
                        tempci.append(w)
                    else:
                        tempcs.append(w)
            elif x == "Temperatura de Descarga":
                tempd.append(y)
            else:
                tempa.append(y)
    print("Contador: ", count)
    corrp = np.array(corrp)
    poil = np.array(poil)
    pev = np.array(pev)
    pcon = np.array(pcon)
    scon = np.array(scon)
    sev = np.array(sev)
    temphi = np.array(temphi)
    temphs = np.array(temphs)
    tempci = np.array(tempci)
    tempcs = np.array(tempcs)
    tempd = np.array(tempd)
    tempa = np.array(tempa)

    # Here we return all variables as a dictionary
    variables.extend((corrp, poil, pev, pcon, scon, sev, temphi, temphs, tempci, tempcs, tempd, tempa))


def plot(x, y, x_label, y_label):
    p.figure(x_label + " vs " + y_label)
    corr = np.corrcoef(x, y)
    corr = corr[0][1]
    p.title("Correlation coefficient: {}".format(corr))
    p.plot(x, y, ".r")
    p.xlabel(x_label)
    p.ylabel(y_label)
    p.show()


# Lets_plot allows to get the list of data and the respective label for the radio buttons selected
def lets_plot(name1, name2):

    """X"""
    if name1 == 'Temperatura de Descarga':
        x = variables[10]
    elif name1 == '% de Corriente a Plena Carga':
        x = variables[0]
    elif name1 == 'Temp Introduciendo Agua de condensación':
        x = variables[8]
    elif name1 == 'Temp Salida agua de condensación':
        x = variables[9]
    elif name1 == 'Temperatura del Depósito de Aceite':
        x = variables[11]
    elif name1 == 'Presión de Aceite':
        x = variables[1]
    elif name1 == 'Temp Introduciendo Agua Helada':
        x = variables[6]
    elif name1 == 'Temp Salida Agua Helada':
        x = variables[7]
    elif name1 == 'Presión de condensador':
        x = variables[3]
    elif name1 == 'Saturacion en condensador':
        x = variables[4]
    elif name1 == 'Presion del Evaporador':
        x = variables[2]
    if name1 == 'Saturacion en Evaporador':
        x = variables[5]

    """Y"""
    if name2 == 'Temperatura de Descarga':
        y = variables[10]
    elif name2 == '% de Corriente a Plena Carga':
        y = variables[0]
    elif name2 == 'Temp Introduciendo Agua de condensación':
        y = variables[8]
    elif name2 == 'Temp Salida agua de condensación':
        y = variables[9]
    elif name2 == 'Temperatura del Depósito de Aceite':
        y = variables[11]
    elif name2 == 'Presión de Aceite':
        y = variables[1]
    elif name2 == 'Temp Introduciendo Agua Helada':
        y = variables[6]
    elif name2 == 'Temp Salida Agua Helada':
        y = variables[7]
    elif name2 == 'Presión de condensador':
        y = variables[3]
    elif name2 == 'Saturacion en condensador':
        y = variables[4]
    elif name2 == 'Presion del Evaporador':
        y = variables[2]
    if name2 == 'Saturacion en Evaporador':
        y = variables[5]

    plot(x, y, name1, name2)

def update(list):
    combo3['values'] = list


def check_for_correlation():
    amount = 0
    corr_mat.fill(0)

    print("cantidad variables: ", len(variables))
    for i in range(0, len(variables)):  # len(variables) to get all data
        for j in range(i, len(variables)):
            if i != j:
                amount += 1
                corr = np.corrcoef(variables[i], variables[j])
                corr = corr[0][1]
                if abs(corr) >= 0.1:
                    print("Relevant correlation")
                    corr_mat[i][j] = 1

                print("Coeficiente de correlación: {}".format(corr))
    print(amount)

    for i in range(12):
        for j in range(i, 12):
            corr_mat[j][i] = corr_mat[i][j]

    print(corr_mat)


    """# Insert values into textbox
    txt_1.configure(state='normal')
    txt_1.insert("end", str(corr[0][1]))
    txt_1.configure(state='disabled')"""

def on_select():

    # this vector saves the values that are correlated to the one selected in the combobox2
    vec = []
    # This vector saves the variables names
    vec2 = []

    val = 0
    for i in range(12):
        if dictionary[i] == combo2.get():
            val = i
            break
    for i in range(0, len(corr_mat)):
        if corr_mat[val][i] == 1:
            vec.append(i)
    for i in range(0, len(vec)):
        vec2.append(dictionary[vec[i]])
    combo3.configure(state='readonly')
    combo3.configure(postcommand=update(vec2))


if __name__ == "__main__":

    '''Main Window'''
    window = Tk()
    # Window title
    window.title("DSRED (Display System for Raspberry pi Extracted Data)")
    # Window size
    window.geometry('600x200')

    """-------------------------------------------------------GUI----------------------------------------------------"""
    '''Labels'''
    lbl_1 = Label(window, text="Push Data")
    lbl_2 = Label(window, text="Get Data")
    lbl_3 = Label(window, text="Graph variables")
    lbl_4 = Label(window, text="Check for correlation")
    lbl_5 = Label(window, text="Correlation coefficient")
    lbl_6 = Label(window, text="X axis")
    lbl_7 = Label(window, text="Y axis")

    '''Buttons actions'''
    # Push data
    btn_1 = Button(window, text="Push data", bg="gray", fg="black", command=pushed)
    # Get data
    btn_2 = Button(window, text="Get data", bg="gray", fg="black", command=lambda: get_data(corr_p, p_oil, p_ev, p_con,
                                                                                            s_con, s_ev, temph_i,
                                                                                            temph_s, tempc_i, tempc_s,
                                                                                            temp_d, temp_a))
    # Graph variables
    btn_3 = Button(window, text="Graph", bg="gray", fg="black", command=lambda: lets_plot(combo2.get(), combo3.get()))
    # Check correlation
    btn_4 = Button(window, text="Check", bg="gray", fg="black", command=lambda: check_for_correlation())

    '''Combo boxes'''
    # Radio buttons values must be different from each other
    selected2 = StringVar()  # Selected for x axis
    selected3 = StringVar()  # Selected for y axis
    combo1 = Combobox(window, width=33, state='readonly')
    combo2 = Combobox(window, width=33, state='readonly')
    combo3 = Combobox(window, width=33, state='disabled')

    combo1['values'] = ('Ultimas 24 horas', 'Ultimas 72 horas', 'Ultima semana')
    combo2['values'] = ('% de Corriente a Plena Carga', 'Presión de Aceite', 'Presion del Evaporador',
                       'Presión de condensador', 'Saturacion en condensador', 'Saturacion en Evaporador',
                       'Temp Introduciendo Agua Helada', 'Temp Salida Agua Helada',
                       'Temp Introduciendo Agua de condensación', 'Temp Salida agua de condensación',
                       'Temperatura de Descarga','Temperatura del Depósito de Aceite')

    combo3['values'] = ('% de Corriente a Plena Carga', 'Presión de Aceite', 'Presion del Evaporador',
                       'Presión de condensador', 'Saturacion en condensador', 'Saturacion en Evaporador',
                       'Temp Introduciendo Agua Helada', 'Temp Salida Agua Helada',
                       'Temp Introduciendo Agua de condensación', 'Temp Salida agua de condensación',
                       'Temperatura de Descarga','Temperatura del Depósito de Aceite')
    #combo3.set("")
    #combo3.trace('values', on_select)
    combo2.bind("<<ComboboxSelected>>", lambda _ : on_select())

    #corrp, poil, pev, pcon, scon, sev, temphi, temphs, tempci, tempcs, tempd, tempa
    dictionary.extend(('% de Corriente a Plena Carga', 'Presión de Aceite', 'Presion del Evaporador',
                       'Presión de condensador', 'Saturacion en condensador', 'Saturacion en Evaporador',
                       'Temp Introduciendo Agua Helada', 'Temp Salida Agua Helada',
                       'Temp Introduciendo Agua de condensación', 'Temp Salida agua de condensación',
                       'Temperatura de Descarga','Temperatura del Depósito de Aceite'))
    '''Textboxes'''
    # Correlation Coefficient
    txt_1 = Text(window, state='disabled', width=20, height=1)

    """-------------------------------------------------GRID--------------------------------------------------------"""
    '''Labels Grid'''
    # Push data
    # lbl_1.grid(column=0, row=0)
    # Get data
    lbl_2.grid(column=0, row=1)
    # Check correlation
    lbl_4.grid(column=2, row=1)
    # X axis
    lbl_6.grid(column=0, row=8)
    # Y axis
    lbl_7.grid(column=0, row=10)


    '''Buttons grid'''
    # Push data
    # btn_1.grid(column=1, row=0)
    # Get data
    btn_2.grid(column=1, row=2)
    # Graph variables
    btn_3.grid(column=1, row=11)
    # Check correlation
    btn_4.grid(column=3, row=1)

    '''Radio buttons grid'''
    # Time lapse
    combo1.grid(column=1, row=1)
    combo2.grid(column=1, row=8)
    combo3.grid(column=1, row=10)

    '''Textboxes grid'''

    # Window loop, must be at the end
    window.mainloop()
