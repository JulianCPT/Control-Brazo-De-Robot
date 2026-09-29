<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:6E0D0D,50:8E1616,100:B22222&height=220&section=header&text=Control%20de%20Brazo%20Rob%C3%B3tico&fontSize=44&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Simulaci%C3%B3n%20en%20PyBullet%20controlada%20por%20potenci%C3%B3metros&descAlignY=58&descSize=16)

*Ingeniería Mecatrónica · Universidad Militar Nueva Granada*

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=800&color=E63946&center=true&vCenter=true&width=560&lines=%22Girar+J1+%E2%86%92+rota+la+base%22;%22Girar+J2+%E2%86%92+mueve+el+codo%22;%22Girar+GRIP+%E2%86%92+abre%2Fcierra+la+pinza%22" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyBullet](https://img.shields.io/badge/PyBullet-Simulación%20física-E63946?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-Panel%20en%20vivo-A0522D?style=for-the-badge&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![Status](https://img.shields.io/badge/estado-académico-6E40C9?style=for-the-badge)

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## ✨ ¿Qué hace este proyecto?

Un **brazo robótico de 2 grados de libertad + pinza** se simula en tiempo real en
**PyBullet**, controlado físicamente por **3 potenciómetros** conectados a una **ESP32**.
Cada potenciómetro representa un ángulo (0°–180°) que la ESP32 lee y envía por **UART**;
Python recibe esos datos, los convierte a los límites reales de cada articulación del
`brazo.urdf` y mueve el robot en la simulación. Un **panel aparte en Tkinter** muestra en
vivo la posición y velocidad de cada articulación.

<div align="center">

| 🎛️ Potenciómetros | 📟 ESP32 | 🔌 Serie (USB) | 🐍 PyBullet + Tkinter |
|:---:|:---:|:---:|:---:|
| Generan el ángulo deseado (0°–180°) | Lee el ADC y arma el mensaje CSV | Envía `J1:.., J2:.., GRIP:..` | Mueve el robot y muestra el panel de estado |

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 📑 Contenido

