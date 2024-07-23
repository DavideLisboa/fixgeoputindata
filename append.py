import arcpy


def append(view, bruto):
    field_mappings = arcpy.FieldMappings()
    field_map = arcpy.FieldMap()
    field_map.addInputField(bruto, "HIDROMETRO")
    field_mappings.addFieldMap(field_map)

    arcpy.Append_management(view, bruto, 'NO_TEST',
                            field_mapping=field_mappings)
