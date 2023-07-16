import pytest
import py_osrm
import constants

data_path = constants.data_path
mld_data_path = constants.mld_data_path
three_test_coordinates = constants.three_test_coordinates
two_test_coordinates = constants.two_test_coordinates

class TestTable:
    osrm = py_osrm.OSRM(
        storage_config = data_path, 
        use_shared_memory = False
    )

    def test_table_annotations(self):
        table_params = py_osrm.TableParameters(
            coordinates = [three_test_coordinates[0], three_test_coordinates[1]],
            annotations = ["distance"]
        )
        res = self.osrm.Table(table_params)
        assert(res["distances"])
        assert(not res["durations"])

        table_params = py_osrm.TableParameters(
            coordinates = [three_test_coordinates[0], three_test_coordinates[1]],
            annotations = ["duration"]
        )
        res = self.osrm.Table(table_params)
        assert(res["durations"])
        assert(not res["distances"])

        table_params = py_osrm.TableParameters(
            coordinates = [three_test_coordinates[0], three_test_coordinates[1]],
            annotations = ["duration", "distance"]
        )
        res = self.osrm.Table(table_params)
        assert(res["durations"])
        assert(res["distances"])

        table_params = py_osrm.TableParameters(
            coordinates = [three_test_coordinates[0], three_test_coordinates[1]]
        )
        res = self.osrm.Table(table_params)
        assert(res["durations"])
        assert(not res["distances"])

    def test_table_snapping(self):
        table_params = py_osrm.TableParameters(
            coordinates = [three_test_coordinates[0], three_test_coordinates[1]],
            snapping = "any"
        )
        res = self.osrm.Table(table_params)
        assert(res["durations"])

    # def test_table_annotation(self):
    #     tables = ["distance", "duration"]

    #     for annotation in tables:
    #         table_params = py_osrm.TableParameters(
    #             coordinates = [three_test_coordinates[0], three_test_coordinates[1]],
    #             annotations = [annotation]
    #         )
    #         res = self.osrm.Table(table_params)
    #      
    #         rows = res[annotation]
    #         for i, col in enumerate(res[annotation]):
    #             assert(len(rows) == len(col))
    #             for j, row in enumerate(col):
    #                 if(i == j):
    #                     # check that diagonal is zero
    #                     assert(col[j] == 0)
    #                 else:
    #                     # everything else is non-zero and finite
    #                     assert(not col[j] == 0)
    #                     assert(math.isfinite(col[j]))
    #         assert(len(table_params.coordinates) == len(rows))

    #     for annotation in tables:
    #         table_params = py_osrm.TableParameters(
    #             coordinates = [three_test_coordinates[0], three_test_coordinates[1]],
    #             sources = [0],
    #             destinations = [0,1],
    #             annotations = [annotation]
    #         )
    #         res = self.osrm.Table(table_params)
    #      
    #         rows = res[annotation]
    #         for i, col in enumerate(res[annotation]):
    #             assert(len(rows) == len(col))
    #             for j, row in enumerate(col):
    #                 if(i == j):
    #                     # check that diagonal is zero
    #                     assert(col[j] == 0)
    #                 else:
    #                     # everything else is non-zero and finite
    #                     assert(not col[j] == 0)
    #                     assert(math.isfinite(col[j]))
    #         assert(len(table_params.sources) == len(rows))

    def test_table_withoutwaypoints(self):
        table_params = py_osrm.TableParameters(
            coordinates = two_test_coordinates,
            annotations = ["duration"]
        )
        table_params.skip_waypoints = True
        res = self.osrm.Table(table_params)
        assert(not res["sources"])
        assert(not res["destinations"])

    def test_table_fallbackspeeds(self):
        table_params = py_osrm.TableParameters(
            coordinates = two_test_coordinates,
            annotations = ["duration"],
            fallback_speed = 1,
            fallback_coordinate_type = "input"
        )
        res = self.osrm.Table(table_params)
        assert(len(res["destinations"]) == 2)
        assert(len(res["fallback_speed_cells"]) == 0)

    def test_table_invalidfallbackspeeds(self):
        osrm = py_osrm.OSRM(
            storage_config = mld_data_path,
            algorithm = "MLD", 
            use_shared_memory = False
        )
        table_params = py_osrm.TableParameters(
            coordinates = two_test_coordinates,
            annotations = ["duration"],
            fallback_speed = -1
        )
        with pytest.raises(RuntimeError) as ex:
            res = osrm.Table(table_params)
        assert(str(ex.value) == "Invalid Table Parameters")

        table_params.fallback_speed = 10
        res = osrm.Table(table_params)

    def test_table_invalidscalefactor(self):
        osrm = py_osrm.OSRM(
            storage_config = mld_data_path,
            algorithm = "MLD", 
            use_shared_memory = False
        )
        table_params = py_osrm.TableParameters(
            coordinates = two_test_coordinates,
            annotations = ["duration"],
            scale_factor = -1
        )
        with pytest.raises(RuntimeError) as ex:
            res = osrm.Table(table_params)
        assert(str(ex.value) == "Invalid Table Parameters")

        table_params.scale_factor = 1
        res = osrm.Table(table_params)
