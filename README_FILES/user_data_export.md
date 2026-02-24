# User Data Export API Endpoint

## Overview
This API endpoint exports all user-related data from PostgreSQL to a SQLite database optimized for mobile use.

## Endpoint
```
GET /surveyor/users/{user_id}/export
```

## Parameters
- `user_id` (int): The ID of the user whose data should be exported

## Response
- **Success (200)**: Returns a SQLite database file (`mse-{user_id}.db`) as an attachment
- **Not Found (404)**: User not found or no data available for the user
- **Server Error (500)**: Database error or internal server error

## Usage Examples

### cURL
```bash
curl -X GET "http://localhost:8080/surveyor/users/123/export" \
     -H "Accept: application/octet-stream" \
     --output "mse-123.db"
```

### Python (requests)
```python
import requests

def download_user_data(user_id, output_path=None):
    url = f"http://localhost:8080/surveyor/users/{user_id}/export"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        filename = output_path or f"mse-{user_id}.db"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded user data to {filename}")
        return filename
    elif response.status_code == 404:
        print("User not found or no data available")
        return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Usage
download_user_data(123)
```

### JavaScript (fetch)
```javascript
async function downloadUserData(userId) {
    try {
        const response = await fetch(`/surveyor/users/${userId}/export`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mse-${userId}.db`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            console.error('Download failed:', response.statusText);
        }
    } catch (error) {
        console.error('Error downloading user data:', error);
    }
}

// Usage
downloadUserData(123);
```

## Exported Data Structure

The exported SQLite database contains the following tables with user-related data:

### Core Tables
- `tbl_user_surveyor` - User information
- `tbl_demandas` - User's demands/surveys
- `tbl_task_survey_boarding` - Survey tasks
- `tbl_notifications` - User notifications

### Cargo-Related Tables
- `tbl_cargo` - Cargo information
- `tbl_cargo_condition` - Cargo condition details
- `tbl_cargo_inspection` - Cargo inspection records
- `tbl_cargo_storage` - Cargo storage information

### Equipment Tables
- `tbl_lifting_material` - Lifting equipment
- `tbl_lifting_operation` - Lifting operations
- `tbl_lashing_material` - Lashing equipment
- `tbl_lashing_cargo` - Lashing operations

### Vessel-Related Tables
- `tbl_vessel` - Vessel information
- `tbl_vessel_crane` - Vessel crane details
- `tbl_swl_capacities` - Safe Working Load capacities

### Additional Tables
- `tbl_preliminary_checklist` - Preliminary checklists

## Data Filtering Logic

The endpoint uses a single optimized query to gather all related entity IDs:

```sql
WITH user_entities AS (
  SELECT 
    d.id_demanda,
    d.id_ship,
    t.id_task
  FROM tbl_demandas d
  LEFT JOIN tbl_task_survey_boarding t ON d.id_demanda = t.id_survey
  WHERE d.id_surveyor = :user_id
)
SELECT 
  ue.*,
  c.cargo_id,
  lm.id_lifting_material,
  lsh.id_lashing_material,
  v.vessel_id,
  vc.crane_id,
  swl.swl_capacity_id
FROM user_entities ue
LEFT JOIN tbl_cargo c ON ue.id_task = c.id_task
LEFT JOIN tbl_lifting_material lm ON ue.id_task = lm.id_task
LEFT JOIN tbl_lashing_material lsh ON ue.id_task = lsh.id_task
LEFT JOIN tbl_vessel v ON ue.id_ship = v.vessel_id
LEFT JOIN tbl_vessel_crane vc ON v.vessel_id = vc.vessel_id
LEFT JOIN tbl_swl_capacities swl ON vc.crane_id = swl.crane_id
```

This ensures only data related to the specific user is exported, maintaining data privacy and reducing file size.

## Error Handling

- **Validation**: Verifies user exists before proceeding
- **Rollback**: Database rollback on any insertion failure
- **Cleanup**: Automatic cleanup of temporary files
- **Logging**: Comprehensive logging for debugging

## Security Considerations

- Only exports data belonging to the specified user
- Validates all foreign key relationships
- Implements proper error handling to prevent data leaks
- Uses parameterized queries to prevent SQL injection

## Performance Notes

- Uses a single optimized query to gather all related IDs
- Implements batch insertion for efficient data transfer
- Creates indexes on the SQLite database for faster mobile queries
- Minimal memory footprint during export process
