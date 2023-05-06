import pytest
import os
from project_paths import paths
from woc.utils.utils_db import DrsDB
from woc.worker import Worker
from woc.exceptions.woc_exceptions import IdNotFoundError


class TestWorkerClass():
  
  def _get_mock_db(self, mocker):
    return mocker.patch('woc.utils.utils_db.DrsDB')


  def test_get_osn_for_drs_obj(self, mocker):
 
    expected_osn = '002397645_v0001-METS_CRB1'
 
    mock_db = self._get_mock_db(mocker)
    mock_db.get_object_osn.return_value = [expected_osn]
    worker = Worker(mock_db)

    drs_obj_id = 1234
    osn = worker.get_osn_for_drs_obj(drs_obj_id)
    assert expected_osn == osn


  def test_verify_same(self, mocker):
    ids_x = [123, 456, 789]
    ids_y = [123, 456, 789]

    worker = Worker(self._get_mock_db(mocker))
    worker.verify_same(ids_x, ids_y)


  def test_verify_same_bad_len(self, mocker):
    ids_x = [123, 456, 789]
    ids_y = [123, 456, 789, 111]

    worker = Worker(self._get_mock_db(mocker))
    with pytest.raises(Exception, match=".*not equal.*"):
      worker.verify_same(ids_x, ids_y)


  def test_verify_same_bad_values(self, mocker):
    ids_x = [123, 406, 789]
    ids_y = [123, 456, 789]

    worker = Worker(self._get_mock_db(mocker))
    with pytest.raises(Exception, match=".*not found.*"):
      worker.verify_same(ids_x, ids_y)


  def test_write_to_disk(self, mocker):
    base_dir = paths.dir_unit_out

    filename_orig = "test.jp2"
    filename_expected = "test.txt"
    file_path = os.path.join(base_dir, filename_orig)
    text = """hello, unit test!
              ..and goodbye :(
           """

    worker = Worker(self._get_mock_db(mocker))
    worker.write_to_disk(file_path, text)

    # Verify
    input_text = ""
    expected_path = os.path.join(base_dir, filename_expected)
    with open(expected_path, "r") as f:
      for line in f:
        input_text += line

    assert input_text == text

    os.remove(expected_path)
