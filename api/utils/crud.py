################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  INTERNAL  ##
################

from . import models
from . import schemas


################
##  EXTERNAL  ##
################

from sqlalchemy.orm import Session
from sqlalchemy import func


################################################################################
##                                    CRUD                                    ##
################################################################################

############
##  READ  ##
############

def get_collector_status(db: Session, offset: int = 0, limit: int = 1):

  """
  Retrieve the most recent status updates for all collectors from the database.

  Parameters
  ----------
  db : Session
    The database session.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.

  Returns
  -------
  List[Tuple[int, List[Dict[str, Any]]]]
    A list of tuples, where each tuple contains the collector ID and a list of dictionaries representing the most recent status updates for that collector.
    Each dictionary contains the following keys:
      - "start_date": The start date of the status update.
      - "end_date": The end date of the status update.
      - "crop": The crop associated with the status update.
  """

  subquery = (
    db.query(
      models.CollectorStatus,
      func.row_number().over(
        partition_by=models.CollectorStatus.collector_id,
        order_by=models.CollectorStatus.start_date.desc()
      ).label("row_number")
    )
    .subquery()
  )

  query = (
    db.query(subquery.c.collector_id,
    func.array_agg(
      func.json_build_object(
        "start_date", subquery.c.start_date,
        "end_date", subquery.c.end_date,
        "crop", subquery.c.crop
      )
    ).label("data"))
    .filter(subquery.c.row_number >= offset)
    .filter(subquery.c.row_number <= limit+offset)
    .group_by(subquery.c.collector_id)
    .order_by(subquery.c.collector_id)
    .all()
  )

  return query


def get_collector_status_by_id(db: Session, collector_id: int, offset: int = 0, limit: int = 100):

  """
  Retrieve the most recent status updates for a specific collector from the database.

  Parameters
  ----------
  db : Session
    The database session.
  collector_id : int
    The ID of the collector to retrieve status updates for.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.

  Returns
  -------
  Tuple[int, List[Dict[str, Any]]]
    A tuple containing the collector ID and a list of dictionaries representing the most recent status updates for that collector.
    Each dictionary contains the following keys:
      - "start_date": The start date of the status update.
      - "end_date": The end date of the status update.
      - "crop": The crop associated with the status update.
  """

  subquery = (
    db.query(models.CollectorStatus)
      .filter(models.CollectorStatus.collector_id == collector_id)
      .order_by(models.CollectorStatus.start_date.desc())
      .offset(offset)
      .limit(limit)
  ).subquery()

  query = (
    db.query(subquery.c.collector_id,
    func.array_agg(
      func.json_build_object(
        "start_date", subquery.c.start_date,
        "end_date", subquery.c.end_date,
        "crop", subquery.c.crop
      )
    ).label("data"))
    .group_by(subquery.c.collector_id)
    .first()
  )

  return query


def get_collector_record(db: Session, offset: int = 0, limit: int = 100):

  """
  Retrieve the most recent collector records from the database.

  Parameters
  ----------
  db : Session
    The database session.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.

  Returns
  -------
  List[Tuple[int, List[Dict[str, Any]]]]
    A list of tuples, where each tuple contains the collector ID and a list of dictionaries representing the most recent records for that collector.
    Each dictionary contains the following keys:
      - "collection_date": The date and time of the record.
      - "read_humidity": The humidity reading for the record.
  """

  subquery = (
    db.query(
      models.CollectorRecord,
      func.row_number().over(
        partition_by=models.CollectorRecord.collector_id,
        order_by=models.CollectorRecord.collection_date.desc()
      ).label("row_number")
    )
    .subquery()
  )

  query = (
    db.query(subquery.c.collector_id,
    func.array_agg(
      func.json_build_object(
        "collection_date", subquery.c.collection_date,
        "read_humidity", subquery.c.read_humidity
      )
    ).label("data"))
    .filter(subquery.c.row_number >= offset)
    .filter(subquery.c.row_number <= limit+offset)
    .group_by(subquery.c.collector_id)
    .order_by(subquery.c.collector_id)
    .all()
  )

  return query


def get_collector_record_by_id(db: Session, collector_id: int, offset: int = 0, limit: int = 100):

  """
  Retrieve the most recent records for a specific collector from the database.

  Parameters
  ----------
  db : Session
    The database session.
  collector_id : int
    The ID of the collector to retrieve records for.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.

  Returns
  -------
  Tuple[int, List[Dict[str, Any]]]
    A tuple containing the collector ID and a list of dictionaries representing the most recent records for that collector.
    Each dictionary contains the following keys:
      - "collection_date": The date and time of the record.
      - "read_humidity": The humidity reading for the record.
  """

  subquery = (
    db.query(models.CollectorRecord)
      .filter(models.CollectorRecord.collector_id == collector_id)
      .order_by(models.CollectorRecord.collection_date.desc())
      .offset(offset)
      .limit(limit)
  ).subquery()

  query = (
    db.query(subquery.c.collector_id, 
    func.array_agg(
      func.json_build_object(
        "collection_date", subquery.c.collection_date,
        "read_humidity", subquery.c.read_humidity
      )
    ).label("data"))
    .group_by(subquery.c.collector_id)
    .first()
  )

  return query


