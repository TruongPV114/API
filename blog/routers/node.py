from typing import List
from fastapi import APIRouter, Depends,status,HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/node',
    tags=['Nodes']
)
get_db = database.get_db

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_node(request: schemas.Node, db: Session = Depends(get_db)):
    new_node = models.Node(pwm=request.pwm,volt=request.volt,ampe=request.ampe,health=request.health,log=request.log)
    db.add(new_node)
    db.commit()
    db.refresh(new_node)
    return new_node


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_node(id:int, db:Session=Depends(get_db)):
    node = db.query(models.Node).filter(models.Node.id == id)
    if not node.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Node with the id {id} is not found')
    node.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_node(id:int,request: schemas.Node,db: Session = Depends(get_db)):
    node = db.query(models.Node).filter(models.Node.id == id)
    if not node.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Node with the id {id} is not found')
    node.update(request.model_dump())
    db.commit()
    return 'updated'


@router.get('/{id}',status_code=200,response_model=schemas.ShowNode)
def show_node(id:int,db: Session = Depends(get_db)):
    node = db.query(models.Node).filter(models.Node.id == id).first()
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Node with the id {id} is not available')
    return node


@router.get('/',response_model=List[schemas.ShowNode])
def all_node(db: Session = Depends(get_db)):
    nodes = db.query(models.Node).all()
    return nodes