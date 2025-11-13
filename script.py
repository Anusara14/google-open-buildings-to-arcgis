import arcpy
import csv
import os

# --- 1. SET YOUR INPUTS HERE ---

# Path to your 2.4GB CSV file
input_csv = r"D:\path\to\your\3af_buildings.csv" 

# Path to your EXISTING geodatabase (the path you copied)
output_gdb = r"C:\Users\YourName\Documents\ArcGIS\Projects\MyProject\MyProject.gdb"

# The name for your new polygon feature class
output_fc_name = "OpenBuildings_3af"

# The name of the WKT column in your CSV (usually 'geometry')
wkt_column_name = "geometry"

# --- End of Inputs ---


# --- Script logic ---
try:
    print(f"Starting script...")
    
    # Set the spatial reference to WGS 1984 (EPSG: 4326)
    sr = arcpy.SpatialReference(4326)

    output_fc = os.path.join(output_gdb, output_fc_name)
    
    print(f"Creating new feature class at: {output_fc}")
    arcpy.management.CreateFeatureclass(
        out_path=output_gdb,
        out_name=output_fc_name,
        geometry_type="POLYGON",
        spatial_reference=sr
    )

    print(f"Adding 'confidence' field...")
    arcpy.management.AddField(output_fc, "confidence", "DOUBLE")
    
    # You can add more fields here if you want
    # arcpy.management.AddField(output_fc, "plus_code", "TEXT")

    # We will insert the Geometry ('SHAPE@') and the confidence value
    cursor_fields = ["SHAPE@", "confidence"] 
    
    with arcpy.da.InsertCursor(output_fc, cursor_fields) as cursor:
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Get the header row
            header = next(reader)
            try:
                # Find the column number for 'geometry' and 'confidence'
                wkt_index = header.index(wkt_column_name)
                conf_index = header.index("confidence")
            except ValueError as e:
                print(f"Error: A column was not found in the CSV header. {e}")
                raise
            
            print("Reading CSV and inserting polygons...")
            row_count = 0
            for row in reader:
                try:
                    wkt_string = row[wkt_index]
                    confidence_val = float(row[conf_index])

                    # This is the line that does the conversion
                    polygon_geometry = arcpy.FromWKT(wkt_string, sr)

                    # Insert the new polygon and its confidence value
                    cursor.insertRow([polygon_geometry, confidence_val])
                    
                    row_count += 1
                    # This will print progress every 10,000 buildings
                    if row_count % 10000 == 0:
                        print(f"Processed {row_count} features...")

                except Exception as e:
                    print(f"Skipping row {row_count + 1} due to error: {e}")

    print(f"--- SCRIPT COMPLETE ---")
    print(f"Successfully created {output_fc} with {row_count} features.")

except Exception as e:
    print(f"An error occurred: {e}")
    arcpy.AddError(e)
