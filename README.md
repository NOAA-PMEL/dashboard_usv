# Saildrone Dashboard
A general purpose application viewing a collection of saildrones.

The saildrones, along with some information that will be used to make the header (title, organization logos, and information URL) and some menu option configuration for selecting drones can be specified in an external .json configuration file. See the .json fies in the source for examples.

# Mission Configuration & Database Seeding Guide

This guide details how to add new USV missions to the dashboard, manage active mission updates, and seed the database using `tasks.py`.

---

## 1. Adding a Mission to `config/missions.json`

Missions are grouped by collection year/type inside `config/missions.json`. To add a new mission, locate or create the corresponding collection key under `"collections"` and add your mission object under `"missions"`.

### Configuration Template

```json
{
  "collections": {
    "usv2026": {
      "title": "2026 USV Missions",
      "missions": {
        "2026_1_atlantic_hurricane": {
          "active": "true",
          "downloads": "false",
          "ui": {
            "title": "2026 Atlantic Hurricane (Saildrones)",
            "href": "https://research.noaa.gov/...",
            "max_columns": "3"
          },
          "drones": {
            "1030": {
              "url": "https://data.pmel.noaa.gov/pmel/erddap/tabledap/sd1030_hurricane_2026",
              "label": "1030"
            }
          }
        }
      }
    }
  }
}
```

### Field Definitions

* **Collection Key** (e.g., `usv2026`): Categorizes groups of missions.
* **Mission Key** (e.g., `2026_1_atlantic_hurricane`): Unique mission identifier (`mid`) used internally by the database and Redis cache.
* **`active`**: String (`"true"` or `"false"`). Dictates update behavior during routine update runs.
* **`downloads`**: String (`"true"` or `"false"`). Controls data download availability in the UI.
* **`ui`**: Formatting options for the dashboard display:
  * **`title`**: Display name for the mission.
  * **`href`**: URL link to external mission information.
  * **`link_text`** *(optional)*: Display text for the external link.
  * **`max_columns`**: Column layout formatting for the UI.
  * **`days_ago`** *(optional)*: Filter threshold for displaying recent data.
* **`drones`**: Object containing drone identifiers:
  * **`url`**: The ERDDAP `tabledap` endpoint supplying location and sensor telemetry.
  * **`label`**: Display label for the vehicle.

---

## 2. How the `active` Flag Works

The `load_missions()` function in `tasks.py` evaluates whether to update data for a given mission based on the following logic:

```python
if mission_exists_df.empty or force or mission['active'] == 'true':
    df = update_mission(mid, mission)
```

* **`"active": "true"`**: Forces `update_mission()` to run during every execution. It re-queries ERDDAP endpoints for fresh track data, deletes previous location records for the mission from PostgreSQL, appends updated locations, and updates Redis metadata.
* **`"active": "false"`**: The mission is treated as historical. If records already exist in the database, `load_missions()` skips updating it. It will only update if the database has no prior records for that mission ID or if `force=True` is passed.

---

## 3. Seeding the Database via `tasks.py`

To populate PostgreSQL with initial trajectory data and store mission metadata in Redis prior to launch, execute `load_missions()` from a Python environment.

### Execution Steps

1. **Navigate to the application root directory** containing `tasks.py` and the `config/` directory.
2. **Launch Python interactive shell**:
   ```bash
   python
   ```
3. **Import and execute the loader**:
   ```python
   import tasks

   # Standard update: loads new/empty missions and updates active ones
   tasks.load_missions()
   ```

### Forcing a Full Database Reload

If you need to replace all existing database records and re-fetch data for all active and historical missions from scratch, set `force=True`:

```python
import tasks

# Force re-download and re-creation of all location tables
tasks.load_missions(force=True)
```


#### Legal Disclaimer
*This repository is a software product and is not official communication
of the National Oceanic and Atmospheric Administration (NOAA), or the
United States Department of Commerce (DOC).  All NOAA GitHub project
code is provided on an 'as is' basis and the user assumes responsibility
for its use.  Any claims against the DOC or DOC bureaus stemming from
the use of this GitHub project will be governed by all applicable Federal
law.  Any reference to specific commercial products, processes, or services
by service mark, trademark, manufacturer, or otherwise, does not constitute
or imply their endorsement, recommendation, or favoring by the DOC.
The DOC seal and logo, or the seal and logo of a DOC bureau, shall not
be used in any manner to imply endorsement of any commercial product
or activity by the DOC or the United States Government.*