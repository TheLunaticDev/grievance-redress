DROP TABLE IF EXISTS grievance;
DROP TABLE IF EXISTS redressal;

CREATE TABLE grievance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  dept TEXT NOT NULL,
  sem TEXT NOT NULL,
  reg_no TEXT UNIQUE NOT NULL,
  roll_no TEXT NOT NULL,
  contact TEXT NOT NULL,
  email_id TEXT,
  grievance TEXT NOT NULL
);

CREATE TABLE redressal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grievance_id INTEGER NOT NULL,
  date TEXT,
  redressal TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (grievance_id) REFERENCES grievance (id)
);
