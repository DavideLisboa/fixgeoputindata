import arcpy


def field_names(tabela):
    return [field.name for field in arcpy.ListFields(tabela)]
