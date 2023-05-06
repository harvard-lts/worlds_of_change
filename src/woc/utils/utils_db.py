import cx_Oracle
import sys
from woc.utils.utils_env import EnvDetails
from woc.exceptions.woc_exceptions import IdNotFoundError


class DrsDB:

  def __init__(self, lib_dir, env='prod'):
    self.env_details = EnvDetails(env)
    self.db = self._get_db_connection(lib_dir, self.env_details)


  def get_file_names_for_object(self, obj_id):
    sql = "SELECT f.ID, f.SUPPLIED_FILENAME from REPOSITORY.DRS_FILE f "\
          "WHERE f.DRS_OBJECT_ID = {}".format(obj_id)
    cursor = self.db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    if not rows:
      raise Exception("No files found for '{}'".format(obj_id))

    file_names = {} 
    for row in rows:
      file_names[row[0]] = row[1]

    return file_names


  def get_jp2_file_ids_for_object(self, obj_id):
    """This method is a helper for querying the DRS DB for JP2 files in the
       provided DRS Object
    """

    jp2_format_id = self.env_details.get_jp2_format_id()
    sql = "SELECT f.ID from REPOSITORY.DRS_FILE f "\
          "WHERE f.FORMAT_ID = {} and f.DRS_OBJECT_ID = {}"\
          .format(jp2_format_id, obj_id)
    cursor = self.db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    if not rows:
      raise IdNotFoundError(
        "Object not found in DRS DB with ID: {}".format(obj_id))

    file_ids = [] 
    for row in rows:
      file_ids.append(row[0])

    return file_ids


  def get_object_osn(self, obj_id):
    """This method is a helper for querying the DRS DB for Object OSN"""

    sql = "SELECT o.OWNER_SUPPLIED_NAME from REPOSITORY.DRS_OBJECT o "\
          "WHERE o.ID = {}"\
          .format(obj_id)
    cursor = self.db.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
      raise IdNotFoundError(
        "Object not found in DRS DB with ID: {}".format(obj_id))

    return row


  def _get_db_connection(self, lib_dir, env_details):
    if lib_dir == None:
      base_dir="/Users/anw822/programming/drs/scripts/drs_cross_environment/lib"
      lib_dir="{}/instantclient_19_8/".format(base_dir)

    try:
      cx_Oracle.init_oracle_client(lib_dir)
    except Exception as err:
      print("Whoops!")
      print(err);
      sys.exit(1);

    dsn_tns = cx_Oracle.makedsn(env_details.get_db_host(),
                                env_details.get_db_port(),
                                env_details.get_db_name())
    db = cx_Oracle.connect(env_details.get_db_user(),
                           env_details.get_db_pass(),
                           dsn_tns, 
                           encoding="UTF-8")
    return db
