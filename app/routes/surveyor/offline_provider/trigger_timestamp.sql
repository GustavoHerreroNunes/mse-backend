-- For Postgresql
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON your_table
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();


-- For Sqlite
CREATE TRIGGER update_timestamp
BEFORE UPDATE ON tbl_cargo
FOR EACH ROW
WHEN OLD.last_modified = NEW.last_modified
BEGIN
  UPDATE tbl_cargo
  SET last_modified = CURRENT_TIMESTAMP,
  sync_action = 'update',
  is_synced = 0
  WHERE rowid = NEW.rowid;
END;

-- Modify tables on create to have default 'create' and 'is_synced' 0 and 'last_modified' CURRENT_TIMESTAMP :rocket:!!!!