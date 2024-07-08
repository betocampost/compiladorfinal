Para instalar las dependencias primero estar en la carpeta del proyecto y ejecutar el siguiente comando:
Antes que nada instalar la primera opcion del siguiente link
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/tag/2022-01-04

1.-ejecutarla y despues instalarla
2.-reiniciar el visual studio code
3.- ejecutar el programa main.py


En Windows:

```bash
python -m venv env
```

En Linux:

```bash
python3 -m venv env
```

Luego activar el entorno virtual:

En Windows:

```bash
env\Scripts\activate
```

En Linux:

```bash
source env/bin/activate
```

Luego instalar las dependencias:

```bash
pip install -r requirements.txt
```

Si no estas en la carpeta del proyecto, puedes ejecutar el siguiente comando:

```bash
cd /path/to/project
pip install -r requirements.txt
```
