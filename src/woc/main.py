import argparse
import os
from woc.utils.utils_db import DrsDB
from woc.worker import Worker

###
## Main ##
###
if __name__ == '__main__':
  # construct the argument parse and parse the arguments
  ap = argparse.ArgumentParser(description=
                  "Fetches FromThePage file transcripts into a local "\
                  "directory structure that can be loaded into the DRS")

  ap.add_argument('-o', '--obj_id',
                  required=True,
                  help='DRS Object ID for which FromThePage transcripts '\
                       'will be fetched')
  ap.add_argument('-s', '--staging_dir',
                  required=True,
                  help='Local directory where transcription files will be '\
                       'staged')
  ap.add_argument('-e', '--env',
                  required=False,
                  choices=['prod', 'qa', 'dev'],
                  default='prod',
                  help='Environment to inspect: prod | qa | dev')
  ap.add_argument('-l', '--lib_dir',
                  required=False,
                  default=os.path.join(os.getcwd(), 'instantclient_19_8'),
                  help='Directory where cx_Oracle:instantclient is located')
  args = vars(ap.parse_args())
 
  obj_id      = args['obj_id']
  staging_dir = args['staging_dir']
  env         = args['env']
  lib_dir     = args['lib_dir']

  db = DrsDB(lib_dir, env)
  worker = Worker(db)
  worker.collect_transcripts(obj_id, staging_dir)

