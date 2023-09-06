DROP TABLE IF EXISTS grievance;
DROP TABLE IF EXISTS redressal;

CREATE TABLE grievance (
  g_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  dept TEXT NOT NULL,
  sem TEXT NOT NULL,
  reg_no TEXT NOT NULL,
  roll_no TEXT NOT NULL,
  contact TEXT NOT NULL,
  email_id TEXT NOT NULL,
  grievance TEXT NOT NULL
);

CREATE TABLE redressal (
  r_id TEXT PRIMARY KEY,
  g_id TEXT NOT NULL,
  date TEXT,
  redressal TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (g_id) REFERENCES grievance (g_id)
);
