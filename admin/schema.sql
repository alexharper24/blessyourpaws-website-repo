-- The Bless Your Paws owner editor's database (D1, its own, in the Bless Your Paws account).
--
-- IF NOT EXISTS throughout, so running this against an existing database does nothing.
--
-- Each content row keeps the WHOLE record as it appears in data/*.json, in `doc`. That is
-- deliberate, and it is the main way this editor differs from Teapup's. The export has to
-- reproduce the files byte for byte, including key order, and a record kept as its own JSON
-- keeps its key order through every save without a shape table to maintain. The few columns
-- beside it exist only for ordering, conflict checks and lookups.
--
-- NO BUYER DATA. A puppy is available, reserved or adopted. Who reserved or adopted her is
-- not stored here, and there is no table for it.
--
-- NO DELETES. Nothing in the editor removes a puppy, a litter, a parent, a review or a photo.
-- A review can be hidden and a litter can be moved to past litters. The one exception is a
-- record created since the last publish, which Undo can take away again because the site
-- never had it.

CREATE TABLE IF NOT EXISTS people (
  email        TEXT PRIMARY KEY COLLATE NOCASE,
  display_name TEXT NOT NULL,
  is_admin     INTEGER NOT NULL DEFAULT 0,
  added_at     TEXT NOT NULL,
  added_by     TEXT NOT NULL
);

-- One table per data file. `key` is the record's slug, or for reviews a generated id.
CREATE TABLE IF NOT EXISTS records (
  file        TEXT NOT NULL CHECK (file IN ('puppies','litters','adults','reviews')),
  key         TEXT NOT NULL,
  doc         TEXT NOT NULL,
  sort_order  INTEGER NOT NULL,
  version     INTEGER NOT NULL DEFAULT 1,
  updated_at  TEXT NOT NULL,
  updated_by  TEXT NOT NULL,
  PRIMARY KEY (file, key)
);

-- A photograph uploaded in the editor, held here until a publish commits it to the repo.
-- The bytes live in this table rather than in R2 (decided 2026-10-16): the browser resizes
-- every photo to at most 2000px before it is sent, so each is well under D1's 2 MB row
-- limit, and it keeps the editor to one storage service with nothing more to subscribe to.
CREATE TABLE IF NOT EXISTS uploads (
  key         TEXT PRIMARY KEY,           -- pending/<folder>/<stem>.jpg
  repo_path   TEXT NOT NULL UNIQUE,       -- uploads/<folder>/<stem>.<ext>
  stem        TEXT NOT NULL UNIQUE,       -- what data/*.json names, e.g. eden-22
  owner_file  TEXT NOT NULL,
  owner_key   TEXT NOT NULL,
  bytes       INTEGER NOT NULL,
  data        BLOB NOT NULL,
  committed   INTEGER NOT NULL DEFAULT 0,
  created_at  TEXT NOT NULL,
  created_by  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  file        TEXT,
  key         TEXT,
  action      TEXT NOT NULL,
  detail      TEXT,
  actor       TEXT NOT NULL,
  created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publishes (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  actor        TEXT NOT NULL,
  summary_json TEXT,
  commit_sha   TEXT,
  started_at   TEXT NOT NULL,
  finished_at  TEXT,
  outcome      TEXT
);
