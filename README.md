Para instalar las dependencias primero estar en la carpeta del proyecto y ejecutar el siguiente comando:

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
