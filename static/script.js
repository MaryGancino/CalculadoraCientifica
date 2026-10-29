
/* =========================================
   CALCULADORA CIENTIFICA CASIO
   CONTROL DE BOTONES Y PANTALLA
========================================= */

// ELEMENTOS DE LA PANTALLA

const pantallaOperacion = document.getElementById("operacion");
const pantallaResultado = document.getElementById("resultado");
const indicador = document.getElementById("indicador");
const indicadorShift = document.getElementById("indicadorShift");
const menuFunciones = document.getElementById("menuFunciones");

// VARIABLES PRINCIPALES

let expresion = [];
let shiftActivo = false;
let modoAngulo = "DEG";
let ultimoResultado = 0;

// SIMBOLOS QUE VEREMOS EN LA PANTALLA

const simbolos = {
    "*": "×",
    "/": "÷",
    "-": "−",
    "**": "^",
    "**2": "²",
    "*10**": "×10^",
    "sqrt(": "√(",
    "root(": "ⁿ√(",
    "log(": "log(",
    "logBase(": "logₐ(",
    "ln(": "ln(",
    "factorial(": "factorial(",
    "abs(": "abs(",
    "pi": "π",
    "sin(": "sin(",
    "cos(": "cos(",
    "tan(": "tan("
};

// ACTUALIZAR LA PANTALLA

function actualizarPantalla() {
    let texto = expresion
        .map(valor => simbolos[valor] ?? valor)
        .join("");

    pantallaOperacion.textContent = texto;
}

// AGREGAR NUMEROS U OPERACIONES

function agregarValor(valor) {
    expresion.push(valor);

    actualizarPantalla();

    pantallaResultado.textContent = "0";
}

// BORRAR LA ULTIMA ENTRADA

function borrarUltimo() {
    expresion.pop();

    actualizarPantalla();

    pantallaResultado.textContent = "0";
}

// LIMPIAR TODA LA CALCULADORA

function limpiarCalculadora() {
    expresion = [];

    actualizarPantalla();

    pantallaResultado.textContent = "0";

    desactivarShift();
}

// ACTIVAR O DESACTIVAR SHIFT

function cambiarShift() {
    shiftActivo = !shiftActivo;

    indicadorShift.textContent = shiftActivo ? "SHIFT" : "";
}

// DESACTIVAR SHIFT

function desactivarShift() {
    shiftActivo = false;

    indicadorShift.textContent = "";
}

// CAMBIAR ENTRE GRADOS Y RADIANES

function cambiarModoAngulo() {
    modoAngulo = modoAngulo === "DEG" ? "RAD" : "DEG";

    indicador.textContent = modoAngulo;
}

// MOSTRAR U OCULTAR MENU

function cambiarMenu() {
    menuFunciones.hidden = !menuFunciones.hidden;
}

// PROCESAR BOTONES DE LA CALCULADORA

function procesarBoton(boton) {
    const valor = boton.dataset.value;
    const accion = boton.dataset.action;
    const funcion = boton.dataset.function;
    const valorShift = boton.dataset.shift;

    // FUNCIONES DEL MENU

    
if (funcion) {

    if (funcion === "modoAngulo") {
        cambiarModoAngulo();
        menuFunciones.hidden = true;
        return;
    }

    const funcionesMenu = {
        modulo: "modulo(",
        gradosRadianes: "gradosRadianes(",
        radianesGrados: "radianesGrados(",
        redondear: "redondear(",
        porcentaje: "porcentaje("
    };

    if (funcionesMenu[funcion]) {
        agregarValor(funcionesMenu[funcion]);
        desactivarShift();
        menuFunciones.hidden = true;
    }

    return;
}


    // BOTON SHIFT

    if (accion === "shift") {
        cambiarShift();
        return;
    }

    // FUNCIONES SECUNDARIAS

    if (shiftActivo && valorShift) {
        agregarValor(valorShift);
        desactivarShift();
        return;
    }

    // BOTONES CON ACCIONES

    if (accion) {
        switch (accion) {
            case "clear":
                limpiarCalculadora();
                break;

            case "del":
                borrarUltimo();
                break;

            case "mode":
                cambiarMenu();
                break;

            case "on":
                limpiarCalculadora();
                menuFunciones.hidden = true;
                break;

            case "close-menu":
                menuFunciones.hidden = true;
                break;

            case "ans":
                agregarValor("Ans");
                break;

            case "sign":
                agregarValor("-");
                break;

            case "equals":
                calcularResultado();
                break;

            default:
                pantallaResultado.textContent = "Pendiente";
                break;
        }

        return;
    }

    // BOTONES NUMERICOS Y MATEMATICOS

    if (valor !== undefined) {
        agregarValor(valor);
        desactivarShift();
    }
}

// DETECTAR CLICS EN LOS BOTONES

document.querySelectorAll("button").forEach(boton => {
    boton.addEventListener("click", () => {
        procesarBoton(boton);
    });
});

// ESTADO INICIAL

menuFunciones.hidden = true;
indicador.textContent = modoAngulo;

actualizarPantalla();


// ENVIAR LA OPERACION A PYTHON

async function calcularResultado() {

    if (expresion.length === 0) {
        return;
    }


    try {

        const respuesta = await fetch("/api/calcular", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                expresion: expresion,
                modoAngulo: modoAngulo,
                ans: ultimoResultado
     })
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            pantallaResultado.textContent =
                datos.error || "Error de cálculo";
            return;
        }

        ultimoResultado = datos.resultado;
        pantallaResultado.textContent = datos.resultado;
    } catch (error) {

        pantallaResultado.textContent = "Error de conexión";

        console.error(error);
    }
}
