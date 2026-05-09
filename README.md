# 🐢 TurtleSurvival

¡Bienvenido a **TurtleSurvival**! Un juego de supervivencia desarrollado en Python utilizando la librería **Arcade** desarrollado por Bianca Stefania Amariutei.


---


## 🛠️ Requisitos Previos

Antes de empezar, asegúrate de tener instalado:
* **Python 3.10, 3.11 o 3.12** (Recomendado 3.12 para evitar problemas de compilación).
* **Git** (para clonar el repositorio).


---


## 🚀 Cómo ejecutar el juego (Modo Desarrollo)

Si quieres ejecutar el código fuente en tu ordenador, sigue estos pasos:

### 1. Clonar el proyecto

Si aún no tienes el código, clona el repositorio:
```bash
git clone https://github.com/bianca-stam/TurtleSurvival
cd TurtleSurvival
```

### 2. Configurar el Entorno Virtual

Es recomendable usar un entorno virtual para mantener las dependencias limpias. Debes usar la versión 3.12.x de Python para no tener problemas con las dependencias.
En Windows:
```PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\activate
```

### 3. Instalar Dependencias

Instala las librerías necesarias (Arcade, Pymunk, etc.):
```PowerShell
pip install -r requirements.txt
```

### 4. Iniciar el juego

```PowerShell
python TurtleSurvival.py
```


---


## 🎮 Cómo Jugar

Para iniciar el juego desde la terminal, ejecuta:

```PowerShell
python TurtleSurvival.py
```

Controles:

Flechas / WASD: Mover a la tortuga.

---

## 📦 Cómo exportar a Ejecutable (.exe)

Para crear un archivo que tus amigos puedan jugar sin instalar Python, usamos PyInstaller.

### 1. Instalar PyInstaller

```PowerShell
pip install pyinstaller
```

### 2. Generar el ejecutable

Ejecuta el siguiente comando en la terminal (asegúrate de que la carpeta assets esté en la raíz):

```PowerShell
pyinstaller --noconsole --clean -n "TurtleSurvival" --add-data "assets;assets" TurtleSurvival.py
```

### 3. Dónde encontrar el juego

Una vez finalizado, ve a la carpeta `dist/TurtleSurvival/`.

El archivo para jugar es TurtleSurvival.exe.

¡Importante!: Para compartirlo, debes comprimir toda la carpeta TurtleSurvival (la que está dentro de dist) en un archivo .zip y enviársela a tus amigos. El .exe no funcionará si está fuera de su carpeta.


---


## 🎨 Créditos y Atribuciones

### Desarrollo
* **Programación y Lógica:** Bianca Stefania Amariutei.
* **Motor Gráfico:** [Arcade Library](https://api.arcade.academy/).

### Recursos de Arte
Este juego utiliza recursos de arte de **[CraftPix](https://craftpix.net/)**. Los assets se utilizan bajo los términos de la **Licencia de CraftPix**, que permite su uso en proyectos de juegos comerciales y personales, cumpliendo con los requisitos de atribución para recursos gratuitos.


---


## 📄 Licencia
Este proyecto es de código abierto y está disponible bajo la licencia **MIT**.
