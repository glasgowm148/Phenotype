use pgvis_for_get;

DROP TABLE IF EXISTS entry_tag;
DROP TABLE IF EXISTS entry_variant;
DROP TABLE IF EXISTS save_info;
DROP TABLE IF EXISTS variant;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS saved_variant;
DROP TABLE IF EXISTS entry;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS saved_tag;

CREATE TABLE variant (
	name varchar(20) NOT NULL,
	type varchar(20),
	certainty varchar(20),
	health_effect varchar(20),
	risk int,
	id int NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE category (
	variant int NOT NULL,
	category varchar(50)
	)
ENGINE = InnoDB;

CREATE TABLE saved_variant (
	user varchar(20) NOT NULL,
	variant varchar(20) NOT NULL,
	accordion int,
	notebook int,
	id int NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE entry (
	id int NOT NULL AUTO_INCREMENT,
	title varchar(200),
	url varchar(200),
	summary varchar(1000),
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE saved_tag (
	id int NOT NULL AUTO_INCREMENT,
	user varchar(20),
	tag varchar(100),
	notebook int,
	PRIMARY KEY (id)
	)
ENGINE = InnoDB;

CREATE TABLE entry_tag (
	entry int,
	tag int
	)
ENGINE = InnoDB;

CREATE TABLE entry_variant (
	entry int,
	variant int
	)
ENGINE = InnoDB;

CREATE TABLE save_info (
	saved_variant int NOT NULL,
	carrier varchar(20)
	)
ENGINE = InnoDB;
