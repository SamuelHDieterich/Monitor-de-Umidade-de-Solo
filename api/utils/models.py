################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  INTERNAL  ##
################

from .database import Base

################
##  EXTERNAL  ##
################

from sqlalchemy import Column, DateTime, Integer, String, Numeric



################################################################################
##                                   MODELS                                   ##
################################################################################

class CollectorStatus(Base):
  __tablename__ = "collector_status"

  collector_id = Column(Integer, primary_key=True)
  start_date = Column(DateTime, primary_key=True)
  end_date = Column(DateTime, nullable=True)
  crop = Column(String)


class CollectorRecord(Base):
  __tablename__ = "collector_record"

  collector_id = Column(Integer, primary_key=True)
  collection_date = Column(DateTime, primary_key=True)
  read_humidity = Column(Integer)
  
  
class CalculatedHumidity(Base):
  __tablename__ = "calculated_humidity"

  collector_id = Column(Integer, primary_key=True)
  calculation_date = Column(DateTime, primary_key=True)
  humidity_percentage = Column(Numeric(5, 2))


class ReceptorStatus(Base):
  __tablename__ = "receptor_status"

  update_date = Column(DateTime, primary_key=True)
  records_in_buffer = Column(Integer)
