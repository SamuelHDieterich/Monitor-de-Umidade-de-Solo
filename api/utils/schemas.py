################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  BUILT-IN  ##
################

from datetime import datetime


################
##  EXTERNAL  ##
################

from pydantic import BaseModel



################################################################################
##                                   SCHEMAS                                  ##
################################################################################

############
##  BASE  ##
############

class BaseModel(BaseModel):
  class Config:
    from_attributes = True


########################
##  COLLECTOR STATUS  ##
########################

class CollectorStatusBase(BaseModel):
  start_date: datetime
  end_date: datetime | None = None
  crop: str


class CollectorStatus(CollectorStatusBase):
  collector_id: int


class CollectorStatusJSON(BaseModel):
  collector_id: int
  data: list[CollectorStatusBase]


########################
##  COLLECTOR RECORD  ##
########################

class CollectorRecordBase(BaseModel):
  collection_date: datetime
  read_humidity: int


class CollectorRecord(CollectorRecordBase):
  collector_id: int


class CollectorRecordJSON(BaseModel):
  collector_id: int
  data: list[CollectorRecordBase]


###########################
##  CALCULATED HUMIDITY  ##
###########################

class CalculatedHumidityBase(BaseModel):
  calculation_date: datetime
  humidity_percentage: float


class CalculatedHumidity(CalculatedHumidityBase):
  collector_id: int


class CalculatedHumidityJSON(BaseModel):
  collector_id: int
  data: list[CalculatedHumidityBase]


################
##  RECEPTOR  ##
################

class ReceptorStatus(BaseModel):
  update_date: datetime
  records_in_buffer: int
