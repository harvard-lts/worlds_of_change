import json
import re
from woc.exceptions.woc_exceptions import IdNotFoundError


"""
This class provides read-access to elements of a IIIF Manifest

Since: 2023-05-05
Author: awoods
"""
class IIIF_Manifest():

  def __init__(self, manifest_str):
    """
    Constructor takes a string that contains the json of the IIIF manifest
    """
    self.manifest = json.loads(manifest_str)


  def _get_canvases(self):
    canvases = []
    for s in self.manifest['sequences']:
      for c in s['canvases']:
        canvases.append(c)
 
    return canvases 


  def num_canvases(self):
    """
    Return the number of canvases found in this manifest
    """
    canvases = self._get_canvases()
    return len(canvases)


  def get_drs_file_ids_for_canvases(self):
    """
    Find drs_file_ids for all canvases in this manifest.
    The drs_file_id is found in the '@id' property of the 'canvases' list.
    An example '@id' is: https://ids.lib.harvard.edu/ids/iiif/460390385
    The drs_file_id in this case is: 460390385
    """
    drs_file_ids = []
    pattern = re.compile('http.*/canvas/canvas-([0-9]+)\\.json$')

    for c in self._get_canvases():
      id = c['@id']
      file_id = pattern.search(id).group(1)
      drs_file_ids.append(int(file_id))

    return drs_file_ids
   

  def get_searchable_text_url_for_drs_file_id(self, drs_file_id):
    """
    Return the url found in the manifest to the "Searchable Plaintext"
     transcript for the provided DRS File ID.
    """
    pattern = re.compile('http.*/canvas/canvas-{}.json$'.format(drs_file_id))
    for c in self._get_canvases():
      id = c['@id']
      if pattern.search(id) != None:
        for sa in c['seeAlso']:
          if sa['label'] != None and sa['label'] == "Searchable Plaintext":
            return sa['@id']

    raise IdNotFoundError(drs_file_id)

    
