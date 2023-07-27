CREATE TABLE SecullumAcesso.dbo.dashboard_user (
	id_dashboard_user int IDENTITY(0,1) NOT NULL,
	user_name varchar(150) NOT NULL,
	password varchar(250) NOT NULL
);

CREATE TABLE SecullumAcesso.dbo.pessoas_adicionais (
	id_pessoas_adicionais int IDENTITY(0,1) NOT NULL,
	pessoa_id int NOT NULL,
	line int NULL
);

CREATE TABLE SecullumAcesso.dbo.lines (
	id int IDENTITY(0,1) NOT NULL,
	desc_line varchar(150) NULL
);
