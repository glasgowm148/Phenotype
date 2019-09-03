use pgvis_for_get;

DROP TABLE IF EXISTS PGP_variant;
DROP TABLE IF EXISTS PGP_category;
DROP TABLE IF EXISTS PGP_entry;
DROP TABLE IF EXISTS PGP_tag;
DROP TABLE IF EXISTS PGP_entry_tag;
DROP TABLE IF EXISTS PGP_user_variant;
DROP TABLE IF EXISTS PGP_variant_category;
DROP TABLE IF EXISTS PGP_entry_category;

CREATE TABLE PGP_variant (
	name varchar(20) NOT NULL,
	summary varchar(2000),
	risk varchar(20),
	rarity varchar(20),
	certainty varchar(20),
	health_effect varchar(20),
	impact varchar(20),
	PRIMARY KEY (name)
	)
ENGINE = InnoDB;

CREATE TABLE PGP_category (
	name varchar(50),
	id int AUTO_INCREMENT,
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE PGP_entry (
	id int NOT NULL AUTO_INCREMENT,
	user varchar(20),
	title varchar(200),
	url varchar(200),
	description varchar(2000),
	additional varchar(2000),
	type varchar(20),
	notebook int, 
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE PGP_tag (
	id int NOT NULL AUTO_INCREMENT,
	user varchar(20),
	title varchar(100),
	notebook int,
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE PGP_user_variant (
	user varchar(20) NOT NULL,
	variant varchar(20) NOT NULL,
	accordion int,
	notebook int,
	affected int,
	PRIMARY KEY (user,variant)
	)
ENGINE = InnoDB;

CREATE TABLE PGP_entry_tag (
	entry int,
	tag int
	)
ENGINE = InnoDB;

CREATE TABLE PGP_entry_category (
	entry int,
	category int
	)
ENGINE = InnoDB;

CREATE TABLE PGP_variant_category (
	variant varchar(20),
	category varchar(50),
	PRIMARY KEY (variant,category)
	)
ENGINE = InnoDB;

INSERT INTO PGP_category VALUES ("Anatomical & Congenital", 1);
INSERT INTO PGP_category VALUES ("Blood", 2);
INSERT INTO PGP_category VALUES ("Breathing", 3);
INSERT INTO PGP_category VALUES ("Cancer", 4);
INSERT INTO PGP_category VALUES ("Drug Response", 5);
INSERT INTO PGP_category VALUES ("Genital & Urinary", 6);
INSERT INTO PGP_category VALUES ("Hearing & Vision", 7);
INSERT INTO PGP_category VALUES ("Heart & Circulatory", 8);
INSERT INTO PGP_category VALUES ("Immune System", 9);
INSERT INTO PGP_category VALUES ("Mental & Behavioral", 10);
INSERT INTO PGP_category VALUES ("Metabolism", 11);
INSERT INTO PGP_category VALUES ("Mouth, Liver, & Digestive", 12);
INSERT INTO PGP_category VALUES ("Muscular, Skeletal, <br>& Connective Tissue", 13);
INSERT INTO PGP_category VALUES ("Nervous System", 14);
INSERT INTO PGP_category VALUES ("Skin", 15);
INSERT INTO PGP_category VALUES ("Other", 16);

