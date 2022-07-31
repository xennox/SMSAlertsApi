from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import schemas, models
import uvicorn

app = FastAPI(title='API управления рассылками')

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/makeclient', status_code=status.HTTP_201_CREATED, tags=['Клиенты'])
def create(request: schemas.Client, db: Session = Depends(get_db)):
    new_client = models.Client(id=request.id, tel=request.tel, tag=request.tag, note=request.note, timebelt=request.timebelt)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.get('/allclients', tags=['Клиенты'])
def all(db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    return clients

@app.get('/client/{id}', status_code=200, tags=['Клиенты'])
def show(id, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Клиент с ID {id} не найден')
    return client

@app.delete('/deleteclient/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Клиенты'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Client).filter(models.Client.id == id).delete(synchronize_session=False)
    db.commit()
    return f'Клиент с ID {id} Удален'

@app.put('/updateclient/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Клиенты'])
def update(id, request: schemas.Client, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == id)
    if not client.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Клиент с ID {id} не найден')
    client.update(request.dict())
    db.commit()
    return f'Клиент с ID {id} Обновлен'

@app.post('/makemalling', status_code=status.HTTP_201_CREATED, tags=['Рассылки'])
def create(request: schemas.Malling, db: Session = Depends(get_db)):
    new_malling = models.Malling(id=request.id, datetimestart=request.datetimestart, datetimeend=request.datetimeend, smstext=request.smstext, tag=request.tag)
    db.add(new_malling)
    db.commit()
    db.refresh(new_malling)
    return new_malling

@app.get('/allmallings', status_code=200, tags=['Рассылки'])
def show(db: Session = Depends(get_db)):
    malling = db.query(models.Malling).all()
    if not malling:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Расслыки не найдены')
    return malling

@app.delete('/deletemalling/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Рассылки'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Malling).filter(models.Malling.id == id).delete(synchronize_session=False)
    db.commit()
    return f'Рассылка с ID {id} Удалена'

@app.put('/updatemalling/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Рассылки'])
def update(id, request: schemas.Malling, db: Session = Depends(get_db)):
    malling = db.query(models.Malling).filter(models.Malling.id == id)
    if not malling.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Рассылка с ID {id} не найдена')
    malling.update(request.dict())
    db.commit()
    return f'Клиент с ID {id} Обновлен'


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)