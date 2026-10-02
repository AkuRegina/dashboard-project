# deviation_dashboard database setup

## Setup

1. Install PostgreSQL and pgAdmin for your convenience, without pgAdmin you will have to execute files with `psql` from the command line.
2. Create a database called `deviation_dashboard`.
3. Set the database owner to your local `postgres` user.
4. Open `Tools -> Query Tool`.
5. Run `schema.sql`.
6. Run `dummy_data.sql`.

You can either open the SQL files directly in Query Tool or copy their contents there and execute them.

## Important

Running `schema.sql` again will recreate the tables and delete the current data.

After that, you will need to run `dummy_data.sql` again to add the data back.

The values in `password_hash` are only placeholders. Real password hashing will be handled by the backend later.

## Views

In order to see deviations with proper naming instead of ids, use:

```sql
SELECT * FROM deviation_details;