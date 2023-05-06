import pytest
import os
from project_paths import paths 
from woc.worker import Worker
from woc.utils.utils_db import DrsDB
from woc.exceptions.woc_exceptions import IdNotFoundError



@pytest.fixture(scope='class')
def setup():
  global worker, db, base_dir
  db = DrsDB(None, 'dev')
  worker = Worker(db)
  base_dir = paths.dir_int_out


@pytest.mark.usefixtures("setup")
class TestWorkerClass():

  def test_get_osn_for_drs_obj(self):
    expected_osn = '002397645_v0001-METS_CRB1'
    drs_obj_id = 400315200 # dev ID
    osn = worker.get_osn_for_drs_obj(drs_obj_id)
    assert expected_osn == osn


  def test_get_osn_for_drs_obj_bad(self):
    id = 12345
    with pytest.raises(IdNotFoundError, match=".*{}.*".format(id)):
      worker.get_osn_for_drs_obj(id)


  def test_get_manifest(self):
    drs_obj_id = 460390368 # prod ID
    manifest = worker.get_manifest(drs_obj_id)

    assert manifest
    assert 16 == manifest.num_canvases()


  def test_get_file_ids_for_drs_obj(self):
    expected_num_file_ids = 380
    drs_obj_id = 400315200 # dev ID
    ids = worker.get_file_ids_for_drs_obj(drs_obj_id)

    assert ids
    assert expected_num_file_ids == len(ids)


  def test_get_transcript_text(self):
    drs_obj_id = 460390368 # prod ID
    file_id    = 460390378 
    manifest = worker.get_manifest(drs_obj_id)

    text = worker.get_transcript_text(file_id, manifest)

    expected_text_len = 135
    assert text
    assert expected_text_len == len(text)

   
  def test_get_supplied_filenames(self):
    drs_obj_id = 400315200 # dev ID
    
    filenames = worker.get_supplied_filenames(drs_obj_id) 

    expected_len = 381
    assert filenames
    assert expected_len == len(filenames)


  def test_write_to_disk(self):
    file_path = os.path.join(base_dir, "test.txt")
    text = """hello!
              ..and goodbye :(
           """

    worker.write_to_disk(file_path, text)

    # Verify
    input_text = ""
    with open(file_path, "r") as f:
      for line in f:
        input_text += line

    assert input_text == text

    os.remove(file_path)
