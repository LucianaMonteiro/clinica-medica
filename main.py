from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import urllib.parse as html
import time


import db
import db_init

ERR_MSG = "Todos os campos precisam ser preenchidos!"
LEN_PAGE = 5

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

    body.pop("page", None)
    return body


async def get_params(req: Request):
    payload = req.query_params

    try:
        params = dict(payload)
    except:
        params = None

    return params


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


# PACIENTES:


@app.get("/api/pacientes", response_class=JSONResponse)
async def pacientes(params=Depends(get_params)):
    if params:
        key = "page"
        page = int(params[key]) if key in params else 0
        page = 0 if page < 0 else page
        dados = db.get_pacientes_paged(LEN_PAGE, page)
        return dados
    else:
        return db.get_pacientes()


@app.get("/api/pacientes/{id}")
async def pacientes(id: int):
    dados = db.get_paciente(id)
    return JSONResponse(dados)


@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_paciente(id: int, body=Depends(get_body)):
    if is_valid(body, 15):
        db.update_paciente(id, body)
        nome = body["nome"]
        dados = db.get_pacientes_position(nome, LEN_PAGE)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/pacientes", response_class=JSONResponse)
async def add_paciente(body=Depends(get_body)):
    if is_valid(body, 15):
        nome = body["nome"]
        db.add_paciente(body)
        dados = db.get_pacientes_position(nome, LEN_PAGE)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/pacientes/search", response_class=JSONResponse)
async def get_pacientes(body=Depends(get_body)):
    key = "search"
    search = body[key] if key in body else ""

    if len(search) > 1:
        dados = db.search_pacientes(search)
    else:
        dados = db.get_pacientes_paged(LEN_PAGE)

    return dados


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def paciente(id: int):
    db.del_paciente(id)
    return ""


# MÉDICOS:


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos(params=Depends(get_params)):
    if params:
        key = "page"
        page = int(params[key]) if key in params else 0
        page = 0 if page < 0 else page
        dados = db.get_medicos_paged(LEN_PAGE, page)
        return dados
    else:
        return db.get_medicos()


@app.get("/api/medicos/{id}")
async def medicos(id: int):
    dados = db.get_medico(id)
    return JSONResponse(dados)


@app.put("/api/medicos/{id}", response_class=JSONResponse)
async def update_medico(id: int, body=Depends(get_body)):
    if is_valid(body, 15):
        db.update_medico(id, body)
        nome = body["nome"]
        dados = db.get_medicos_position(nome, LEN_PAGE)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/medicos", response_class=JSONResponse)
async def add_medico(body=Depends(get_body)):
    if is_valid(body, 15):
        nome = body["nome"]
        db.add_medico(body)
        dados = db.get_medicos_position(nome, LEN_PAGE)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/medicos/search", response_class=JSONResponse)
async def get_medicos(body=Depends(get_body)):
    key = "search"
    search = body[key] if key in body else ""

    if len(search) > 1:
        dados = db.search_medicos(search)
    else:
        dados = db.get_medicos_paged(LEN_PAGE)

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


def is_valid(body: dict, qtd: int):
    return sum([1 if v else 0 for _, v in body.items()]) == qtd


# Ler o arquivo com o fragmento e retornar uma string:
def fragment(arq_name):
    html = open(
        f"./static/fragments/{arq_name}.html", "r", encoding="utf-8"
    ).readlines()
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
