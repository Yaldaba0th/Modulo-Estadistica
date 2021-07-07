DROP DATABASE igmava;

CREATE DATABASE igmava;

USE igmava;

CREATE TABLE Cliente(
	RUT VARCHAR(20) NOT NULL PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL,
	Procedencia VARCHAR(50),
	Telefono INT,
	Correo VARCHAR(50),
	Contacto VARCHAR(20)
);

CREATE TABLE Reserva(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	RUT VARCHAR(50) NOT NULL,
	Check_in DATE NOT NULL,
	Check_out DATE NOT NUll,
	Costo INT NOT NULL,
	Pagado BOOLEAN,
	FOREIGN KEY(RUT) REFERENCES Cliente(RUT)
);

CREATE TABLE Cabin(
	ID INT NOT NULL PRIMARY KEY,
	Precio INT NOT NULL
);

CREATE TABLE CabsRes(
	IDreserva INT NOT NULL,
	IDcabin INT NOT NULL,
	PRIMARY KEY (IDreserva, IDcabin),
	FOREIGN KEY(IDreserva) REFERENCES Reserva(ID),
	FOREIGN KEY(IDcabin) REFERENCES Cabin(ID)
);

CREATE TABLE ObsCab(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Cabin INT NOT NULL,
	Tipo VARCHAR(20) NOT NULL,
	Fecha DATE NOT NULL,
	Descripcion VARCHAR(500),
	Arreglado BOOLEAN,
	FOREIGN KEY(Cabin) REFERENCES Cabin(ID)
);

INSERT INTO Cliente
VALUES
('18345984-3', 'Juan Perez', 'Metropolitana', 92384857, 'asd@gmai.com', 'directo'),
('13948237-4', 'Maria Gonzales', 'Valparaiso', 84472647, 'example@hotmail.com', 'Airbnb'),
('9345872-k', 'Alberto Medina', 'Biobio', 83647183, 'ejemplo@uach.cl', 'directo'),
('9995872-k', 'Jose Josephson', 'Biobio', 43247183, 'exa@uach.cl', 'directo'),
('00000000-0', '0', '0', 0, '0', '0');

INSERT INTO Cabin
VALUES
(1, 50),
(2, 50),
(3, 50);

INSERT INTO Reserva
VALUES
(1, '18345984-3', '2020-12-10', '2020-12-15', '150', 0),
(2, '13948237-4', '2020-12-14', '2020-12-15', 80, 1),
(3, '9345872-k', '2020-12-16', '2020-12-20', 600, 0),
(4, '9345872-k', '2020-01-10', '2020-01-20', 600, 0),
(5, '9345872-k', '2021-12-01', '2021-12-20', 600, 0);

INSERT INTO CabsRes
VALUES
(1, 1),
(2, 2),
(3, 1),
(3, 2);

INSERT INTO ObsCab
VALUES
(1, 1, 'Electrico', '2020-01-01', 'Un problema electrico', 1),
(2, 1, 'Electrico', '2021-01-01', 'Otro problema electrico', 0);
