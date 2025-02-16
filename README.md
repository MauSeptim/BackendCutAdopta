# Instrucciones

El comando para instalar dependencias es este (hacerlo con el entorno virtual activado y en el mismo directorio del txt)
```
pip install -r requirements.txt
```


# CREAR EL ENTORNO VIRTUAL (Desde la carpeta raiz)

    python -m venv venv

# ACTIVAR EL ENTORNO VIRTUAL

    venv\Scripts\activate

# INSTALAR REQUIREMENTS

    pip install -r requirements.txt

# EJECUTAR EL SERVIDOR (Desde la carpeta donde se encuentra el main.py)

    uvicorn main:app --reload

# Especificando host y puerto:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
