# https://fastapi.tiangolo.com/tutorial/sql-databases/

################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  INTERNAL  ##
################

from utils import crud, models, schemas
from utils.database import SessionLocal, engine


################
##  EXTERNAL  ##
################

from fastapi import Depends, FastAPI, HTTPException, Query, status
from mangum import Mangum
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session



################################################################################
##                                     APP                                    ##
################################################################################

app = FastAPI(
  title="API para monitor de umidade de solo",
  description="API para monitor de umidade de solo",
  version="0.0.1",
)

handler = Mangum(app=app)



################################################################################
##                                 CONNECTION                                 ##
################################################################################

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():

  """
  Create a new database session and yield it to the caller.

  Yields
  ------
  Session
    A SQLAlchemy Session object representing a database session.
  """

  db = SessionLocal()

  try:
    yield db
  finally:
    db.close()



################################################################################
##                                    ROUTES                                  ##
################################################################################

############
##  ROOT  ##
############

@app.get("/")
def root():
  return {"message": "Hello World"}


############
##  READ  ##
############

@app.get(
  path="/collector/status",
  response_model=list[schemas.CollectorStatusJSON],
  tags=["Collector"],
  description="Retrieve the most recent status updates for all collectors from the database."
)
async def get_collector_status(
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=1, ge=1),
  db: Session = Depends(get_db),
):

  """
  Retrieve the most recent status updates for all collectors from the database.

  Parameters
  ----------
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  List[CollectorStatusJSON]
    A list of CollectorStatusJSON objects representing the most recent status updates for all collectors.
  """

  return crud.get_collector_status(db, offset, limit)


@app.get(
  path="/collector/{collector_id}/status",
  response_model=schemas.CollectorStatusJSON,
  tags=["Collector"],
  description="Retrieve the most recent status update for a specific collector from the database.",
)
async def get_collector_status_by_id(
  collector_id: int,
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=100, ge=1),
  db: Session = Depends(get_db),
):

  """
  Retrieve the most recent status update for a specific collector from the database.

  Parameters
  ----------
  collector_id : int
    The ID of the collector to retrieve the status update for.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  CollectorStatusJSON
    A CollectorStatusJSON object representing the most recent status update for the specified collector.

  Raises
  ------
  HTTPException
    If the specified collector is not found in the database.
  """

  collector_status = crud.get_collector_status_by_id(db, collector_id, offset, limit)
  if collector_status is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collector not found")
  return collector_status


@app.get(
  path="/collector/record/",
  response_model=list[schemas.CollectorRecordJSON],
  tags=["Collector"],
  description="Retrieve the most recent records for all collectors from the database."
)
async def get_collector_record(
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=1, ge=1),
  db: Session = Depends(get_db),
):

  """
  Retrieve the most recent records for all collectors from the database.

  Parameters
  ----------
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  List[CollectorRecordJSON]
    A list of CollectorRecordJSON objects representing the most recent records for all collectors.
  """

  return crud.get_collector_record(db, offset, limit)


@app.get(
  path="/collector/{collector_id}/record",
  response_model=schemas.CollectorRecordJSON,
  tags=["Collector"],
  description="Retrieve the most recent records for a specific collector from the database."
)
async def get_collector_record_by_id(
  collector_id: int,
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=100, ge=1),
  db: Session = Depends(get_db),
):

  """
  Retrieve the most recent records for a specific collector from the database.

  Parameters
  ----------
  collector_id : int
    The ID of the collector to retrieve the records for.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  CollectorRecordJSON
    A CollectorRecordJSON object representing the most recent records for the specified collector.

  Raises
  ------
  HTTPException
    If the specified collector is not found in the database.
  """

  collector_record = crud.get_collector_record_by_id(db, collector_id, offset, limit)
  if collector_record is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collector not found")
  return collector_record


@app.get(
  path="/collector/calculated_humidity",
  response_model=list[schemas.CalculatedHumidityJSON],
  tags=["Collector"],
  description="Retrieve the most recent calculated humidity records for all collectors from the database."
)
async def get_collector_calculated_humidity(
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=1, ge=1),
  db: Session = Depends(get_db),
):

  """
  Retrieve the most recent calculated humidity records for all collectors from the database.

  Parameters
  ----------
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  List[CalculatedHumidityJSON]
    A list of CalculatedHumidityJSON objects representing the most recent calculated humidity records for all collectors.
  """

  return crud.get_collector_calculated_humidity(db, offset, limit)


