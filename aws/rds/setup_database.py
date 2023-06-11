#################
##  LIBRARIES  ##
#################

import os
from configparser import ConfigParser
import psycopg2
from jinja2 import Template


#################
##  CONSTANTS  ##
#################

CREDENTIALS_FILE = os.path.join("config", "credentials.conf")
SQL_FOLDER = os.path.join("sql")


###################
##  CREDENTIALS  ##
###################

credentials = ConfigParser()
credentials.read(CREDENTIALS_FILE)


##################
##  CONNECTION  ##
##################

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(**dict(credentials.items("DATABASE")))

# Create a cursor object from the connection
cur = conn.cursor()

# Create tables
with open(os.path.join(SQL_FOLDER, "create_tables.sql"), "r") as f:
  sql = f.read()
  cur.execute(sql)

# Create roles
with open(os.path.join(SQL_FOLDER, "create_roles.sql.jinja"), "r") as f:
  sql = Template(f.read()).render(**dict(credentials.items("ROLES")))
  cur.execute(sql)

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
cur.close()
conn.close()
