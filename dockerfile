# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Apache and mod_wsgi
RUN apt-get update && apt-get install -y \
    apache2 \
    apache2-dev \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    libapache2-mod-wsgi-py3 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install mod_wsgi for Apache-Python integration
RUN pip install mod_wsgi

# Configure mod_wsgi for Apache
RUN mod_wsgi-express install-module > /etc/apache2/mods-available/wsgi.load \
    && a2enmod wsgi

# Add ServerName directive globally to suppress warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf


# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure static files are collected properly
RUN python manage.py collectstatic --noinput

# Apache configuration
RUN echo '<VirtualHost *:80>\n\
    ServerName localhost\n\
    DocumentRoot /app\n\
    \n\
    WSGIDaemonProcess unisda_strategic_plan python-path=/app\n\
    WSGIProcessGroup unisda_strategic_plan\n\
    WSGIScriptAlias / /app/unisda_strategic_plan/wsgi.py\n\
    \n\
    <Directory /app/unisda_strategic_plan>\n\
        <Files wsgi.py>\n\
            Require all granted\n\
        </Files>\n\
    </Directory>\n\
    \n\
    Alias /static/ /app/staticfiles/\n\
    <Directory /app/staticfiles>\n\
        Require all granted\n\
    </Directory>\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Enable the Apache site
RUN a2ensite 000-default

# Expose port 80
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]
