import arcpy


def calculate_shape(latitude, longitude):
    # Create a point geometry from the provided latitude and longitude
    return arcpy.PointGeometry(arcpy.Point(longitude, latitude))


def append_excel_data(input_excel, target_table):

    hidrometro = []

    # Read HIDROMETRO, Latitude, and Longitude from the Excel file
    with arcpy.da.SearchCursor(target_table, ["HIDROMETRO"]) as search_cursor:
        for row in search_cursor:
            hidrometro.append(row[0])
    del search_cursor

    # Update the target table
    with arcpy.da.SearchCursor(input_excel, ["Num_hid", "Latitude", "Longitude"]) as cursor:
        for row in cursor:
            if row[0] in hidrometro:
                with arcpy.da.UpdateCursor(target_table, ["HIDROMETRO", "LATITUDE", "LONGITUDE", "Shape"], "HIDROMETRO = " + "'" + str(row[0]) + "'") as update_cursor:
                    for row1 in update_cursor:
                        # Update Latitude and Longitude from the Excel file
                        row1[1] = row[1]
                        row1[2] = row[2]

                        # Calculate Shape based on the updated Latitude and Longitude
                        row1[3] = calculate_shape(row[1], row[2])
                        update_cursor.updateRow(row1)
            else:
                # If HIDROMETRO is not in the Excel file, add data from the Excel file
                with arcpy.da.InsertCursor(target_table, ["HIDROMETRO", "Latitude", "Longitude", "SHAPE@"]) as insert_cursor:
                    insert_cursor.insertRow([row[0], row[1],
                                            row[2],
                                            calculate_shape(row[1],
                                                            row[2])])

        del cursor
        del update_cursor
        del insert_cursor

# Call the function with your actual paths
