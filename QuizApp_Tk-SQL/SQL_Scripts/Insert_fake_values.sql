USE questions;

DELETE FROM maths;
DELETE FROM sci;
DELETE FROM gk;

INSERT INTO maths VALUES
(1, 'abc', 'mcq', 'a', 'b', 'c', 'd', 'c'),
(2, 'def', 'true/false', null, null, null, null, 't'),
(3, 'ghi', 'oneWord', null, null, null, null, 'xyz');

INSERT INTO sci VALUES
(1, 'How many states of matter are there?', 'mcq', '2', '1', '4', '3', 'c'),
(2, 'def', 'true/false', null, null, null, null, 't'),
(3, 'ghi', 'what is the powerouse of the cell', null, null, null, null, 'mitochondria'),
(4, 'def', 'true/false', null, null, null, null, 't');

INSERT INTO gk VALUES
(1, 'How many moons does mars have?', 'mcq', '1', '4', '3', '2', 'd'),
(2, 'def', 'true/false', null, null, null, null, 't'),
(3, 'ghi', 'oneWord', null, null, null, null, 'xyz');
