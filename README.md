# Google Open Buildings CSV to ArcGIS Pro Importer

A simple Python script to efficiently process the massive Google Open Buildings CSV files (which use WKT geometry) and convert them into a Polygon Feature Class inside an ArcGIS Pro File Geodatabase (GDB). The Google Open Buildings dataset is distributed as massive, multi-gigabyte CSV files. Trying to import these directly into ArcGIS Pro or QGIS often fails, lags, or crashes ("Not Responding"). This is because these programs try to load the entire file into memory at once.

This script (`process_gob.py`) uses `arcpy` and the `csv` library to read the CSV file **one row at a time**. It converts the WKT (Well-Known Text) string from each row into a polygon geometry and immediately inserts it into the geodatabase.

This method is memory-efficient and is the correct way to process datasets that are too large to load all at once.

## Features
* Converts text WKT strings into polygon geometries.
* Handles massive, multi-gigabyte CSV files without crashing.
* Saves output directly to a File Geodatabase.
* Prints progress to the console (e.g., "Processed 10000 features...").
* Relies only on the standard `arcpy` library included with ArcGIS Pro.

## Requirements
* ArcGIS Pro
* A Google Open Buildings CSV file (you can download them [here](https://sites.research.google/open-buildings/)).

## ⚙️ How to Use

1.  **Create your Geodatabase:** In ArcGIS Pro, use the **Catalog** pane to create a new File Geodatabase (e.g., `MyProject.gdb`) where you want the polygons to be saved.
2.  **Copy its Path:** Right-click the new `.gdb` file and select **Copy Path**.
3.  **Edit the Script:** Open the `process_gob.py` script (the code you have) in a text editor.
4.  **Update the 4 Input Variables** at the top of the script with your specific file paths:

    ```python
    # --- 1. SET YOUR INPUTS HERE ---

    # Path to your large CSV file (e.g., 3af_buildings.csv)
    input_csv = r"D:\path\to\your\3af_buildings.csv" 

    # Path to your EXISTING geodatabase (the path you copied in step 2)
    output_gdb = r"C:\path\to\your\Project.gdb"

    # The name for your new polygon feature class
    output_fc_name = "OpenBuildings_3af"

    # The name of the WKT column in your CSV (usually 'geometry')
    wkt_column_name = "geometry"
    ```

5.  **Run the Script:**
    * In ArcGIS Pro, open the **View** tab and click **Python Window**.
    * Paste the *entire, edited* script into the window.
    * Press **Enter** twice to run it.
6.  **Be Patient:** The script will take a long time to process a large file (potentially hours). You will see progress messages in the window, like `Processed 10000 features...`.

---

## 🏭 How the Script Works: Step-by-Step

Think of the script as an **automated factory line**. Your 2.4GB CSV is a giant box of raw materials (text "recipes" for polygons), and your File Geodatabase (GDB) is the empty warehouse where you want to store the finished products (real polygons).

### Step 1: Import Toolboxes
```python
import arcpy
import csv
import os
