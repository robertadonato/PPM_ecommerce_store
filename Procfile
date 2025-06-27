release: bash -c "mkdir -p /app/media/products && cp -r media/products/* /app/media/products/ && python manage.py loaddata shop/all_data.json"
web: bash -c "mkdir -p /app/staticfiles && python manage.py collectstatic --noinput && gunicorn ecommerce_project.wsgi:application --preload --bind 0.0.0.0:$PORT"
