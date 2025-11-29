import socket
import json
from random import randint
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def check_hostname(request):
    return JsonResponse({
        'msg': 'Wassup Universe!!',
        'hostname': socket.gethostname()
    })

@csrf_exempt
def healthcheck(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'БД и приложуха доступны'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'произошла какая-то ошибка', 'error': str(e)}, status=500)


@csrf_exempt
def change_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS winners (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    prize INT
                )
            """)
            cursor.execute(
                "INSERT INTO winners (prize) VALUES (%s)",
                [str(randint(1, 1000))]
            )
            cursor.execute("SELECT * FROM winners")
            prize = cursor.fetchone()[0]

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Как же он хорош</title>
            </head>
            <body>
                <h1>Твой приз: ${prize}</h1>
                <h3>Сервер: {socket.gethostname()}</h3>
            </body>
            </html>
            """
            
            return HttpResponse(html_content, content_type='text/html; charset=utf-8')

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)