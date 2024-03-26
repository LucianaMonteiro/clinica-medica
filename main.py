from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import urllib.parse as html
import time


import db
import db_init

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
    # time.sleep(2)
    return db.get_pacientes()


@app.get("/api/pacientes/{id}")
async def pacientes(id: int):
    dados = db.get_paciente(id)
    return JSONResponse(dados)


@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_paciente(id: int, body=Depends(get_body)):
    if is_valid(body, 11):
        db.update_paciente(id, body)
        dados = db.get_pacientes()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/pacientes", response_class=JSONResponse)
async def add_paciente(body=Depends(get_body)):
    if is_valid(body, 11):
        db.add_paciente(body)

        dados = db.get_pacientes()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)

@app.post("/api/pacientes/search", response_class=JSONResponse)
async def get_pacientes(body=Depends(get_body)):
    busca = body["search"]
    dados = db.get_pacientes() if len(busca) < 2 else db.search_pacientes(busca)
    return dados

@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def paciente(id: int):
    db.del_paciente(id)
    return ""


# MÉDICOS:


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos():
    # time.sleep(2)
    return db.get_medicos()


@app.get("/api/medicos/{id}")
async def medicos(id: int):
    dados = db.get_medico(id)
    return JSONResponse(dados)


@app.put("/api/medicos/{id}", response_class=JSONResponse)
async def update_medico(id: int, body=Depends(get_body)):
    if is_valid(body, 11):
        db.update_medico(id, body)
        dados = db.get_medicos()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/medicos", response_class=JSONResponse)
async def add_medico(body=Depends(get_body)):
    if is_valid(body, 11):
        db.add_medico(body)
        dados = db.get_medicos()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)
    
@app.post("/api/medicos/search", response_class=JSONResponse)
async def get_medicos(body=Depends(get_body)):
    search = body["search"]
    dados = db.get_medicos() if len(search) < 2 else db.search_medicos(search)
    return dados


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medico(id: int):
    db.del_medico(id)
    return ""

# ----------------------------- #
#    Retornar fragmentos HTML   #
# ----------------------------- #


# reotornar template para adicionar paciente:
@app.get("/html/pacientes/new/add", response_class=HTMLResponse)
async def add_paciente():
    html = fragment("paciente_add")
    return html

# retornar template para editar paciente:
@app.get("/html/pacientes/{id}/edit", response_class=HTMLResponse)
async def edit_paciente(id: int):
    dados = db.get_paciente(id)
    return fragment_format(dados, "paciente_edit")

# reotornar template para detalhar paciente:
@app.get("/html/pacientes/{id}/detalhe", response_class=HTMLResponse)
async def detalhe_paciente(id: int):
    dados = db.get_paciente(id)
    return fragment_format(dados, "paciente_detalhe")

# reotornar template para adicionar médico:
@app.get("/html/medicos/new/add", response_class=HTMLResponse)
async def add_medico():
    html = fragment("medico_add")
    return html

# reotornar template para editar médico:
@app.get("/html/medicos/{id}/edit", response_class=HTMLResponse)
async def edit_medico(id: int):
    dados = db.get_medico(id)
    return fragment_format(dados, "medico_edit")

# reotornar template para detalhar médico:
@app.get("/html/medicos/{id}/detalhe", response_class=HTMLResponse)
async def detalhe_medico(id: int):
    dados = db.get_medico(id)
    return fragment_format(dados, "medico_detalhe")

# Ler o arquivo com o fragmento e retornar uma string:
def fragment(arq_name):
    html = open(f"./static/fragments/{arq_name}.html", "r", encoding='utf-8').readlines()
    return "".join(html)

# Devolver a string html preenchida com os valores fornecidos:
def fragment_format(dados, arq_name):
    if dados:
        html = fragment(arq_name)
        html = html.format(**dados[0])
        return html
    else:
        raise HTTPException(status_code=404)

# --------------------------------------- #
# Funções auxiliares e endpoints de teste #
# --------------------------------------- #
    
    
# resetar o banco de dados:
@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    db_init.tables_init()
    return "/app/home.html"


def is_valid(body: dict, qtd: int):
    return sum([1 if v else 0 for _, v in body.items()]) == qtd