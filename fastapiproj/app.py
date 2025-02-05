from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def new_route():
    return {'message': 'Feliz Natal!', 'anothermessage': 'Brutalist!'}
