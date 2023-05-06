import pytest
import os
from project_paths import paths
from woc.iiif_manifest import IIIF_Manifest
from woc.exceptions.woc_exceptions import IdNotFoundError


# Global test variables
manifest = None
expected_drs_file_ids = [
  460390370,
  460390371,
  460390372,
  460390373,
  460390374,
  460390375,
  460390376,
  460390377,
  460390378,
  460390379,
  460390380,
  460390381,
  460390382,
  460390383,
  460390384,
  460390385
]

@pytest.fixture
def setup():
  manifest_file = os.path.join(paths.dir_unit_resources, "manifest-30786.json")
  with open(manifest_file, 'r') as file:
    manifest_str = file.read()
  global manifest
  manifest = IIIF_Manifest(manifest_str)


def test_num_canvases(setup):
  num = manifest.num_canvases()
  assert num != None  
  assert len(expected_drs_file_ids) == num


def test_get_drs_file_ids_for_canvases(setup):
  drs_file_ids = manifest.get_drs_file_ids_for_canvases()
  assert drs_file_ids != None
  assert len(drs_file_ids) == len(expected_drs_file_ids)
  
  for expected_id in expected_drs_file_ids:
    assert expected_id in drs_file_ids


def test_get_searchable_text_url_for_drs_file_id_bad(setup):
  id = 123456789
  with pytest.raises(IdNotFoundError, match=".*{}.*".format(id)):
    manifest.get_searchable_text_url_for_drs_file_id(id)


def test_get_searchable_text_url_for_drs_file_id(setup):
  expected_url =\
    "https://fromthepage.com/iiif/30786/export/1014310/plaintext/searchable"

  id = 460390378
  url = manifest.get_searchable_text_url_for_drs_file_id(id)

  assert url != None
  assert expected_url == url
