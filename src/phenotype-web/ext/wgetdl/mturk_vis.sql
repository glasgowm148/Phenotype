use pgvis_for_get;

DROP TABLE IF EXISTS mturk_dem;
DROP TABLE IF EXISTS mturk_pretask;
DROP TABLE IF EXISTS mturk_vis;

CREATE TABLE mturk_dem (
	user varchar(20),
	q1 varchar(20),
	q2 varchar(20),
	q3 varchar(20),
	q4 varchar(20),
	q5 varchar(20),
	q6 varchar(20),
	q7a varchar(20),
	q7b varchar(20),
	q7c varchar(20),
	q7d varchar(20),
	q7e varchar(20),
	q7f varchar(20),
	q7g varchar(20),
	q8 varchar(20),
	time int
	)
ENGINE = InnoDB;

CREATE TABLE mturk_pretask (
	user varchar(20),
	q1 varchar(20),
	q2 varchar(20),
	q3 varchar(20),
	q4 varchar(20),
	q5 varchar(20),
	q6 varchar(20),
	time int
	)
ENGINE = InnoDB;

CREATE TABLE mturk_vis (
	user varchar(20),
	q1 varchar(20),
	q2 varchar(20),
	q3 varchar(20),
	q4 varchar(20),
	q5 varchar(20),
	q6 varchar(20),
	q7 varchar(20),
	q8 varchar(20),
	q9a varchar(20),
	q9b varchar(20),
	q9c varchar(20),
	q9d varchar(20),
	q9e varchar(20),
	q9f varchar(20),
	q9g varchar(20),
	q9h varchar(20),
	p1 varchar(20),
	p2 varchar(20),
	p3 varchar(20),
	p4 varchar(20),
	p5 varchar(20),
	p6 varchar(20),
	p7 varchar(20),
	p8 varchar(20),
	p9 varchar(20),
	p10 varchar(20),
	p11 varchar(20),
	p12 varchar(20),
	p13 varchar(20),
	p14 varchar(20),
	i4 varchar(20),
	i5 varchar(20),
	time int
	)
ENGINE = InnoDB;