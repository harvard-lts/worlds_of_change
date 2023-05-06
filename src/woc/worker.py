from woc.utils.utils_db import DrsDB
from woc.exceptions.woc_exceptions import IdNotFoundError
from woc.iiif_manifest import IIIF_Manifest
import os
import requests

"""
This class is the central collection of functionality to retrieve and stage
transcripts from the FromThePage service.

Since: 2023-05-05
Author: awoods
"""
class Worker():


  def __init__(self, db):
    self.db = db


  def get_osn_for_drs_obj(self, drs_obj_id):
    osn = self.db.get_object_osn(drs_obj_id)
    if osn is None:
      raise IdNotFoundError(drs_obj_id)

    return osn[0]


  def get_manifest(self, drs_obj_id):
    url = 'https://fromthepage.com/iiif/for/https://iiif.lib.harvard.edu/'\
        'manifests/drs:{}'.format(drs_obj_id)
    r = requests.get(url)

    if r.status_code >= 300:
      raise Exception("{} : {}".format(r.status_code, url))

    return IIIF_Manifest(r.text)


  def get_file_ids_for_drs_obj(self, drs_obj_id):
    file_ids = self.db.get_jp2_file_ids_for_object(drs_obj_id)
    if file_ids is None:
      raise Exception(drs_obj_id)

    return file_ids

  
  def verify_same(self, ids_x, ids_y):
    if len(ids_x) != len(ids_y):
      raise Exception("Number of file IDs in DRS and IIIF Manifest are not "\
                      "equal: {} != {}"\
                      .format(len(ids_x), len(ids_y)))

    for x in ids_x:
      if x not in ids_y:
        raise Exception("ID not found in Manifest! ID: {}, Manifest: {}"\
                        .format(x, ids_y))


  def get_transcript_text(self, file_id, manifest):
    url = manifest.get_searchable_text_url_for_drs_file_id(file_id)

    r = requests.get(url)
    if r.status_code >= 300:
      raise Exception("{} : {}".format(r.status_code, url))

    return r.text


  def get_supplied_filenames(self, drs_obj_id):
    filenames = self.db.get_file_names_for_object(drs_obj_id)

    if filenames is None:
      raise Exception(drs_obj_id)

    return filenames


  def write_to_disk(self, file_path, text):
    # Replace .jp2 extension with .txt
    path = os.path.splitext(file_path)[0] + '.txt'

    with open(path, "w") as f:
      f.write(text)



  def collect_transcripts(self, drs_obj_id, out_dir):
    # get OSN for drs_obj_id
    osn = self.get_osn_for_drs_obj(drs_obj_id)

    # create directory named: OSN
    osn_dir = os.path.join(out_dir, osn)
    os.makedirs(osn_dir, exist_ok=True)

    # get manifest from FromThePage for drs_obj_id
    manifest = self.get_manifest(drs_obj_id)

    ## Verify manifest and DRS obj have same file_ids
    file_ids_drs      = self.get_file_ids_for_drs_obj(drs_obj_id)
    file_ids_manifest = manifest.get_drs_file_ids_for_canvases()

    self.verify_same(file_ids_drs, file_ids_manifest)

    supplied_filenames = self.get_supplied_filenames(drs_obj_id)

    # get transcripts from FromThePage for all images in manifest
    for i in file_ids_manifest:
      # get "Supplied Filename" from DRS DB for each drs_file_id
      text = self.get_transcript_text(i, manifest)
      supplied_filename = supplied_filenames[int(i)]

      # save transcript in OSN directory, with name "Supplied Filename".txt
      self.write_to_disk(os.path.join(osn_dir, supplied_filename), text)