def get_collector_calculated_humidity(db: Session, offset: int = 0, limit: int = 1):

  """
  Retrieve the most recent calculated humidity values for all collectors from the database.

  Parameters
  ----------
  db : Session
    The database session.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.

  Returns
  -------
  List[Tuple[int, List[Dict[str, Any]]]]
    A list of tuples, where each tuple contains the collector ID and a list of dictionaries representing the most recent calculated humidity values for that collector.
    Each dictionary contains the following keys:
      - "calculation_date": The date and time of the calculation.
      - "humidity_percentage": The calculated humidity percentage.
  """

  subquery = (
    db.query(
      models.CalculatedHumidity,
      func.row_number().over(
        partition_by=models.CalculatedHumidity.collector_id,
        order_by=models.CalculatedHumidity.calculation_date.desc()
      ).label("row_number")
    )
    .subquery()
  )

  query = (
    db.query(subquery.c.collector_id,
    func.array_agg(
      func.json_build_object(
        "calculation_date", subquery.c.calculation_date,
        "humidity_percentage", subquery.c.humidity_percentage
      )
    ).label("data"))
    .filter(subquery.c.row_number >= offset)
    .filter(subquery.c.row_number <= limit+offset)
    .group_by(subquery.c.collector_id)
    .order_by(subquery.c.collector_id)
    .all()
  )

  return query    


def get_collector_calculated_humidity_by_id(db: Session, collector_id: int, offset: int = 0, limit: int = 100):
  
  """
  Retrieve the most recent calculated humidity values for a specific collector from the database.

  Parameters
  ----------
  db : Session
    The database session.
  collector_id : int
    The ID of the collector to retrieve calculated humidity values for.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 100.

  Returns
  -------
  Tuple[int, List[Dict[str, Any]]]
    A tuple containing the collector ID and a list of dictionaries representing the most recent calculated humidity values for that collector.
    Each dictionary contains the following keys:
      - "calculation_date": The date and time of the calculation.
      - "humidity_percentage": The calculated humidity percentage.
  """
  
  subquery = (
    db.query(models.CalculatedHumidity)
      .filter(models.CalculatedHumidity.collector_id == collector_id)
      .order_by(models.CalculatedHumidity.calculation_date.desc())
      .offset(offset)
      .limit(limit)
  ).subquery()

  query = (
    db.query(subquery.c.collector_id,
    func.array_agg(
      func.json_build_object(
        "calculation_date", subquery.c.calculation_date,
        "humidity_percentage", subquery.c.humidity_percentage
      )
    ).label("data"))
    .group_by(subquery.c.collector_id)
    .first()
  )

  return query


def get_receptor_status(db: Session, offset: int = 0, limit: int = 1):

  """
  Retrieve the most recent receptor status updates from the database.

  Parameters
  ----------
  db : Session
    The database session.
  offset : int, optional
    The number of records to skip. Defaults to 0.
  limit : int, optional
    The maximum number of records to retrieve. Defaults to 1.

  Returns
  -------
  List[ReceptorStatus]
    A list of ReceptorStatus objects representing the most recent updates.
  """

  query = (
    db.query(models.ReceptorStatus)
      .order_by(models.ReceptorStatus.update_date.desc())
      .offset(offset)
      .limit(limit)
      .all()
  )

  return query


##############
##  CREATE  ##
##############

def post_collector_status(db: Session, collector_id: int, status: schemas.CollectorStatusBase):

  """
  Create a new status record for a specific collector in the database.

  Parameters
  ----------
  db : Session
    The database session.
  collector_id : int
    The ID of the collector to create a status record for.
  status : CollectorStatusBase
    A CollectorStatusBase object representing the status record to create.

  Returns
  -------
  CollectorStatus
    A CollectorStatus object representing the newly created status record.
  """

  db_status = models.CollectorStatus(collector_id=collector_id, **status.model_dump())
  db.add(db_status)
  db.commit()
  db.refresh(db_status)

  return db_status


def post_collector_record(db: Session, collector_id: int, record: schemas.CollectorRecordBase):

  """
  Create a new record for a specific collector in the database.

  Parameters
  ----------
  db : Session
    The database session.
  collector_id : int
    The ID of the collector to create a record for.
  record : CollectorRecordBase
    A CollectorRecordBase object representing the record to create.

  Returns
  -------
  CollectorRecord
    A CollectorRecord object representing the newly created record.
  """

  db_record = models.CollectorRecord(collector_id=collector_id, **record.model_dump())
  db.add(db_record)
  db.commit()
  db.refresh(db_record)

  return db_record


def post_collector_calculated_humidity(db: Session, collector_id: int, calculated_humidity: schemas.CalculatedHumidityBase):
  
  """
  Create a new calculated humidity record for a specific collector in the database.

  Parameters
  ----------
  db : Session
    The database session.
  collector_id : int
    The ID of the collector to create a calculated humidity record for.
  calculated_humidity : CalculatedHumidityBase
    A CalculatedHumidityBase object representing the calculated humidity record to create.

  Returns
  -------
  CalculatedHumidity
    A CalculatedHumidity object representing the newly created calculated humidity record.
  """
  
  db_calculated_humidity = models.CalculatedHumidity(collector_id=collector_id, **calculated_humidity.model_dump())
  db.add(db_calculated_humidity)
  db.commit()
  db.refresh(db_calculated_humidity)

  return db_calculated_humidity


def post_receptor_status(db: Session, status: schemas.ReceptorStatus):

  """
  Create a new status record for a receptor in the database.

  Parameters
  ----------
  db : Session
    The database session.
  status : ReceptorStatus
    A ReceptorStatus object representing the status record to create.

  Returns
  -------
  ReceptorStatus
    A ReceptorStatus object representing the newly created status record.
  """

  db_status = models.ReceptorStatus(**status.model_dump())
  db.add(db_status)
  db.commit()
  db.refresh(db_status)

  return db_status
