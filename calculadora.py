import math


# ==============================
# FUNCIONES DE OPERACIONES BASICAS
# ==============================

def sumar(numeroUno, numeroDos):
    return numeroUno + numeroDos


def restar(numeroUno, numeroDos):
    return numeroUno - numeroDos


def multiplicar(numeroUno, numeroDos):
    return numeroUno * numeroDos


def dividir(numeroUno, numeroDos):
    if numeroDos == 0:
        print("Error: no se puede dividir entre cero.")
        return None
    return numeroUno / numeroDos


def calcularPotencia(base, exponente):
    return base ** exponente


def calcularModulo(numeroUno, numeroDos):
    if numeroDos == 0:
        print("Error: no se puede calcular el modulo con cero.")
        return None
    return numeroUno % numeroDos


# ==============================
# FUNCIONES DE RAICES
# ==============================

def calcularRaizCuadrada(numero):
    if numero < 0:
        print("Error: no existe una raiz cuadrada real de un numero negativo.")
        return None
    return math.sqrt(numero)


def calcularRaizEnesima(numero, indice):
    if indice == 0:
        print("Error: el indice de la raiz no puede ser cero.")
        return None

    if numero < 0:
        if indice % 2 == 0:
            print("Error: una raiz par de un numero negativo no es real.")
            return None
        return -((-numero) ** (1 / indice))

    return numero ** (1 / indice)


# ==============================
# FUNCIONES DE TRIGONOMETRIA
# Los angulos se ingresan en grados
# ==============================

def calcularSeno(angulo):
    return math.sin(math.radians(angulo))


def calcularCoseno(angulo):
    return math.cos(math.radians(angulo))


def calcularTangente(angulo):
    anguloRad = math.radians(angulo)

    if math.isclose(math.cos(anguloRad), 0, abs_tol=1e-10):
        print("Error: la tangente no esta definida para ese angulo.")
        return None

    return math.tan(anguloRad)


# ==============================
# FUNCIONES DE LOGARITMOS
# ==============================

def calcularLogaritmoDecimal(numero):
    if numero <= 0:
        print("Error: el logaritmo requiere un numero mayor que cero.")
        return None
    return math.log10(numero)


def calcularLogaritmoNatural(numero):
    if numero <= 0:
        print("Error: el logaritmo requiere un numero mayor que cero.")
        return None
    return math.log(numero)


def calcularLogaritmoBase(numero, base):
    if numero <= 0 or base <= 0 or base == 1:
        print("Error: el numero debe ser positivo y la base positiva distinta de uno.")
        return None
    return math.log(numero, base)


# ==============================
# OTRAS FUNCIONES MATEMATICAS
# ==============================

def calcularValorAbsoluto(numero):
    return abs(numero)


def calcularFactorial(numero):
    if numero < 0 or not numero.is_integer():
        print("Error: el factorial requiere un entero no negativo.")
        return None
    return math.factorial(int(numero))


def calcularPorcentaje(numero, porcentaje):
    return numero * porcentaje / 100


def convertirGradosARadianes(angulo):
    return math.radians(angulo)


def convertirRadianesAGrados(anguloRad):
    return math.degrees(anguloRad)


def redondearNumero(numero, decimales):
    return round(numero, decimales)


# ==============================
# FUNCIONES PARA LEER DATOS
# ==============================

def pedirNumero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Entrada no valida. Escribe un numero.")


def pedirEntero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada no valida. Escribe un numero entero.")


# ==============================
# MENU PRINCIPAL
# ==============================

def mostrarMenu():
    print("\n========== CALCULADORA CIENTIFICA ==========")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Potencia")
    print("6. Raiz cuadrada")
    print("7. Raiz enesima")
    print("8. Seno")
    print("9. Coseno")
    print("10. Tangente")
    print("11. Logaritmo decimal (base 10)")
    print("12. Logaritmo natural (base e)")
    print("13. Logaritmo con una base elegida")
    print("14. Valor absoluto")
    print("15. Factorial")
    print("16. Porcentaje")
    print("17. Modulo")
    print("18. Convertir grados a radianes")
    print("19. Convertir radianes a grados")
    print("20. Mostrar el valor de pi")
    print("21. Redondear un numero")
    print("0. Salir")
    print("============================================")


def ejecutarCalculadora():
    while True:
        mostrarMenu()
        opcion = input("Elige una opcion: ").strip()
        resultado = None

        if opcion == "0":
            print("Gracias por usar la calculadora.")
            break

        elif opcion in ("1", "2", "3", "4", "5", "17"):
            numeroUno = pedirNumero("Ingresa el primer numero: ")
            numeroDos = pedirNumero("Ingresa el segundo numero: ")

            if opcion == "1":
                resultado = sumar(numeroUno, numeroDos)
            elif opcion == "2":
                resultado = restar(numeroUno, numeroDos)
            elif opcion == "3":
                resultado = multiplicar(numeroUno, numeroDos)
            elif opcion == "4":
                resultado = dividir(numeroUno, numeroDos)
            elif opcion == "5":
                resultado = calcularPotencia(numeroUno, numeroDos)
            elif opcion == "17":
                resultado = calcularModulo(numeroUno, numeroDos)

        elif opcion in ("6", "8", "9", "10", "11", "12", "14", "15", "18", "19"):
            numero = pedirNumero("Ingresa el numero o angulo: ")

            if opcion == "6":
                resultado = calcularRaizCuadrada(numero)
            elif opcion == "8":
                resultado = calcularSeno(numero)
            elif opcion == "9":
                resultado = calcularCoseno(numero)
            elif opcion == "10":
                resultado = calcularTangente(numero)
            elif opcion == "11":
                resultado = calcularLogaritmoDecimal(numero)
            elif opcion == "12":
                resultado = calcularLogaritmoNatural(numero)
            elif opcion == "14":
                resultado = calcularValorAbsoluto(numero)
            elif opcion == "15":
                resultado = calcularFactorial(numero)
            elif opcion == "18":
                resultado = convertirGradosARadianes(numero)
            elif opcion == "19":
                resultado = convertirRadianesAGrados(numero)

        elif opcion == "7":
            numero = pedirNumero("Ingresa el numero: ")
            indice = pedirEntero("Ingresa el indice de la raiz: ")
            resultado = calcularRaizEnesima(numero, indice)

        elif opcion == "13":
            numero = pedirNumero("Ingresa el numero: ")
            base = pedirNumero("Ingresa la base: ")
            resultado = calcularLogaritmoBase(numero, base)

        elif opcion == "16":
            numero = pedirNumero("Ingresa el numero: ")
            porcentaje = pedirNumero("Ingresa el porcentaje: ")
            resultado = calcularPorcentaje(numero, porcentaje)

        elif opcion == "20":
            resultado = math.pi

        elif opcion == "21":
            numero = pedirNumero("Ingresa el numero: ")
            decimales = pedirEntero("Cantidad de decimales: ")
            if decimales < 0:
                print("La cantidad de decimales no puede ser negativa.")
                continue
            resultado = redondearNumero(numero, decimales)

        else:
            print("Opcion no valida. Intenta nuevamente.")
            continue

        if resultado is not None:
            print("Resultado:", resultado)


# ==============================
# INICIO DEL PROGRAMA
# ==============================

if __name__ == "__main__":
    ejecutarCalculadora()
