################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  BUILT-IN  ##
################

import json


################
##  EXTERNAL  ##
################

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



################################################################################
##                                  DATABASE                                  ##
################################################################################

# Credentials
CREDENTIALS_PATH = "credentials.json"

with open(CREDENTIALS_PATH, "r") as f:
  credentials = json.load(f)

# PostgreSQL connection
POSTGRESQL_URL = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"

# SQLAlchemy
engine = create_engine(POSTGRESQL_URL)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()
