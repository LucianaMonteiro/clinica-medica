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

@app.get("/api/medicos", response_class=HTMLResponse)
async def medicos(request: Request):
    medicos = get_medicos()
    dados_html = templates.TemplateResponse(
        "tpl_medicos.html", {"request": request, "dados": medicos}
    )

    return dados_html

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
            "especialidade": "cardiologia",
            "turno": "noturno",
            "status": "ativo",
        },
        {
            "nome": "Dileyciane Monteiro",
            "crm": "234567",
            "especialidade": "dermatologia",
            "turno": "diurno",
            "status": "em análise",
        },
    ]

    return dados

    """
        Nome	CRM	Especialidade	Turno	Situação	 
        					 
        Naelle Monteiro	345678	Pediatria	Diurno	Ativo	 
        Lidia Monteiro	456789	Nutrição	Vespertino	Inativo
    """