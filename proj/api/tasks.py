from proj.celery import app
@app.task
def prueba():
    print(hola)
