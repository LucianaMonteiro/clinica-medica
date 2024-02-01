from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/app", StaticFiles(directory="static", html="True"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api/pacientes")
async def pacientes():
    return get_pacientes()


@app.get("/api/medicos")
async def medicos():
    dados = get_medicos()
    return dados

@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medicos(id: str):
    return ""

@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def pacientes(id: str):
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


def get_medicos():
    dados = [
        {
            "nome": "Kaio Oliveira",
            "crm": "123456",
            "email": "kaio@gmail.com",
            "especialidade": "cardiologia",
            "turno": "noturno",
            "status": "ativo",
        },
        {
            "nome": "Dileyciane Monteiro",
            "crm": "234567",
            "email": "ciane@gmail.com",
            "especialidade": "dermatologia",
            "turno": "diurno",
            "status": "em análise",
        },
        {
            "nome": "Naelle Monteiro",
            "crm": "345678",
            "email": "NAELLE@gmail.com",
            "especialidade": "pediatria",
            "turno": "DIURNO",
            "status": "ATIVO",
        },
        {
            "nome": "Lidia Monteiro",
            "crm": "456789",
            "email": "lidia@gmail.com",
            "especialidade": "nutrição",
            "turno": "vespertino",
            "status": "INATIVO",
        },
    ]

    return dados


def get_pacientes():
    dados = [
        {
            "nome": "Izaias Lima",
            "email": "izaias@lima.com",
            "telefone": "61 98181-3390",
            "status": "internado",
        },
        {
            "nome": "Luciete Lima",
            "email": "luciete@lima.com",
            "telefone": "61 98136-0050",
            "status": "em atendimento",
        },
        {
            "nome": "Natan Monteiro",
            "email": "natan@monteiro.com",
            "telefone": "61 98313-4298",
            "status": "atendido",
        },
        {
            "nome": "Luciana Monteiro",
            "email": "luciana@monteiro.com",
            "telefone": "61 98313-4289",
            "status": "liberada",
        },
    ]

    return dados
