FROM php:8.3-fpm

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    libpq-dev \
    nginx \
    && docker-php-ext-install pdo pdo_pgsql

COPY . .

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# ✅ Ensure Composer runs inside the container and installs dependencies
#  RUN composer install --no-dev --prefer-dist --no-interaction --no-progress

# ✅ Set correct permissions for Laravel storage & cache
#  RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

#  CMD ["php-fpm"]