- [🦾 Articulaciones y comportamiento del robot](#-articulaciones-y-comportamiento-del-robot)
- [📸 Capturas](#-capturas)
- [🎥 Videos de funcionamiento](#-videos-de-funcionamiento)
- [📐 Arquitectura general](#-arquitectura-general)
- [📁 Estructura del repositorio](#-estructura-del-repositorio)
- [⚙️ Requisitos](#️-requisitos)
- [▶️ Cómo correrlo](#️-cómo-correrlo)
- [📡 Protocolo de comunicación](#-protocolo-de-comunicación)
- [🧩 Explicación del código, bloque por bloque](#-explicación-del-código-bloque-por-bloque)
- [🧠 Conceptos clave](#-conceptos-clave)
- [🛠️ Solución de problemas](#️-solución-de-problemas)
- [👤 Autor](#-autor)

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 🦾 Articulaciones y comportamiento del robot

<div align="center">

| Señal | Joint(s) en el URDF | Tipo | Rango real | Comportamiento |
|:---:|:---|:---:|:---:|:---|
| **J1** | `joint_1` (base → brazo1) | revolute | -2.5 a 2.5 rad | Rota la **base** del brazo |
| **J2** | `joint_2` (brazo1 → brazo2) | revolute | -2.0 a 2.0 rad | Mueve el **codo** |
| **GRIP** | `joint_dedo_izq` + `joint_dedo_der` (en espejo) | prismatic | 0.0 a 0.04 m | Abre / cierra la **pinza** |

</div>

> 💡 `joint_gripper` (el bloque rojo de la pinza) es un joint **fijo**: no se mueve por sí
> solo, viaja siempre pegado al brazo. Lo único que se abre y cierra son los dos dedos,
> siempre en espejo, controlados por la misma señal `GRIP`.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 📸 Capturas

<div align="center">

<table>
  <tr>
    <td align="center">
      <img src="docs/im%C3%A1genes/Circuito%20con%20Potenciometros%20Manejo%20del%20Robot.jpeg" width="480"/><br/>
      <sub>Montaje físico: ESP32 + 3 potenciómetros</sub>
    </td>
    <td align="center">
      <img src="docs/im%C3%A1genes/Prueba%20Robot.jpeg" width="480"/><br/>
      <sub>Brazo simulado en PyBullet</sub>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <img src="docs/im%C3%A1genes/Prueba%20Robot%20Visualizando%20Manejo%20del%20Circuito.jpeg" width="480"/><br/>
      <sub>Circuito físico y simulación funcionando al mismo tiempo</sub>
    </td>
  </tr>
</table>

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 🎥 Videos de funcionamiento

> GitHub no reproduce videos `.mp4` alojados en el repo directamente dentro del README,
> así que se dejan como enlaces descargables/reproducibles desde el navegador, además de
> un GIF de vista rápida para cada uno.

- ▶️ [**Prueba del robot**](docs/videos/Prueba%20Robot.mp4) — el brazo respondiendo a los potenciómetros en PyBullet.
- ▶️ [**Prueba con el circuito visible**](docs/videos/Prueba%20Robot%20Visualizando%20Manejo%20del%20Circuito.mp4) — circuito físico y simulación al mismo tiempo.

<div align="center">

**GIF — el codo (J2) girando en la simulación:**

<img src="docs/videos/GIF%20Codo%20Robot.gif" width="480" alt="GIF del codo del robot en movimiento" />

**GIF — circuito físico controlando la simulación:**

<img src="docs/videos/GIF%20Circuito.gif" width="420" alt="GIF circuito y simulación" />

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 📐 Arquitectura general

<div align="center">

```
🎛️  Potenciómetros (J1, J2, GRIP)
        │  lectura ADC (0-4095)
        ▼
📟  ESP32 (esp32_sensores.ino)
        │  mapea a grados 0°-180°
        │  UART @ 115200 baudios, cada 100 ms
        │  "J1:120,J2:80,GRIP:45"
        ▼
🐍  main.py (PC)
        │  parsea la línea CSV
        │  convierte grados -> rango real del joint (brazo.urdf)
        ├──▶ 🦾 PyBullet: mueve joint_1, joint_2, dedos (POSITION_CONTROL)
        └──▶ 🖥️ Tkinter: panel con posición/velocidad en vivo
```

</div>

> 💡 **Idea clave:** la ESP32 **no sabe nada de robótica**. Solo lee 3 potenciómetros y
> los convierte a grados. Toda la lógica de conversión a radianes/metros, los límites del
> URDF y el control de posición viven en `main.py`, en la PC.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 📁 Estructura del repositorio

```
Control-Brazo-De-Robot/
├── main.py                     # Programa principal en Python (PC): PyBullet + panel Tkinter
├── brazo.urdf                  # Modelo del robot (base, brazo1, brazo2, pinza y dedos)
├── requirements.txt             # Dependencias de Python
├── esp32_sensores/
│   └── esp32_sensores.ino      # Firmware del ESP32: lee potenciómetros y envía por UART
├── docs/                       # Capturas y videos de demostración
│   ├── imágenes/
│   │   ├── Circuito con Potenciometros Manejo del Robot.jpeg
│   │   ├── Prueba Robot.jpeg
│   │   └── Prueba Robot Visualizando Manejo del Circuito.jpeg
│   └── videos/
│       ├── Prueba Robot.mp4
│       ├── Prueba Robot Visualizando Manejo del Circuito.mp4
│       ├── GIF Codo Robot.gif
│       └── GIF Circuito.gif
└── README.md
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## ⚙️ Requisitos

<div align="center">
<img src="https://skillicons.dev/icons?i=python,arduino,cpp&theme=dark" />
</div>

- ✅ Python 3.10+
- ✅ Una ESP32 con **3 potenciómetros** conectados a los pines ADC:
  - `J1` → GPIO 34 · `J2` → GPIO 35 · `GRIP` → GPIO 32 (VCC a 3.3 V, GND a GND)
- ✅ Arduino IDE con el paquete de placas **esp32 by Espressif Systems**
- ✅ Cable USB para conectar la ESP32 a la PC

**Instalación de dependencias de Python:**

```bash
pip install -r requirements.txt
```

> ℹ️ `pybullet_data`, `time`, `math` y `tkinter` vienen incluidos con PyBullet o con la
> instalación estándar de Python (en Linux puede requerir `sudo apt install python3-tk`).

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## ▶️ Cómo correrlo

1. **Sube el firmware** `esp32_sensores/esp32_sensores.ino` a la ESP32 desde el Arduino IDE.
2. **Conecta los 3 potenciómetros** según las conexiones sugeridas en el `.ino`.
3. **Edita el puerto serie** en `main.py`:
   ```python
   PUERTO = "COM3"   # Windows: "COM3", "COM4"...  |  Linux/Mac: "/dev/ttyUSB0", "/dev/ttyACM0"...
   ```
4. **Ejecuta la simulación:**
   ```bash
   python main.py
   ```
5. Se abren dos ventanas: la **simulación de PyBullet** y el **panel Tkinter** con la
   posición y velocidad de cada articulación. Mueve los potenciómetros y observa el brazo
   moverse en tiempo real.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 📡 Protocolo de comunicación

<div align="center">

| Campo | Significado | Rango enviado por ESP32 |
|:---:|:---|:---:|
| `J1` | Ángulo deseado de la base | 0° – 180° |
| `J2` | Ángulo deseado del codo | 0° – 180° |
| `GRIP` | Apertura deseada de la pinza | 0° – 180° |

</div>

Ejemplo de línea recibida por UART cada 100 ms:

```
J1:120,J2:80,GRIP:45
```

`main.py` convierte cada valor de 0°–180° al rango **real** del joint correspondiente
(radianes para `J1`/`J2`, metros para `GRIP`), usando los límites definidos en `brazo.urdf`.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 🧩 Explicación del código, bloque por bloque

### 1️⃣ `main.py` — control principal (PC)

<details>
<summary><b>⚙️ Límites reales de las articulaciones</b></summary>

```python
LIMITES = {
    "J1": {"joint": "joint_1", "min": -2.5, "max": 2.5, "force": 100, "max_velocity": 1.5},
    "J2": {"joint": "joint_2", "min": -2.0, "max": 2.0, "force": 80,  "max_velocity": 1.2},
}

DEDOS = {
    "joint_dedo_izq": {"min": 0.0, "max": 0.04, "force": 20, "max_velocity": 0.5},
    "joint_dedo_der": {"min": 0.0, "max": 0.04, "force": 20, "max_velocity": 0.5},
}
```

Estos diccionarios se toman directamente del `brazo.urdf`. `J1` y `J2` se mueven en
radianes; los dedos se mueven en metros (0 a 0.04 m), siempre en espejo, para que la
apertura máxima quede alineada con el borde del bloque de la pinza.

</details>

<details>
<summary><b>🔄 De grados de potenciómetro a valor real del joint</b></summary>

```python
def grados_a_valor_joint(grados, minimo, maximo):
    grados = max(0, min(180, grados))
    return minimo + (grados / 180.0) * (maximo - minimo)
```

Convierte el ángulo 0°–180° del potenciómetro a una interpolación lineal dentro del rango
real del joint (por ejemplo, 90° en `J1` → 0 rad, el centro del rango -2.5 a 2.5).

</details>

<details>
<summary><b>📩 Parseo de la línea UART</b></summary>

```python
def parsear_linea(linea):
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
```

Convierte `"J1:120,J2:80,GRIP:45"` en `{'J1': 120.0, 'J2': 80.0, 'GRIP': 45.0}`. Si la
línea llega incompleta o corrupta (ruido típico de UART), devuelve `None` en vez de
lanzar un error.

</details>

<details>
<summary><b>🦾 Aplicar la lectura al robot</b></summary>

```python
def mover_joint(robot_id, indice, valor, force=200):
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=indice,
        controlMode=p.POSITION_CONTROL,
        targetPosition=valor,
        force=force,
    )

def aplicar_lectura(robot_id, nombre_a_indice, datos):
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
```

`J1` y `J2` mueven el brazo directamente. `GRIP` se trata distinto: convierte el ángulo a
una fracción 0–1 y mueve **ambos dedos a la vez, en espejo**, cada uno con su propio
`force`.

</details>

<details>
<summary><b>🖥️ Panel Tkinter en tiempo real</b></summary>

```python
ventana, etiquetas_valor = crear_panel()
```

`crear_panel()` construye una ventana aparte con una tabla (articulación / posición /
velocidad) para **J1 (base)**, **J2 (codo)** y **Pinza**. `actualizar_panel()` lee
`p.getJointState(...)` para cada joint, convierte posición a grados y velocidad a
grados/s (mm/s para la pinza), y refresca las etiquetas con `ventana.update_idletasks()` +
`ventana.update()` — sin bloquear el bucle de simulación. Si el usuario cierra la
ventana, la función devuelve `False` para poder salir del bucle principal limpiamente.

</details>

<details>
<summary><b>🔁 Bucle principal</b></summary>

```python
while True:
    linea = ser.readline().decode("utf-8", errors="ignore")
    datos = parsear_linea(linea)
    if datos:
        aplicar_lectura(robot_id, nombre_a_indice, datos)

    p.stepSimulation()

    panel_abierto = actualizar_panel(ventana_panel, etiquetas_valor, robot_id, nombre_a_indice)
    if not panel_abierto:
        break

    time.sleep(0.01)
```

Repite: leer UART → aplicar al robot → avanzar la física de PyBullet → refrescar el
panel. `time.sleep(0.01)` evita saturar la CPU sin afectar la fluidez percibida.

</details>

### 2️⃣ `esp32_sensores.ino` — firmware del ESP32

> 🧠 **Filosofía del sketch:** este programa **no controla el robot**, solo lee 3
> potenciómetros y reporta sus ángulos por UART.

<details>
<summary><b>📥 Lectura y envío periódico</b></summary>

```cpp
if (ahora - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = ahora;

    int lecturaJ1   = analogRead(PIN_J1);
    int lecturaJ2   = analogRead(PIN_J2);
    int lecturaGrip = analogRead(PIN_GRIP);

    int gradosJ1   = map(lecturaJ1,   0, ADC_MAX, ANGULO_MIN, ANGULO_MAX);
    int gradosJ2   = map(lecturaJ2,   0, ADC_MAX, ANGULO_MIN, ANGULO_MAX);
    int gradosGrip = map(lecturaGrip, 0, ADC_MAX, ANGULO_MIN, ANGULO_MAX);

    Serial.print("J1:"); Serial.print(gradosJ1);
    Serial.print(",J2:"); Serial.print(gradosJ2);
    Serial.print(",GRIP:"); Serial.println(gradosGrip);
}
```

Cada 100 ms lee los 3 pines ADC (12 bits, 0–4095) y los mapea a 0°–180° con `map()`, luego
imprime la línea CSV que `main.py` va a parsear.

</details>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 🧠 Conceptos clave

<details>
<summary><b>🦴 URDF (Unified Robot Description Format)</b></summary>

Formato XML que describe un robot como un árbol de **links** (cuerpos rígidos) unidos por
**joints** (articulaciones), con sus límites, masas e inercias. PyBullet carga `brazo.urdf`
con `p.loadURDF(...)` para simular la física del brazo.

</details>

<details>
<summary><b>🔩 Joint revolute vs. prismatic</b></summary>

Un **joint revolute** (`joint_1`, `joint_2`) gira alrededor de un eje, en radianes. Un
**joint prismatic** (`joint_dedo_izq`, `joint_dedo_der`) se desliza en línea recta, en
metros. Por eso `J1`/`J2` y `GRIP` usan escalas distintas al convertir grados.

</details>

<details>
<summary><b>🎯 POSITION_CONTROL en PyBullet</b></summary>

Modo de control donde se le indica al motor del joint una posición objetivo
(`targetPosition`) y una fuerza máxima (`force`); el motor interno de PyBullet calcula el
torque necesario para llegar allí, similar a un servo real.

</details>

<details>
<summary><b>🔌 Comunicación serie (UART/USB)</b></summary>

Forma simple de que una PC y un microcontrolador se hablen: un cable USB por el que viajan
bytes, línea por línea. Aquí la ESP32 envía texto (`"J1:120,J2:80,GRIP:45\n"`) y Python lo
lee con `ser.readline()`.

</details>

<details>
<summary><b>📊 ADC (Convertidor Analógico-Digital)</b></summary>

Convierte un voltaje analógico (el que entrega cada potenciómetro) en un número digital.
La ESP32 usa 12 bits de resolución, es decir, valores de 0 a 4095.

</details>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

## 🛠️ Solución de problemas

| Problema | Posible solución |
|:---|:---|
| `ModuleNotFoundError` (`pybullet`, `serial`) | Ejecuta `pip install pybullet pyserial` |
| No se encuentra `brazo.urdf` | Ejecuta `main.py` desde la carpeta raíz del repositorio |
| No se pudo conectar al ESP32 | Verifica `PUERTO` en `main.py` y cierra el Monitor Serial del Arduino IDE |
| El brazo no se mueve | Confirma que el ESP32 esté enviando datos (Monitor Serial) y que `PUERTO` sea correcto |
| El panel Tkinter no abre / error de Tk | En Linux instala `sudo apt install python3-tk` |
| Los dedos no se abren igual | Revisa que ambos potenciómetros de `GRIP` compartan la misma señal (solo hay un `GRIP`) |

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:6E0D0D,100:B22222&height=3&section=header" width="100%"/>

<div align="center">

## 👤 Autor

**Julián** · Ingeniería Mecatrónica · Universidad Militar Nueva Granada

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:B22222,50:8E1616,100:6E0D0D&height=120&section=footer)

</div>
