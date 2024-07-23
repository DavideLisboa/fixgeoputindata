import arcpy
from field_names import field_names


def add_data(view, bruto):
    fields_view = field_names(view)
    fields_bruto = field_names(bruto)

    cursor_view = arcpy.da.SearchCursor(view, fields_view)
    cursor_feature = arcpy.da.UpdateCursor(bruto, fields_bruto)
    existing_hidrometro_set = set()

    for row_feature in cursor_feature:
        hidrometro_value = row_feature[fields_bruto.index("HIDROMETRO")]
        existing_hidrometro_set.add(hidrometro_value)
    # Check if LATITUDE and LONGITUDE in the feature class have data
        for row_view in cursor_view:
            if row_view[fields_view.index("HIDROMETRO")] == hidrometro_value:
                if row_feature[fields_bruto.index("LATITUDE")] is not None and row_feature[fields_bruto.index("LONGITUDE")] is not None:
                    # Case 1: Update all other columns except LATITUDE, LONGITUDE, and SHAPE
                    for field_name in fields_bruto:
                        if field_name not in ["LATITUDE", "LONGITUDE", "Shape", "HIDROMETRO"]:
                            # Search for matching row in the first table
                            row_feature[fields_bruto.index(
                                        field_name)] = row_view[fields_view.index(field_name)]
                    cursor_feature.updateRow(row_feature)
                    break

                else:
                    for field_name in fields_view:
                        if field_name not in ["Shape", "HIDROMETRO"]:
                            row_feature[fields_bruto.index(
                                        field_name)] = row_view[fields_view.index(field_name)]

                            # Get latitude and longitude values
                    latitude = row_view[fields_view.index("LATITUDE")]
                    longitude = row_view[fields_view.index(
                        "LONGITUDE")]

                    # Update geometry position
                    row_feature[fields_bruto.index("Shape")] = arcpy.Point(
                        longitude, latitude)

                    cursor_feature.updateRow(row_feature)
                    break

    print("HIDROMETRO não encontrado:")
    for row_view in cursor_view:
        hidrometro_value_view = row_view[fields_view.index("HIDROMETRO")]
        objectid_view = row_view[fields_view.index("OBJECTID")]
        if hidrometro_value_view not in existing_hidrometro_set:
            print(
                f"HIDROMETRO: {hidrometro_value_view}, OBJECTID: {objectid_view}")
        if hidrometro_value_view in ["", None, " "]:
            print(
                f"OBJECTID: {objectid_view} Hidrometro vazio")

    del cursor_view
    del cursor_feature
