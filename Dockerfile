FROM python:3.12

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expor porta padrão do Django
EXPOSE 8000

# Rodar migrações e iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
