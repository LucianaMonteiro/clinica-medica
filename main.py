from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import urllib.parse as html
import time


import db
import db_init
import static.fragments.html_add as add
import static.fragments.html_edit as edit

ERR_MSG = "Todos os campos precisam ser preenchidos!"

app = FastAPI()
app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


async def get_body(req: Request):
    payload = await req.body()
    payload = payload.decode("utf8")
    payload = html.unquote(payload)

    try:
        body = json.loads(payload)
    except:
        lista = list(payload.split("&"))
        body = dict(l.split("=") for l in lista)

    return body


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


# PACIENTES:


@app.get("/api/pacientes")
async def pacientes():
    time.sleep(2)
    return db.get_pacientes()


@app.get("/api/pacientes/{id}")
async def pacientes(id: int):
    dados = db.get_paciente(id)
    return JSONResponse(dados)


@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_paciente(id: int, body=Depends(get_body)):
    if is_valid(body, 4):
        db.update_paciente(id, body)
        dados = db.get_pacientes()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/pacientes", response_class=JSONResponse)
async def add_paciente(body=Depends(get_body)):
    if is_valid(body, 4):
        db.add_paciente(body)

        dados = db.get_pacientes()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def paciente(id: int):
    db.del_paciente(id)
    return ""


# MÉDICOS:


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos():
    time.sleep(2)
    return db.get_medicos()


@app.put("/api/medicos/{id}", response_class=JSONResponse)
async def update_medico(id: int, body=Depends(get_body)):
    if is_valid(body, 6):
        db.update_medico(id, body)
        dados = db.get_medicos()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/medicos", response_class=JSONResponse)
async def add_medico(body=Depends(get_body)):
    if is_valid(body, 6):
        db.add_medico(body)
        dados = db.get_medicos()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medico(id: int):
    db.del_medico(id)
    return ""


# reotornar template para adicionar paciente:
@app.get("/api/pacientes/0/add", response_class=HTMLResponse)
async def add_paciente():
    return add.paciente_html()


# reotornar template para adicionar médico:
@app.get("/api/medicos/0/add", response_class=HTMLResponse)
async def add_medico():
    return add.medico_html()


# retornar template para editar paciente:
@app.get("/api/pacientes/{id}/edit", response_class=HTMLResponse)
async def edit_paciente(id: int):
    paciente = db.get_paciente(id)

    if paciente:
        dados = paciente[0]
        return edit.paciente_html(dados)
    else:
        raise HTTPException(status_code=404)


@app.get("/api/medicos/{id}/edit", response_class=HTMLResponse)
async def edit_medico(id: int):
    medico = db.get_medico(id)

    if medico:
        dados = medico[0]
        return edit.medico_html(dados)
    else:
        raise HTTPException(status_code=404)


# resetar o banco de dados:
@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    db_init.tables_init()
    return "/app/home.html"


def is_valid(body: dict, qtd: int):
    return sum([1 if v else 0 for _, v in body.items()]) == qtd
