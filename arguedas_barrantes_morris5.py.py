def entradas():
    largo, ancho, piezas= map(int, input().split())
    Piezas= []
    for i in range(piezas):
        pieza= []
        for j in range(4):
            pieza.append(list(input().strip()))
        Piezas.append(pieza)
    return largo, ancho, Piezas

def rotar_90(matriz):
    return [list(row) for row in zip(*matriz[::-1])]

def espejo(matriz):
    return [fila[::-1] for fila in matriz]

def variables(pieza, guardadas={}):
    beta= tuple(map(tuple, pieza))
    if beta in guardadas:
        return guardadas[beta]
    variables= []
    en_uso= [fila[:] for fila in pieza]
    for i in range(4):
        variables.append(en_uso)
        variables.append(espejo(en_uso))
        en_uso = rotar_90(en_uso)

    guardadas[beta]= variables
    return variables

def puede_colocar(tablero, pieza, fila, columna):
    for i in range(len(pieza)):
        for j in range(len(pieza[0])):
            if pieza[i][j] != '.' and (fila + i >= len(tablero) or columna + j >= len(tablero[0]) or tablero[fila + i][columna + j] != '.'):
                return False
    return True

def colocar_pieza(tablero, pieza, fila, columna):
    for i in range(len(pieza)):
        for j in range(len(pieza[i])):
            if pieza[i][j] != '.':
                tablero[fila + i][columna + j]= pieza[i][j]

def AUXILIO(largo, ancho, Piezas, pieza_actual= 0, tablero= None, cambios= {}, estados= {}):
    if tablero is None:
        tablero= [['.' for i in range(ancho)] for j in range(largo)]
    if pieza_actual == len(Piezas):
        return tablero
    estado_actual= (pieza_actual, tuple(map(tuple, tablero)))
    if estado_actual in estados:
        return estados[estado_actual]

    for fila in range(largo):
        for columna in range(ancho):
            pieza_key = tuple(map(tuple, Piezas[pieza_actual]))
            for variacion in cambios.get(pieza_key, variables(Piezas[pieza_actual])):
                if puede_colocar(tablero, variacion, fila, columna):
                    tablero1 = [fila[:] for fila in tablero]
                    colocar_pieza(tablero1, variacion, fila, columna)
                    solucion = AUXILIO(largo, ancho, Piezas, pieza_actual + 1, tablero1, cambios, estados)
                    if solucion:
                        estados[estado_actual]= solucion
                        return solucion
    estados[estado_actual]= None
    return None

largo, ancho, piezas= entradas()
Final= AUXILIO(largo, ancho, piezas)

if Final:
    completo= all(elemento != '.' for fila in Final for elemento in fila)
    if completo:
        for fila in Final:
            print(''.join(fila))
    else:
        print('-1')
else:
    print('-1')
