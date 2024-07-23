import pandas as pd
import arcpy

excel_file_path = 'C:\IMAGEM\SAE-LOUVEIRA\SAE-LOUVEIRA_PROJETO\dados_enviados\Consumidores.xlsx'
# UTM Zone for Louveira
utm_zone = 23
# Assuming your Excel columns for UTM X and Y are named 'UTM_X' and 'UTM_Y', replace with actual column names
utm_x_column = 'X'
utm_y_column = 'Y'

df = pd.read_excel(excel_file_path)

# Create a SpatialReference object for the UTM coordinate system
# UTM NAD83 coordinate system
utm_sr = arcpy.SpatialReference(32700 + utm_zone)

# Function to convert UTM coordinates to latitudes and longitudes


def utm_to_latlon(utm_x, utm_y):
    point = arcpy.PointGeometry(arcpy.Point(utm_x, utm_y), utm_sr)
    # WGS84 geographic coordinate system
    point = point.projectAs(arcpy.SpatialReference(4326))
    return point.firstPoint.Y, point.firstPoint.X


# Create new columns for Latitude and Longitude in the DataFrame
df['Latitude'], df['Longitude'] = zip(
    *df.apply(lambda row: utm_to_latlon(row[utm_x_column], row[utm_y_column]), axis=1))

# Save the updated DataFrame back to a new Excel file
output_excel_file = 'C:\IMAGEM\SAE-LOUVEIRA\SAE-LOUVEIRA_PROJETO\dados_enviados\Consumidores_novo.xlsx'
df.to_excel(output_excel_file, index=False)

print(
    f"Conversion and update complete. Updated data exported to {output_excel_file}.")
