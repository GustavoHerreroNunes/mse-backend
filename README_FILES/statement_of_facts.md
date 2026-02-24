# Statement of Facts API Module

## Overview

The Statement of Facts module provides comprehensive CRUD operations for managing operation logs and milestone tracking in the MSE system. This module handles the `tbl_statement_of_facts` table which stores critical operational events and their associated metadata.

## Database Schema

### tbl_statement_of_facts
- `event_id` (SERIAL PRIMARY KEY): Unique identifier for each event
- `milestone_name` (VARCHAR(50) NOT NULL): References tbl_sof_milestones.milestone_name
- `event_timestamp` (TIMESTAMPTZ NOT NULL DEFAULT NOW()): When the event occurred
- `status` (VARCHAR(8) NOT NULL): Event status ('Active' or 'Finished')
- `survey_id` (INT NOT NULL): Associated survey identifier
- `cargo_id` (INT): Optional cargo identifier
- `lifting_id` (INT): Optional lifting operation identifier
- `lashing_id` (INT): Optional lashing operation identifier
- `location` (TEXT): Optional location description

### tbl_sof_milestones
- `milestone_name` (VARCHAR(50) PRIMARY KEY): Valid milestone names

## Features

### Dynamic Validation
- **Milestone Name Validation**: Automatically validates that milestone_name exists in tbl_sof_milestones table
- **Status Validation**: Ensures status is either 'Active' or 'Finished'
- **Schema Validation**: Uses Marshmallow for comprehensive data validation

### Full CRUD Operations
1. **Create** (POST /statement-of-facts)
2. **Read** (GET /statement-of-facts/{event_id})
3. **Update** (PUT /statement-of-facts/{event_id})
4. **Delete** (DELETE /statement-of-facts/{event_id})

### Additional Query Operations
- **Get by Survey** (GET /statement-of-facts/survey/{survey_id})
- **Get by Event** (GET /statement-of-facts/event/{event_id})

## API Endpoints

### POST /statement-of-facts
Creates a new statement of facts entry.

**Required Fields:**
- `milestone_name`: Must exist in tbl_sof_milestones
- `status`: 'Active' or 'Finished'
- `survey_id`: Integer

**Optional Fields:**
- `event_timestamp`: ISO format datetime (defaults to NOW())
- `cargo_id`: Integer
- `lifting_id`: Integer
- `lashing_id`: Integer
- `location`: String

### GET /statement-of-facts/{event_id}
Retrieves a specific statement of facts entry by event ID.

### PUT /statement-of-facts/{event_id}
Updates an existing statement of facts entry. Supports partial updates.

### DELETE /statement-of-facts/{event_id}
Deletes a statement of facts entry by event ID.

### GET /statement-of-facts/survey/{survey_id}
Retrieves all statement of facts entries for a specific survey, ordered by timestamp (DESC).

### GET /statement-of-facts/event/{event_id}
Alternative endpoint to retrieve a statement of facts entry by event ID with 404 error handling.

## Error Handling

- **400**: Validation errors, missing required fields
- **404**: Record not found
- **500**: Internal server errors

All errors return JSON responses with descriptive error messages.

## Integration

The module is integrated into the Flask application through:
- Blueprint registration in `app/__init__.py`
- Route imports in `app/routes/__init__.py`
- API documentation in `api-gateway.yaml`

## Usage Example

```python
# Creating a new statement of facts entry
payload = {
    "milestone_name": "CARGO_LOADING_START",
    "status": "Active",
    "survey_id": 123,
    "cargo_id": 456,
    "location": "Port of Santos, Berth 12"
}

# POST /statement-of-facts
# Content-Type: application/json
# Body: payload
```

## File Structure

```
app/routes/surveyor/statement_of_facts/
├── __init__.py                           # Blueprint definition
├── schema.py                            # Marshmallow schema with validation
├── options.py                           # CORS OPTIONS handlers
├── add_statement_of_facts.py           # POST endpoint
├── get_statement_of_facts.py           # GET by event_id endpoint
├── get_statement_of_facts_by_survey.py # GET by survey_id endpoint
├── get_statement_of_facts_by_event.py  # GET by event_id (alternative)
├── update_statement_of_facts.py        # PUT endpoint
└── delete_statement_of_facts.py        # DELETE endpoint
```

## Dependencies

- Flask
- SQLAlchemy
- Marshmallow
- Flask-Marshmallow

The module follows the same patterns and conventions used throughout the MSE API codebase, ensuring consistency and maintainability.
