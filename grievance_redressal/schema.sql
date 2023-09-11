DROP TABLE IF EXISTS grievance;
DROP TABLE IF EXISTS redressal;
DROP TABLE IF EXISTS user;

CREATE TABLE grievance (
  g_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  course TEXT NOT NULL,
  dept TEXT NOT NULL,
  sem TEXT NOT NULL,
  reg_no TEXT NOT NULL,
  roll_no TEXT NOT NULL,
  contact TEXT NOT NULL,
  email_id TEXT NOT NULL,
  grievance TEXT NOT NULL,
  datetime TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE redressal (
  r_id TEXT PRIMARY KEY,
  g_id TEXT NOT NULL,
  schedule TEXT,
  redressal TEXT NOT NULL,
  datetime TEXT NOT NULL,
  FOREIGN KEY (g_id) REFERENCES grievance (g_id)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
