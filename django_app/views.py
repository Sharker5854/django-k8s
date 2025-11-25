import socket
import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hostname_view(request):
    """Основная страница с hostname для проверки балансировки"""
    return JsonResponse({
        'message': 'Hello from Django with Vault and PostgreSQL!',
        'hostname': socket.gethostname(),
        'pod_ip': socket.gethostbyname(socket.gethostname())
    })

@csrf_exempt
def health_view(request):
    """Health check endpoint"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)

@csrf_exempt
def db_test_view(request):
    """Тестовый endpoint для работы с БД"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    message TEXT
                )
            """)
            cursor.execute(
                "INSERT INTO visits (message) VALUES (%s)",
                [f"Visit from {socket.gethostname()}"]
            )
            cursor.execute("SELECT COUNT(*) FROM visits")
            count = cursor.fetchone()[0]

        return JsonResponse({
            'hostname': socket.gethostname(),
            'total_visits': count,
            'message': 'Database operation completed successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)