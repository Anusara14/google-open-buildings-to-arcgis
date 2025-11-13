# Google Open Buildings CSV to ArcGIS Pro Importer

This repository contains a Python script to efficiently process the massive **Google Open Buildings CSV** files (which use **WKT geometry**) and convert them into a **Polygon Feature Class** inside an **ArcGIS Pro File Geodatabase (GDB)**. This script (`process_gob.py`) uses **arcpy** and Python’s **csv** module to:

* read the CSV **one row at a time**
* convert each **WKT** string into a polygon
* immediately write it into the geodatabase

This approach is **memory-efficient**, reliable, and ideal for massive datasets.

---

## ⭐ Features

* Converts text WKT strings into real polygon geometries
* Handles multi-gigabyte CSV files without crashing
* Writes directly into a File Geodatabase
* Provides progress updates (`Processed 10000 features...`)
* Uses only built-in ArcGIS Pro tools (arcpy)

---

## 📦 Requirements

* **ArcGIS Pro**
* A Google Open Buildings CSV file (e.g., `3af_buildings.csv`)

---

## ⚙️ How to Use

### 1. Create Your Geodatabase

Use the *Catalog* pane → **Create File Geodatabase** (e.g., `MyProject.gdb`).

### 2. Copy Its Path

Right-click → **Copy Path**.

### 3. Edit the Script

Open `process_gob.py` and update the input variables:

```python
# --- 1. SET YOUR INPUTS HERE ---

# Path to your large CSV file (e.g., 3af_buildings.csv)
input_csv = r"D:\path\to\your\3af_buildings.csv" 

# Path to your EXISTING geodatabase
output_gdb = r"C:\path\to\your\Project.gdb"

# Name for your new polygon feature class
output_fc_name = "OpenBuildings_3af"

# Name of the WKT column in your CSV (usually 'geometry')
wkt_column_name = "geometry"
```

### 4. Run the Script in ArcGIS Pro

* Open **View → Python Window**
* Paste the full script
* Press **Enter twice** to run

### 5. Be Patient

Processing may take:

* 20 minutes for smaller tiles
* 1–4 hours for large files

You will see:

```
Processed 10000 features...
```

---

## 🏭 How the Script Works (Step-by-Step)

Think of the script as a **factory assembly line**:

* The CSV = box of raw materials
* The GDB = warehouse
* The script = machines that convert recipes (WKT) into real polygons

---

### Step 1: Import Toolboxes

```python
import arcpy
import csv
import os
```

These tools help with GIS operations, reading CSVs, and handling file paths.

---

### Step 2: The "Job Order" (Your Inputs)

```python
input_csv = r"..."
output_gdb = r"..."
output_fc_name = "..."
wkt_column_name = "..."
```

You tell the script:

* where the CSV is
* where the geodatabase is
* what to name the output
* which CSV column contains the WKT

---

### Step 3: Set Up the "Assembly Line"

```python
sr = arcpy.SpatialReference(4326)
output_fc = os.path.join(output_gdb, output_fc_name)
```

* Uses **WGS 84 (EPSG:4326)**
* Builds the full path for the new feature class

---

### Step 4: Build the Empty "Container"

```python
arcpy.management.CreateFeatureclass(...)
arcpy.management.AddField(...)
```

* Creates the empty polygon feature class
* Adds attribute fields like `confidence`

---

### Step 5: The Main Loop (Processing the CSV)

This is why the script succeeds when QGIS freezes.

```python
with arcpy.da.InsertCursor(output_fc, cursor_fields) as cursor:
```

This opens a high-speed loader door into your feature class.

Inside:

* opens the CSV
* reads the header
* finds the index of `geometry` and `confidence`
* loops through **every row**

For each row:

1. **Extract WKT and confidence**
2. **Convert WKT → Polygon**

```python
polygon_geometry = arcpy.FromWKT(wkt_string, sr)
```

3. **Insert into geodatabase**

```python
cursor.insertRow([polygon_geometry, confidence_val])
```

This repeats **millions of times** efficiently.

---

### Step 6: Progress Reports and Completion

```python
if row_count % 10000 == 0:
    print(f"Processed {row_count} features...")
```

After completion, everything closes automatically and a final message appears.

---

## 📄 License

This project is licensed under the **MIT License**.
