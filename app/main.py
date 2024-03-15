from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from models import Base
from database import get_db, engine
from utilities import get_info
from crud import get_url_by_key, create_db_url, create_custom_db_url, update_clicks, deactiavte_url

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

 
# #FRONTEND 
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
def analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def delete(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

@app.post("/home", response_class=HTMLResponse)
async def create_url(request: Request, original_url:str = Form(...), custom_url:str = Form(None), db: Session = Depends(get_db)):
    if custom_url:
        db_url = create_custom_db_url(original_url, custom_url, db)
        if db_url == None:
            return templates.TemplateResponse("error.html", context= {"request": request})
        # url = db_url.key
        url = get_info(db_url).url
        qr_code_path = db_url.qr_code_path
        qr_code_download_link = f"/static/qr_codes/{db_url.key}.png"
        return templates.TemplateResponse("home.html", {"request": request, "url": url, "key": db_url.key, 
                                                        "qr_code_path": qr_code_path, "qr_code_download_link": qr_code_download_link})
                                                                  
    else:
        db_url = create_db_url(original_url=original_url, db=db)
        if db_url == None:
            return templates.TemplateResponse("invalid_error.html", context= {"request": request})
        # url = db_url.key
        url = get_info(db_url).url
        qr_code_path = db_url.qr_code_path
        qr_code_download_link = f"/static/qr_codes/{db_url.key}.png"
        return templates.TemplateResponse("home.html", {"request": request, "url": url, "key": db_url.key, 
                                                        "qr_code_path": qr_code_path, "qr_code_download_link": qr_code_download_link})


@app.post("/analytics", response_class=HTMLResponse)
async def get_analytics(request: Request, url_key: str = Form(...), db: Session = Depends(get_db)):
    url = get_url_by_key(url_key, db)
    if url != None:
        qr_code_path = url.qr_code_path
        qr_code_download_link = f"/static/qr_codes/{url.key}.png"
        return templates.TemplateResponse("analytics.html", context= {"request": request, 
                                                             "original_url": url.original_url,
                                                             "clicks": url.clicks,
                                                             "qr_code_path": qr_code_path,
                                                             "qr_code_download_link": qr_code_download_link})
    if url == None:
        return templates.TemplateResponse("invalid_error.html", {"request": request})

@app.post("/delete", response_class=HTMLResponse)
def delete_url(request: Request, url_key: str = Form(...), db: Session = Depends(get_db)):
    url= deactiavte_url(url_key, db)
    if url == None:
        return templates.TemplateResponse("invalid_error.html", {"request": request})
    else:
        deleted = True
        return templates.TemplateResponse("delete.html", {"request": request, "deleted": deleted})

@app.get("/error", response_class=HTMLResponse)
def error(request: Request):
    return templates.TemplateResponse("error.html", {"request": request})

@app.get("/inavlid_error", response_class=HTMLResponse)
def invalid_error(request: Request):
    return templates.TemplateResponse("invalid_error.html", {"request": request})


#FORWARD TO ORIGINAL URL
@app.get("/{url_key}")
async def forward_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    url = get_url_by_key(url_key, db)
    if url:
        update_clicks(url, db)
        return RedirectResponse(url.original_url)
    else:
        return templates.TemplateResponse("invalid_error.html", {"request": request})


#SHOW URL INFO
# @app.get("/analytics/{url_key}", response_model=ShowURL)
# async def get_admin_info(url_key: str, request: Request, db: Session = Depends(get_db)):
#     url = get_url_by_key(url_key, db)
#     if url:
#         return get_info(url)
#     else:
#         raise_not_found(f"{request} not found")


#PEEK URL WITH SHORTENED URL
# @app.get("/admin/peek/{url_key}")
# async def peek_url(url_key: str, request: Request, db: Session = Depends(get_db)):
#     url = get_url_by_key(url_key, db)
#     if url:
#         return url.original_url
#     else:
#         raise_not_found(f"{request} not found")


# @app.get("/admin/qrcode/{url_key}")
# async def peek_url_qr_code(url_key: str, request: Request, db: Session = Depends(get_db)):
#     url = get_url_by_key(url_key, db)
#     if url:
#         return url.qr_code_path
#     else:
#         raise_not_found(f"{request} not found")


# #DELETE URL
# @app.delete("/admin/{url_key}")
# def delete_url(url_key: str, request: Request, db: Session = Depends(get_db)):
#     url= deactiavte_url(url_key, db)
#     if url:
#         {"Message": "URL successfully deleted"}
#     else:
#         raise_not_found(f"{request} not found")



#CREATE A SHORTENED URL
# @app.post("/shorten_url", response_model=ShowURL)
# async def create_url(url: CustomURL, db: Session = Depends(get_db)):
#     if url.custom_url:
#         db_url = create_custom_db_url(url=url, db=db)
#         if db_url == None:
#             return raise_conflict("URL already in use")
#         return get_info(db_url)
#     else:
#         db_url = create_db_url(url=url, db=db)
#         return get_info(db_url)