@app.get(
  path="/collector/{collector_id}/calculated_humidity",
  response_model=schemas.CalculatedHumidityJSON,
  tags=["Collector"],
  description="Retrieve the most recent calculated humidity record for a specific collector from the database."
)
async def get_collector_calculated_humidity_by_id(
  collector_id: int,
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=100, ge=1),
  db: Session = Depends(get_db),
):
  
  """
  Retrieve the most recent calculated humidity record for a specific collector from the database.

  Parameters
  ----------
  collector_id : int
    The ID of the collector to retrieve the calculated humidity record for.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  CalculatedHumidityJSON
    A CalculatedHumidityJSON object representing the most recent calculated humidity record for the specified collector.

  Raises
  ------
  HTTPException
    If the specified collector is not found in the database.
  """

  collector_calculated_humidity = crud.get_collector_calculated_humidity_by_id(db, collector_id, offset, limit)
  if collector_calculated_humidity is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collector not found")
  return collector_calculated_humidity


@app.get(
  path="/receptor/status",
  response_model=list[schemas.ReceptorStatus],
  tags=["Receptor"],
  description="Retrieve the most recent status records for all receptors from the database."
)
async def get_receptor_status(
  offset: int = Query(default=0, ge=0),
  limit: int = Query(default=1, ge=1),
  db: Session = Depends(get_db),
):

  """
  Retrieve the most recent status records for all receptors from the database.

  Parameters
  ----------
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  List[ReceptorStatus]
    A list of ReceptorStatus objects representing the most recent status records for all receptors.
  """

  receptor_status = crud.get_receptor_status(db, offset, limit)
  if receptor_status is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No status found")
  return receptor_status


##############
##  CREATE  ##
##############

@app.post(
  path="/collector/{collector_id}/status",
  response_model=schemas.CollectorStatus,
  tags=["Collector"],
  description="Create a new status record for a specific collector in the database."
)
async def post_collector_status(
  collector_id: int,
  body: schemas.CollectorStatusBase,
  db: Session = Depends(get_db),
):

  """
  Create a new status record for a specific collector in the database.

  Parameters
  ----------
  collector_id : int
    The ID of the collector to create the status record for.
  body : CollectorStatusBase
    The request body containing the data for the new status record.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  CollectorStatus
    A CollectorStatus object representing the newly created status record.

  Raises
  ------
  HTTPException
    If the specified collector is not found in the database or if the primary key already exists.
  """

  try:
    return crud.post_collector_status(db, collector_id, body)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Primary key already exists")


@app.post(
  path="/collector/{collector_id}/record",
  response_model=schemas.CollectorRecord,
  tags=["Collector"],
  description="Create a new record for a specific collector in the database."
)
async def post_collectors_record(
  collector_id: int,
  body: schemas.CollectorRecordBase,
  db: Session = Depends(get_db),
):

  """
  Create a new record for a specific collector in the database.

  Parameters
  ----------
  collector_id : int
    The ID of the collector to create the record for.
  body : CollectorRecordBase
    The request body containing the data for the new record.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  CollectorRecord
    A CollectorRecord object representing the newly created record.

  Raises
  ------
  HTTPException
    If the specified collector is not found in the database or if the primary key already exists.
  """

  try:
    return crud.post_collector_record(db, collector_id, body)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Primary key already exists")


@app.post(
  path="/collector/{collector_id}/calculated_humidity",
  response_model=schemas.CalculatedHumidity,
  tags=["Collector"],
  description="Create a new calculated humidity record for a specific collector in the database."
)
async def post_collector_calculated_humidity(
  collector_id: int,
  body: schemas.CalculatedHumidityBase,
  db: Session = Depends(get_db),
):

  """
  Create a new calculated humidity record for a specific collector in the database.

  Parameters
  ----------
  collector_id : int
    The ID of the collector to create the calculated humidity record for.
  body : CalculatedHumidityBase
    The request body containing the data for the new calculated humidity record.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  CalculatedHumidity
    A CalculatedHumidity object representing the newly created calculated humidity record.

  Raises
  ------
  HTTPException
    If the specified collector is not found in the database or if the primary key already exists.
  """

  try:
    return crud.post_collector_calculated_humidity(db, collector_id, body)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Primary key already exists")


@app.post(
  path="/receptor/status",
  response_model=schemas.ReceptorStatus,
  tags=["Receptor"],
  description="Create a new status record for a specific receptor in the database."
)
async def post_receptor_status(
  body: schemas.ReceptorStatus,
  db: Session = Depends(get_db),
):

  """
  Create a new status record for a specific receptor in the database.

  Parameters
  ----------
  body : ReceptorStatus
    The request body containing the data for the new status record.
  db : Session, optional
    The database session. This parameter is automatically injected by FastAPI.

  Returns
  -------
  ReceptorStatus
    A ReceptorStatus object representing the newly created status record.

  Raises
  ------
  HTTPException
    If the primary key already exists.
  """

  try:
    return crud.post_receptor_status(db, body)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Primary key already exists")
