import pybullet as p
import pybullet_data
import time
import math
import serial
import tkinter as tk

# ------------------------------------------------------------
# CONFIGURACION UART - ajusta el puerto segun tu computador
#   Windows: "COM3", "COM4", ...
#   Linux/Mac: "/dev/ttyUSB0", "/dev/ttyACM0", ...
# ------------------------------------------------------------
PUERTO = "COM3"
BAUDIOS = 115200

# ------------------------------------------------------------
# Limites reales de los joints que SI se mueven (tomados del brazo.urdf).
# joint_gripper ya no esta aqui: ahora es un joint "fixed", el bloque rojo
# queda siempre pegado al brazo naranja. Solo J1, J2 y los dedos se mueven.
# ------------------------------------------------------------
LIMITES = {
    "J1": {"joint": "joint_1", "min": -2.5, "max": 2.5, "force": 100, "max_velocity": 1.5},
    "J2": {"joint": "joint_2", "min": -2.0, "max": 2.0, "force": 80,  "max_velocity": 1.2},
}

# Los dos dedos se mueven en espejo, controlados por el mismo GRIP.
# max=0.04 coincide con el limite del URDF: en apertura maxima, el borde
# interno de cada dedo queda alineado con el borde externo del bloque rojo.
DEDOS = {
    "joint_dedo_izq": {"min": 0.0, "max": 0.04, "force": 20, "max_velocity": 0.5},
    "joint_dedo_der": {"min": 0.0, "max": 0.04, "force": 20, "max_velocity": 0.5},
}


def grados_a_valor_joint(grados, minimo, maximo):
    """Convierte un angulo de potenciometro (0-180) al rango real del joint."""
    grados = max(0, min(180, grados))
    return minimo + (grados / 180.0) * (maximo - minimo)


def parsear_linea(linea):
    """Convierte 'J1:120,J2:80,GRIP:45' en {'J1':120.0,'J2':80.0,'GRIP':45.0}."""
    linea = linea.strip()
    if not linea or ":" not in linea:
        return None
    try:
        datos = {}
        for parte in linea.split(","):
            clave, valor = parte.split(":")
            datos[clave.strip()] = float(valor.strip())
        return datos
    except ValueError:
        return None


def mover_joint(robot_id, indice, valor, force=200):
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=indice,
        controlMode=p.POSITION_CONTROL,
        targetPosition=valor,
        force=force,
    )


def aplicar_lectura(robot_id, nombre_a_indice, datos):
    """Mueve los joints del robot segun los datos recibidos por UART.
    J1 y J2 mueven el brazo. GRIP mueve SOLO los dos dedos (en espejo);
    el bloque rojo (gripper_base) ya no se mueve, queda fijo al brazo."""
    for clave, grados in datos.items():
        if clave in LIMITES:
            cfg = LIMITES[clave]
            valor = grados_a_valor_joint(grados, cfg["min"], cfg["max"])
            indice = nombre_a_indice.get(cfg["joint"])
            if indice is not None:
                mover_joint(robot_id, indice, valor)

        elif clave == "GRIP":
            frac = max(0.0, min(180.0, grados)) / 180.0
            for nombre_dedo, lim in DEDOS.items():
                valor_dedo = lim["min"] + frac * (lim["max"] - lim["min"])
                indice_dedo = nombre_a_indice.get(nombre_dedo)
                if indice_dedo is not None:
                    mover_joint(robot_id, indice_dedo, valor_dedo, force=lim["force"])


def crear_panel():
    """Crea una ventana aparte (Tkinter) con una tabla que muestra la
    posicion y velocidad de cada articulacion. Se actualiza en tiempo real
    sin bloquear la simulacion de PyBullet."""
    ventana = tk.Tk()
    ventana.title("Estado del brazo (grados y velocidad)")
    ventana.geometry("360x160")
    ventana.resizable(False, False)

    fuente_encabezado = ("Consolas", 11, "bold")
    fuente_dato = ("Consolas", 11)

    encabezados = ["Articulacion", "Posicion", "Velocidad"]
    for col, texto in enumerate(encabezados):
        tk.Label(ventana, text=texto, font=fuente_encabezado, borderwidth=1,
                  relief="solid", width=14, bg="#dddddd").grid(row=0, column=col)

    filas = ["J1 (base)", "J2 (codo)", "Pinza"]
    etiquetas_valor = {}
    for fila, nombre in enumerate(filas, start=1):
        tk.Label(ventana, text=nombre, font=fuente_dato, borderwidth=1,
                  relief="solid", width=14).grid(row=fila, column=0)

        lbl_pos = tk.Label(ventana, text="--", font=fuente_dato, borderwidth=1,
                            relief="solid", width=14)
        lbl_pos.grid(row=fila, column=1)

        lbl_vel = tk.Label(ventana, text="--", font=fuente_dato, borderwidth=1,
                            relief="solid", width=14)
        lbl_vel.grid(row=fila, column=2)

        etiquetas_valor[nombre] = (lbl_pos, lbl_vel)

    return ventana, etiquetas_valor


