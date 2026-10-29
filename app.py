
from flask import Flask, render_template, request, jsonify
import ast
import math

# IMPORTAR LAS FUNCIONES DE NUESTRA CALCULADORA ORIGINAL

from calculadora import (
    sumar,
    restar,
    multiplicar,
    dividir,
    calcularPotencia,
    calcularModulo,
    calcularRaizCuadrada,
    calcularRaizEnesima,
    calcularSeno,
    calcularCoseno,
    calcularTangente,
    calcularLogaritmoDecimal,
    calcularLogaritmoNatural,
    calcularLogaritmoBase,
    calcularValorAbsoluto,
    calcularFactorial,
    calcularPorcentaje,
    convertirGradosARadianes,
    convertirRadianesAGrados,
    redondearNumero
)

app = Flask(__name__)


# ========================================
# PAGINA PRINCIPAL
# ========================================

@app.route("/")
def mostrarCalculadora():
    return render_template("index.html")


# ========================================
# VALIDAR RESULTADOS
# ========================================

def validarResultado(numero):

    if type(numero) not in (int, float):
        raise ValueError("Resultado matemático no válido")

    if abs(numero) > 1e100:
        raise ValueError("Resultado demasiado grande")

    if not math.isfinite(numero):
        raise ValueError("Resultado fuera de rango")

    return numero


# ========================================
# FUNCIONES CIENTIFICAS
# ========================================

def ejecutarFuncion(nombre, argumentos, modoAngulo):

    # FUNCIONES DE UN SOLO ARGUMENTO

    funcionesUnaEntrada = {
        "sqrt": calcularRaizCuadrada,
        "log": calcularLogaritmoDecimal,
        "ln": calcularLogaritmoNatural,
        "abs": calcularValorAbsoluto,
        "gradosRadianes": convertirGradosARadianes,
        "radianesGrados": convertirRadianesAGrados
    }

    if nombre in funcionesUnaEntrada:

        if len(argumentos) != 1:
            raise ValueError("La función requiere un número")

        numero = argumentos[0]

        if nombre == "sqrt" and numero < 0:
            raise ValueError("La raíz cuadrada requiere un número positivo o cero")

        if nombre in ("log", "ln") and numero <= 0:
            raise ValueError("El logaritmo requiere un número mayor que cero")

        return funcionesUnaEntrada[nombre](numero)

    # TRIGONOMETRIA

    if nombre in ("sin", "cos", "tan"):

        if len(argumentos) != 1:
            raise ValueError("Se requiere un ángulo")

        angulo = argumentos[0]

        # Nuestro Python original trabaja en grados.
        # Convertimos cuando el usuario selecciona RAD.
        if modoAngulo == "RAD":
            angulo = math.degrees(angulo)

        if nombre == "sin":
            resultado = calcularSeno(angulo)

        elif nombre == "cos":
            resultado = calcularCoseno(angulo)

        else:
            if math.isclose(
                math.cos(math.radians(angulo)),
                0,
                abs_tol=1e-10
            ):
                raise ValueError("La tangente no está definida")

            resultado = calcularTangente(angulo)

        # Corregir pequeñas imprecisiones decimales
        if abs(resultado) < 1e-12:
            resultado = 0

        return resultado

    # FACTORIAL

    if nombre == "factorial":

        if len(argumentos) != 1:
            raise ValueError("Se requiere un número")

        numero = argumentos[0]

        if numero < 0 or not float(numero).is_integer():
            raise ValueError("El factorial requiere un entero no negativo")

        if numero > 170:
            raise ValueError("Factorial demasiado grande")

        return calcularFactorial(float(numero))

    # RAIZ ENESIMA
    # Formato: root(indice, numero)

    if nombre == "root":

        if len(argumentos) != 2:
            raise ValueError("Ingresa índice y número")

        indice, numero = argumentos

        if indice == 0 or not float(indice).is_integer():
            raise ValueError("El índice debe ser un entero distinto de cero")

        indice = int(indice)

        if numero < 0 and indice % 2 == 0:
            raise ValueError("No existe raíz par real de un número negativo")

        if numero == 0 and indice < 0:
            raise ValueError("No se puede dividir entre cero")

        return calcularRaizEnesima(numero, indice)

    # LOGARITMO DE BASE PERSONALIZADA
    # Formato: logBase(numero, base)

    if nombre == "logBase":

        if len(argumentos) != 2:
            raise ValueError("Ingresa número y base")

        numero, base = argumentos

        if numero <= 0 or base <= 0 or base == 1:
            raise ValueError("Número y base inválidos para logaritmo")

        return calcularLogaritmoBase(numero, base)

    # MODULO O RESIDUO
    # Formato: modulo(numeroUno, numeroDos)

    if nombre == "modulo":

        if len(argumentos) != 2:
            raise ValueError("Ingresa dos números")

        if argumentos[1] == 0:
            raise ValueError("No se puede calcular módulo con cero")

        return calcularModulo(argumentos[0], argumentos[1])

    # PORCENTAJE
    # Formato: porcentaje(numero, porcentaje)

    if nombre == "porcentaje":

        if len(argumentos) != 2:
            raise ValueError("Ingresa número y porcentaje")

        return calcularPorcentaje(argumentos[0], argumentos[1])

    # REDONDEAR
    # Formato: redondear(numero, decimales)

    if nombre == "redondear":

        if len(argumentos) != 2:
            raise ValueError("Ingresa número y decimales")

        numero, decimales = argumentos

        if not float(decimales).is_integer():
            raise ValueError("Los decimales deben ser enteros")

        decimales = int(decimales)

        if decimales < 0 or decimales > 15:
            raise ValueError("Usa entre 0 y 15 decimales")

        return redondearNumero(numero, decimales)

    raise ValueError("Función no permitida")


