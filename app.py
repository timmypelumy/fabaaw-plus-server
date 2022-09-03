from fastapi import FastAPI,HTTPException, Depends
from routers import users
from config import app_settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from models.users import Token
from lib.security import authenticate_user, create_access_token

ALLOWED_ORIGINS = [

    'http://localhost:3000' 
]


app = FastAPI(title='Fabaaw Plus', description= "A decentralized identity management system powered by blockchain technology",version= '0.1.0')


app.add_middleware(
    CORSMiddleware,
    allow_origins= ALLOWED_ORIGINS,
    allow_credentials= False,
    allow_methods=["*"],
	allow_headers=["*"],
    max_age=3600,
)

@app.get('/ping', tags=["Check API Server Status"])
def ping():
    return {
        f'{app_settings.app_name}' : "To the moon!" 
    }




# ? lOGIN URL 


@app.post("/api/v1/login", response_model= Token )
async def login_for_access_token( form : OAuth2PasswordRequestForm = Depends() ):
    user = await authenticate_user(form.username, form.password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers = {'WWW-Authenticate' : 'Bearer'})

    access_token = create_access_token({ 'sub' : user.get('user_id') })
    return {
        "accessToken" : access_token , 'tokenType'  :'bearer'
    }



app.include_router(
    router=users.router,
    prefix='/api/v1',
    tags=['Users'],
)



# Run application
if __name__ == "__main__" and app_settings.env == 'development':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)








