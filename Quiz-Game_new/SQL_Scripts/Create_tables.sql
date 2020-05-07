USE questions;
DROP TABLE IF EXISTS maths;
CREATE TABLE maths
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
type	 VARCHAR(10)  CHECK (type = 'mcq' OR type = 'true/false' OR type = 'oneWord') NOT NULL,
optionA  VARCHAR(10),
optionB  VARCHAR(10),
optionC  VARCHAR(10),
optionD  VARCHAR(10),
ansMcq   CHAR(1) CHECK (ansMcq = 'a' OR ansMcq = 'b' OR ansMcq = 'c' OR ansMcq = 'd'),
ansTf    CHAR(1) CHECK (ansTf = 't' OR ansTf = 'f'),
ansOw    VARCHAR(20)
);

DROP TABLE IF EXISTS sci;
CREATE TABLE sci
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
type	 VARCHAR(10)  CHECK (type = 'mcq' OR type = 'true/false' OR type = 'oneWord') NOT NULL,
optionA  VARCHAR(10),
optionB  VARCHAR(10),
optionC  VARCHAR(10),
optionD  VARCHAR(10),
ansMcq   CHAR(1) CHECK (ansMcq = 'a' OR ansMcq = 'b' OR ansMcq = 'c' OR ansMcq = 'd'),
ansTf    CHAR(1) CHECK (ansTf = 't' OR ansTf = 'f'),
ansOw    VARCHAR(20)
);

DROP TABLE IF EXISTS gk;
CREATE TABLE gk
(
Q_num    INT		  PRIMARY KEY,
question VARCHAR(255) NOT NULL,
type	 VARCHAR(10)  CHECK (type = 'mcq' OR type = 'true/false' OR type = 'oneWord') NOT NULL,
optionA  VARCHAR(10),
optionB  VARCHAR(10),
optionC  VARCHAR(10),
optionD  VARCHAR(10),
ansMcq   CHAR(1) CHECK (ansMcq = 'a' OR ansMcq = 'b' OR ansMcq = 'c' OR ansMcq = 'd'),
ansTf    CHAR(1) CHECK (ansTf = 't' OR ansTf = 'f'),
ansOw    VARCHAR(20)
);
