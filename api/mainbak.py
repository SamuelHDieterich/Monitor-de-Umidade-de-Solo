################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  BUILT-IN  ##
################

import json
from typing import Any
from datetime import datetime


################
##  EXTERNAL  ##
################

# Psycopg2
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Path, Depends, HTTPException, status



################################################################################
##                                     APP                                    ##
################################################################################

app = FastAPI(
  title="API para monitor de umidade de solo",
  description="API para monitor de umidade de solo",
  version="0.0.1",
)



################################################################################
##                                 CONNECTION                                 ##
################################################################################

with open("credentials.json", "r") as f:
  credentials = json.load(f)

def connect_db():
  try:
    connection = pg2.connect(**credentials)
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    yield cursor
  except (Exception, pg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
  finally:
    if cursor:
      cursor.close()
    if connection:
      connection.close()


################################################################################
##                                   MODELS                                   ##
################################################################################

class ReceptorStatus(BaseModel):
  update_date: datetime 
  records_in_buffer: int


################################################################################
##                                   ROUTES                                   ##
################################################################################

@app.get(
  path="/receptor/status",
  response_model=ReceptorStatus,
)
async def get_receptor_status(cursor: Any = Depends(connect_db)):
  try:
    cursor.execute("SELECT * FROM receptor_status WHERE update_date = (SELECT MAX(update_date) FROM receptor_status)")
    records = cursor.fetchone()
    return records
  except (Exception, pg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)



################################################################################
##                                   SCRIPT                                   ##
################################################################################

# if __name__ == "__main__":
#   import uvicorn
#   uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)