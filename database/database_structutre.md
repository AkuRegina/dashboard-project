# Database structure

## users table

- `user_id` - Primary Key
- `f_name`
- `l_name`
- `email`
- `password_hash`

---

## severity table

- `severity_id` - Primary Key
- `name`

Example values:
- Low
- Medium
- High
- Critical

---

## concern_types

- `concern_type_id` - Primary Key
- `name`

Example values:
- Safety Concern
- Installation Issue
- Quality Issue
- Material Issue
- Other

---

## deviations

Main table

- `deviation_id` - Primary Key
- `ship`
- `concern_type_id` - Foreign Key -> `concern_types.concern_type_id`
- `severity_id` - Foreign Key -> `severity.severity_id`
- `description`
- `status`
- `deadline`
- `submitted_by` - Foreign Key -> `users.user_id`
- `assigned_to` - Foreign Key -> `users.user_id`
- `created_at`

`submitted_by` stores the user who created the deviation.

`assigned_to` stores the user responsible for the deviation and can be NULL.

---

## comments

- `comment_id` - Primary Key
- `deviation_id` - Foreign Key -> `deviations.deviation_id`
- `user_id` - Foreign Key -> `users.user_id`
- `comment_text`
- `created_at`

If a deviation is deleted, its comments are deleted automatically.

---

## Views

### deviation_details view

Joins:

- `deviations.concern_type_id` -> `concern_types.concern_type_id`
- `deviations.severity_id` -> `severity.severity_id`
- `deviations.submitted_by` -> `users.user_id`
- `deviations.assigned_to` -> `users.user_id`

It can be used with:

```sql
SELECT * FROM deviation_details;