# ========================================
# INTERPRETAR LA EXPRESION MATEMATICA
# ========================================

def resolverOperacion(nodo, modoAngulo, ans, profundidad=0):

    if profundidad > 40:
        raise ValueError("Expresión demasiado compleja")

    def resolver(hijo):
        return resolverOperacion(
            hijo, modoAngulo, ans, profundidad + 1
        )

    # EXPRESION PRINCIPAL

    if isinstance(nodo, ast.Expression):
        return resolver(nodo.body)

    # NUMEROS

    if isinstance(nodo, ast.Constant):

        if type(nodo.value) in (int, float):
            return validarResultado(nodo.value)

        raise ValueError("Valor no permitido")

    # CONSTANTES MATEMATICAS

    if isinstance(nodo, ast.Name):

        if nodo.id == "pi":
            return math.pi

        if nodo.id == "Ans":
            return validarResultado(ans)

        raise ValueError("Constante no permitida")

    # SIGNO POSITIVO O NEGATIVO

    if isinstance(nodo, ast.UnaryOp):

        numero = resolver(nodo.operand)

        if isinstance(nodo.op, ast.USub):
            return validarResultado(-numero)

        if isinstance(nodo.op, ast.UAdd):
            return validarResultado(numero)

    # OPERACIONES BASICAS

    if isinstance(nodo, ast.BinOp):

        numeroUno = resolver(nodo.left)
        numeroDos = resolver(nodo.right)

        if isinstance(nodo.op, ast.Add):
            resultado = sumar(numeroUno, numeroDos)

        elif isinstance(nodo.op, ast.Sub):
            resultado = restar(numeroUno, numeroDos)

        elif isinstance(nodo.op, ast.Mult):
            resultado = multiplicar(numeroUno, numeroDos)

        elif isinstance(nodo.op, ast.Div):

            if numeroDos == 0:
                raise ValueError("No se puede dividir entre cero")

            resultado = dividir(numeroUno, numeroDos)

        elif isinstance(nodo.op, ast.Pow):

            if abs(numeroDos) > 100:
                raise ValueError("Exponente demasiado grande")

            resultado = calcularPotencia(numeroUno, numeroDos)

        else:
            raise ValueError("Operación no permitida")

        return validarResultado(resultado)

    # LLAMADAS A FUNCIONES MATEMATICAS

    if isinstance(nodo, ast.Call):

        if not isinstance(nodo.func, ast.Name):
            raise ValueError("Función no permitida")

        if nodo.keywords or len(nodo.args) > 2:
            raise ValueError("Argumentos no permitidos")

        nombre = nodo.func.id

        argumentos = [
            resolver(argumento)
            for argumento in nodo.args
        ]

        resultado = ejecutarFuncion(
            nombre, argumentos, modoAngulo
        )

        return validarResultado(resultado)

    raise ValueError("Expresión no permitida")


# ========================================
# API PARA CALCULAR
# ========================================

@app.route("/api/calcular", methods=["POST"])
def calcular():

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            raise ValueError("Solicitud inválida")

        expresion = datos.get("expresion", [])
        modoAngulo = datos.get("modoAngulo", "DEG")
        ans = datos.get("ans", 0)

        if modoAngulo not in ("DEG", "RAD"):
            raise ValueError("Modo angular inválido")

        if not isinstance(expresion, list):
            raise ValueError("Expresión inválida")

        if not all(type(valor) is str for valor in expresion):
            raise ValueError("Expresión inválida")

        if len(expresion) > 200:
            raise ValueError("Expresión demasiado larga")

        if type(ans) not in (int, float):
            raise ValueError("Ans inválido")

        ans = validarResultado(ans)

        operacion = "".join(expresion)

        if not operacion or len(operacion) > 240:
            raise ValueError("Expresión vacía o demasiado larga")

        # El porcentaje individual equivale a dividir entre 100
        operacion = operacion.replace("%", "/100")

        # Cerrar paréntesis abiertos automáticamente
        abiertos = operacion.count("(")
        cerrados = operacion.count(")")

        if abiertos > cerrados:
            operacion += ")" * (abiertos - cerrados)

        arbol = ast.parse(operacion, mode="eval")

        resultado = resolverOperacion(
            arbol, modoAngulo, ans
        )

        resultado = validarResultado(resultado)

        # Mostrar hasta 12 cifras significativas
        resultado = float(f"{resultado:.12g}")

        return jsonify({
            "resultado": resultado
        })

    except (
        ValueError,
        SyntaxError,
        ArithmeticError,
        RecursionError,
        TypeError
    ) as error:

        return jsonify({
            "error": str(error)
        }), 400


# ========================================
# EJECUTAR FLASK
# ========================================

if __name__ == "__main__":
    app.run(debug=True)
