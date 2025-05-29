# Sistema de Nodos Incrementales con Docker Compose

Este proyecto implementa una aplicación distribuida de nodos que se pasan un valor incrementalmente usando Flask y Docker.

---

## Contenido del repositorio

- `node.py` — Código Python que ejecuta el servidor Flask para cada nodo.
- `Dockerfile` — Imagen Docker para construir el contenedor con Python y dependencias.
- `docker-compose.yaml` — Orquestación de varios nodos con diferentes variables de entorno.

---

## Requisitos previos

- Tener instalado Docker y Docker Compose.
- Acceso a terminal / consola.

---

## Pasos para ejecutar la aplicación

### 1. Clonar el repositorio 

```bash
git clone https://github.com/CarlosBauluz/P5_Distribuidos.git
cd https://github.com/CarlosBauluz/P5_Distribuidos.git

### 2. Comando para crear imagen, contenedores y ejecutarlo (Se ejecuta en la carpeta raiz)

```bash
docker compose up

### 3. Acceder al programa

Para acceder al programa se tendrá que acceder al localhost:5000 trás el docker compose up y ahí ya se podrá ejecutar.
#### IMPORTANTE: PARA VER LOS VALORES ACTUALIZADOS EN LA PESTAÑA, HAY QUE RECARGARLA MANUALMENTE

### 4. Desinstalar/Borrar el programa

Lo primero es realizar control + c

Después se realiza el comando: 

```bash
docker compose down

Por último se accede a docker y se borra manualmente la imagen residual que queda ahí guardada.
