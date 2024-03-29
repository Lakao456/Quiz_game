USE questions;
DROP TABLE IF EXISTS maths;
CREATE TABLE maths
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
qtype	 VARCHAR(100) NOT NULL,
optionA  VARCHAR(100),
optionB  VARCHAR(100),
optionC  VARCHAR(100),
optionD  VARCHAR(100),
answer 	 VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS sci;
CREATE TABLE sci
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
qtype	 VARCHAR(100) NOT NULL,
optionA  VARCHAR(100),
optionB  VARCHAR(100),
optionC  VARCHAR(100),
optionD  VARCHAR(100),
answer 	 VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS gk;
CREATE TABLE gk
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
qtype	 VARCHAR(100) NOT NULL,
optionA  VARCHAR(100),
optionB  VARCHAR(100),
optionC  VARCHAR(100),
optionD  VARCHAR(100),
answer 	 VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS eng;
CREATE TABLE eng
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
qtype	 VARCHAR(100) NOT NULL,
optionA  VARCHAR(100),
optionB  VARCHAR(100),
optionC  VARCHAR(100),
optionD  VARCHAR(100),
answer 	 VARCHAR(100) NOT NULL
);
