import uvicorn
from fastapi import FastAPI, UploadFile, File, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import io
from PIL import Image
import os
import shutil
import psycopg2
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from process import process_and_return


load_dotenv('.env')

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="postgres",
    port=os.getenv("DATABASE_PORT")
)


app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/sign")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/sign")
async def signup(
    request: Request, username: str = Form(...), email: str = Form(...),password1: str = Form(...),password2:str = Form(...) 
):
   
    cur = conn.cursor()
    cur.execute("INSERT INTO users(Username,Email,Password_) VALUES (%s, %s,%s)", (username,email,password1))
    conn.commit()
    cur.close() 
 
    return RedirectResponse("/login", status_code=303)

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def do_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE Username=%s and Password_=%s", (username,password))
    existing_user = cur.fetchone()
    cur.close()
    
    if existing_user:
        print(existing_user)
        return RedirectResponse("/upload", status_code=303)
    
    else:
        return JSONResponse(status_code=401, content={"message": "Wrong credentials"})

   
# @app.get("/home")
# def homepage(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})

@app.get("/upload")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(request: Request,image: UploadFile):
    if image.filename != '':
        ## Saving the uploaded image to the specified directory
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        ## Processing the uploaded image 
        img = Image.open(image_path)
        predictions = process_and_return(image_path)

    #     return {"message": "Image uploaded and processed successfully.","Pred":predictions}
    # return {"error": "No image selected."}

        return templates.TemplateResponse("index.html", {"request": request, "message": "Image uploaded and processed successfully.", "Pred": predictions})
    return templates.TemplateResponse("index.html", {"request": request, "error": "No image selected."})



if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)


   #apt-get install -y libgl1-mesa-dev
   #sudo apt-get install libgl1-mesa-glx
   #pip install python-multipart
   #python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl