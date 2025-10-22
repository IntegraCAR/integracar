from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campus_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_inicio(request: Request):
    campus = campus_repo.obter_todos()
    response = templates.TemplateResponse(
        "publico/inicio.html", 
        {
            "request": request,
            "campus": campus
        }
    )
    return response