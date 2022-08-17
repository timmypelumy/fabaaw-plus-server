from fastapi import FastAPI
from routers import users
from config import app_settings


app = FastAPI(title='Fabaaw Plus', description= "A decentralized identity management system powered by blockchain technology",version= '0.1.0')


@app.on_event('startup')
def startup():
    pass



@app.on_event('shutdown')
def shutdown():
    pass



allowed_origins = [

    'http://localhost:3000'
    
]



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get('/ping', tags=["Check API Server Status"])
def ping():
    return {
        f'{app_settings.app_name}' : "To the moon!" 
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








