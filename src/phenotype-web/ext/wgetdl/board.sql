use pgvis_for_get;

DROP TABLE IF EXISTS board_user;
DROP TABLE IF EXISTS board_name;
DROP TABLE IF EXISTS link_board;
DROP TABLE IF EXISTS link_tag;

CREATE TABLE board_user (
	user_id varchar(10),
	board_id varchar(10)
	)
ENGINE = InnoDB;

CREATE TABLE board_name (
	board_id int NOT NULL AUTO_INCREMENT,
	board_name varchar(50),
	primary key (board_id)
	)
ENGINE = InnoDB;

CREATE TABLE link_board (
	link_id int NOT NULL AUTO_INCREMENT,
	link_title varchar(100),
	link_address varchar(100),
	board_id int NOT NULL,
	primary key (link_id)
	)
ENGINE = InnoDB;

CREATE TABLE link_tag (
	link_id int NOT NULL,
	tag varchar(20)
	)
ENGINE = InnoDB;