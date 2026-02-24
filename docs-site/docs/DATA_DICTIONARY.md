# Data Dictionary

## Overview
This document defines every field in the `nyc311_clean` table in the SQLite database. Fields are organized into four categories: identifiers, complaint details, location, and derived columns.

**Null Policy Legend**
| Policy | Meaning |
|--------|---------|
| NOT NULL | Field must always be populated — null values are a DQ violation |
| NULLABLE | Field may be null under defined conditions |
| CONDITIONAL | Field nullability depends on another field's value |

---

## Identifiers

### unique_key
| Attribute | Detail |
|-----------|--------|
| Type | INTEGER |
| Null Policy | NOT NULL |
| Description | Unique identifier for each service request assigned by NYC 311 |
| Source Field | `unique_key` |
| DQ Rule | DQ-005 — must be unique across all records |

### created_date
| Attribute | Detail |
|-----------|--------|
| Type | DATETIME |
| Null Policy | NOT NULL |
| Description | Date and time the service request was created |
| Source Field | `created_date` |
| Format | YYYY-MM-DD HH:MM:SS |
| Notes | Parsed from string to datetime in transform.py |

### closed_date
| Attribute | Detail |
|-----------|--------|
| Type | DATETIME |
| Null Policy | CONDITIONAL |
| Description | Date and time the service request was closed |
| Source Field | `closed_date` |
| Format | YYYY-MM-DD HH:MM:SS |
| Notes | Null when complaint is still open. Must be populated when is_open = False |
| DQ Rule | DQ-004 — must be consistent with is_open flag |

---

## Complaint Details

### agency
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | Acronym of the responding agency (e.g. NYPD, DSNY, DEP) |
| Source Field | `agency` |

### agency_name
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | Full name of the responding agency |
| Source Field | `agency_name` |

### complaint_type
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | High level category of the complaint (e.g. Noise - Residential, Illegal Parking) |
| Source Field | `complaint_type` |
| Notes | Title-cased in transform.py |

### descriptor
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | Specific description of the complaint within the complaint type category |
| Source Field | `descriptor` |
| DQ Rule | DQ-001 — must not be null |

### location_type
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NULLABLE |
| Description | Type of location where the complaint was reported (e.g. Street, Residential Building) |
| Source Field | `location_type` |

### status
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | Current status of the service request (e.g. Open, Closed, Pending) |
| Source Field | `status` |
| Notes | Title-cased in transform.py |

### resolution_description
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | CONDITIONAL |
| Description | Description of how the complaint was resolved |
| Source Field | `resolution_description` |
| Notes | Expected to be populated for closed complaints. Null for open complaints is acceptable |
| DQ Rule | DQ-006 — closed complaints should have resolution description |

### resolution_action_updated_date
| Attribute | Detail |
|-----------|--------|
| Type | DATETIME |
| Null Policy | CONDITIONAL |
| Description | Date the resolution action was last updated |
| Source Field | `resolution_action_updated_date` |
| Format | YYYY-MM-DD HH:MM:SS |

---

## Location

### incident_zip
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NULLABLE |
| Description | 5-digit US zip code of the incident location |
| Source Field | `incident_zip` |
| Format | 5-digit zero-padded string (e.g. 10001) |
| Notes | Converted from float64 to zero-padded string in transform.py |
| DQ Rule | DQ-002 — must match 5-digit format |

### incident_address
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NULLABLE |
| Description | Street address of the incident |
| Source Field | `incident_address` |

### street_name
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NULLABLE |
| Description | Street name of the incident location |
| Source Field | `street_name` |

### city
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NULLABLE |
| Description | City of the incident location |
| Source Field | `city` |
| Notes | Title-cased in transform.py |

### borough
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | NYC borough of the incident (Brooklyn, Queens, Bronx, Manhattan, Staten Island) |
| Source Field | `borough` |
| Notes | Title-cased in transform.py |
| Acceptable Values | Brooklyn, Queens, Bronx, Manhattan, Staten Island, Unspecified |

### community_board
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | NYC community board number for the incident location |
| Source Field | `community_board` |

### council_district
| Attribute | Detail |
|-----------|--------|
| Type | INTEGER |
| Null Policy | NULLABLE |
| Description | NYC council district number for the incident location |
| Source Field | `council_district` |
| Notes | Converted from float64 to Int64 in transform.py |

### police_precinct
| Attribute | Detail |
|-----------|--------|
| Type | STRING |
| Null Policy | NOT NULL |
| Description | NYPD precinct number for the incident location |
| Source Field | `police_precinct` |

### latitude
| Attribute | Detail |
|-----------|--------|
| Type | FLOAT |
| Null Policy | NULLABLE |
| Description | Latitude coordinate of the incident location |
| Source Field | `latitude` |
| DQ Rule | DQ-003 — must be present if longitude is present |

### longitude
| Attribute | Detail |
|-----------|--------|
| Type | FLOAT |
| Null Policy | NULLABLE |
| Description | Longitude coordinate of the incident location |
| Source Field | `longitude` |
| DQ Rule | DQ-003 — must be present if latitude is present |

### x_coordinate_state_plane
| Attribute | Detail |
|-----------|--------|
| Type | FLOAT |
| Null Policy | NULLABLE |
| Description | X coordinate in NY State Plane coordinate system |
| Source Field | `x_coordinate_state_plane` |

### y_coordinate_state_plane
| Attribute | Detail |
|-----------|--------|
| Type | FLOAT |
| Null Policy | NULLABLE |
| Description | Y coordinate in NY State Plane coordinate system |
| Source Field | `y_coordinate_state_plane` |

---

## Derived Columns
These columns do not exist in the source data — they are created in `transform.py`.

### is_open
| Attribute | Detail |
|-----------|--------|
| Type | BOOLEAN |
| Null Policy | NOT NULL |
| Description | True if the complaint is still open, False if closed |
| Derived From | `closed_date` — True when closed_date is null |
| DQ Rule | DQ-004 — must be consistent with closed_date |

### resolution_hours
| Attribute | Detail |
|-----------|--------|
| Type | FLOAT |
| Null Policy | CONDITIONAL |
| Description | Number of hours between created_date and closed_date |
| Derived From | `closed_date` - `created_date` in hours |
| Notes | Null when complaint is still open (is_open = True) |

### created_year
| Attribute | Detail |
|-----------|--------|
| Type | INTEGER |
| Null Policy | NOT NULL |
| Description | Year the complaint was created — extracted for reporting |
| Derived From | `created_date` |

### created_month
| Attribute | Detail |
|-----------|--------|
| Type | INTEGER |
| Null Policy | NOT NULL |
| Description | Month the complaint was created — extracted for reporting |
| Derived From | `created_date` |
| Range | 1-12 |

---

## Dropped Columns
These columns existed in the raw source data but were removed in `transform.py` due to 90%+ null rates.

| Column | Null Rate | Reason Dropped |
|--------|-----------|----------------|
| facility_type | 100% | No analytical value |
| due_date | 100% | No analytical value |
| descriptor_2 | 91.7% | Insufficient coverage |
| vehicle_type | 95.8% | Insufficient coverage |
| taxi_company_borough | 99.9% | Insufficient coverage |
| taxi_pick_up_location | 99.3% | Insufficient coverage |
| bridge_highway_name | 99.2% | Insufficient coverage |
| bridge_highway_direction | 99.5% | Insufficient coverage |
| road_ramp | 99.4% | Insufficient coverage |
| bridge_highway_segment | 99.2% | Insufficient coverage |
| landmark | 9.5% | No governance value |
| bbl | 7.6% | No governance value |