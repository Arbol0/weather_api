# Imagen base oficial de Python 3.8
FROM python:3.8-slim

# Directorio de trabajo
WORKDIR /app

# Copiar Pipfile y Pipfile.lock
COPY Pipfile* ./

# Instalar pipenv
RUN pip install --no-cache-dir pipenv

# Instalar dependencias del Pipfile
RUN pipenv install --system --deploy

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto para correr Django en modo desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