def actualizar_panel(ventana, etiquetas_valor, robot_id, nombre_a_indice):
    """Lee posicion/velocidad de cada joint y actualiza el panel Tkinter.
    Devuelve False si el usuario cerro la ventana (para poder salir del
    bucle principal sin lanzar error)."""
    idx_j1 = nombre_a_indice.get("joint_1")
    idx_j2 = nombre_a_indice.get("joint_2")
    idx_dedo = nombre_a_indice.get("joint_dedo_izq")  # los dos dedos van en espejo

    j1_pos, j1_vel = p.getJointState(robot_id, idx_j1)[0:2] if idx_j1 is not None else (0.0, 0.0)
    j2_pos, j2_vel = p.getJointState(robot_id, idx_j2)[0:2] if idx_j2 is not None else (0.0, 0.0)
    dedo_pos, dedo_vel = p.getJointState(robot_id, idx_dedo)[0:2] if idx_dedo is not None else (0.0, 0.0)

    j1_deg, j1_vel_deg_s = math.degrees(j1_pos), math.degrees(j1_vel)
    j2_deg, j2_vel_deg_s = math.degrees(j2_pos), math.degrees(j2_vel)
    grip_pct = (dedo_pos / DEDOS["joint_dedo_izq"]["max"]) * 100.0
    grip_vel_mm_s = dedo_vel * 1000.0

    try:
        lbl_pos, lbl_vel = etiquetas_valor["J1 (base)"]
        lbl_pos.config(text=f"{j1_deg:6.1f} deg")
        lbl_vel.config(text=f"{j1_vel_deg_s:6.1f} deg/s")

        lbl_pos, lbl_vel = etiquetas_valor["J2 (codo)"]
        lbl_pos.config(text=f"{j2_deg:6.1f} deg")
        lbl_vel.config(text=f"{j2_vel_deg_s:6.1f} deg/s")

        lbl_pos, lbl_vel = etiquetas_valor["Pinza"]
        lbl_pos.config(text=f"{grip_pct:5.1f} %")
        lbl_vel.config(text=f"{grip_vel_mm_s:6.1f} mm/s")

        ventana.update_idletasks()
        ventana.update()
        return True
    except tk.TclError:
        # El usuario cerro la ventana del panel
        return False


# ------------------------------------------------------------
# Conectar a PyBullet
# ------------------------------------------------------------
physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Cargar el robot (con masas/inercias -> ya no se separa la pinza)
robot_id = p.loadURDF("brazo.urdf", [0, 0, 0], useFixedBase=True)

# Verificar articulaciones
num_joints = p.getNumJoints(robot_id)
print(f"Articulaciones encontradas: {num_joints}")

nombre_a_indice = {}
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    nombre = info[1].decode("utf-8")
    nombre_a_indice[nombre] = i
    print(f"Joint {i}: {nombre} (tipo: {info[2]})")

# ------------------------------------------------------------
# Crear el panel aparte con la tabla de grados/velocidad
# ------------------------------------------------------------
ventana_panel, etiquetas_valor = crear_panel()

# ------------------------------------------------------------
# Conectar al ESP32 por UART
# ------------------------------------------------------------
print(f"Conectando al puerto {PUERTO} a {BAUDIOS} baudios...")
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)  # esperar a que el ESP32 reinicie tras abrir el puerto
print("Conectado. Escuchando datos UART (Ctrl+C para salir)...")

# ------------------------------------------------------------
# Bucle principal: leer UART, mover el robot y actualizar el panel
# ------------------------------------------------------------
try:
    while True:
        linea = ser.readline().decode("utf-8", errors="ignore")
        datos = parsear_linea(linea)
        if datos:
            aplicar_lectura(robot_id, nombre_a_indice, datos)
            print(f"Recibido: {datos}")

        p.stepSimulation()

        panel_abierto = actualizar_panel(ventana_panel, etiquetas_valor, robot_id, nombre_a_indice)
        if not panel_abierto:
            print("Panel cerrado por el usuario, terminando...")
            break

        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nFinalizado por el usuario.")
finally:
    ser.close()
    p.disconnect()
