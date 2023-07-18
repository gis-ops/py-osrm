import pytest
import py_osrm
import constants

data_path = constants.data_path
mld_data_path = constants.mld_data_path
test_tile = constants.test_tile

class TestTile:
    osrm = py_osrm.OSRM(
        storage_config = data_path, 
        use_shared_memory = False
    )

    def test_tile(self):
        tile_params = py_osrm.TileParameters(test_tile["at"])
        res = self.osrm.Tile(tile_params)
        assert(len(res) == test_tile["size"])

    def test_tile_preconditions(self):
        with pytest.raises(Exception):
            # Must be an array
            tile_params = py_osrm.TileParameters(17059, 11948, -15)
        with pytest.raises(Exception):
            # Must be unsigned
            tile_params = py_osrm.TileParameters([17059, 11948, -15])
        tile_params = py_osrm.TileParameters([17059, 11948, 15])
        res = self.osrm.Tile(tile_params)
