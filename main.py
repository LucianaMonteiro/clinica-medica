from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import urllib.parse as html
import time


import db
import db_init
import static.fragments.html_edit as edit

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
async def pacientes(id):
    dados = db.get_paciente(id)
    return JSONResponse(dados)

@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_pacientes(id, body=Depends(get_body)):
    db.update_pacientes(id, body)
    dados = db.get_pacientes()
    return dados

@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def paciente(id: str):
    db.del_paciente(id)
    return ""

# MÉDICOS:

@app.get("/api/medicos", response_class=JSONResponse)
async def medicos():
    time.sleep(2)
    return db.get_medicos()

@app.put("/api/medicos/{id}", response_class=JSONResponse)
async def update_medicos(id, body=Depends(get_body)):
    db.update_medicos(id, body)
    dados = db.get_medicos()
    return dados

@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medico(id: str):
    db.del_medico(id)
    return ""

# resetar o banco de dados:
@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    db_init.tables_init()
    return "/app/home.html"

# retornar template para editar paciente:
@app.get("/api/pacientes/{id}/edit", response_class=HTMLResponse)
async def edit_paciente(id):
    paciente = db.get_paciente(id)

    if paciente:
        dados = paciente[0]
        return edit.paciente_html(dados)
    else:
        return ""
    
@app.get("/api/medicos/{id}/edit", response_class=HTMLResponse)
async def edit_medico(id):
    medico = db.get_medico(id)

    if medico:
        dados = medico[0]
        return edit.medico_html(dados)
    else:
        return ""

# @app.get("/api/medicos", response_class=HTMLResponse)
# async def medicos():
#     dados_httml = """
#         <table>
#             <thead>
#                 <tr>
#                     <th>Nome</th>
#                 </tr>
#             </thead>

#             <tbody>
#                 <tr>
#                     <td>Kaio Oliveira</td>
#                 </tr>
#             </tbody>
#         </table>
# """
#     return dados_httml
