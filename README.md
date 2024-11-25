python3.11 -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
O
pip install fastapi uvicorn python-dotenv google-auth google-auth-oauthlib google-api-python-client


6. Ejecutar la Aplicación
Inicia la aplicación con Uvicorn:

bash
Copy code
uvicorn app.main:app --reload
La aplicación estará disponible en http://localhost:8000.

Pruebas Adicionales
Para probar que todo funciona correctamente, puedes también acceder a la documentación automática que proporciona FastAPI:

Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
Aquí podrás ver y probar todos los endpoints disponibles.