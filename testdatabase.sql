

CREATE TABLE Landlord (
landlordID    INTEGER NOT NULL,
name          VARCHAR(50),

PRIMARY KEY (landlordID)
);
CREATE TABLE Property (
propertyID			      INTEGER NOT NULL,
province		   VARCHAR(50) NOT NULL,
street			VARCHAR(50) NOT NULL,
postcode		   CHAR(6) NOT NULL,
price			   DECIMAL(10,2),
monthlyIncome	DECIMAL(20,2),
lotSize		   INTEGER,
buildDate		YEAR,
landlordID		INTEGER,

PRIMARY KEY (propertyID)
);
CREATE TABLE MonthlyExpenses (
propertyID	INTEGER NOT NULL,
date		   DATE,
landID		INTEGER NOT NULL,

PRIMARY KEY (propertyID, date),
FOREIGN KEY (propertyID) REFERENCES Property(propertyID)
);
CREATE TABLE Tenant (
tenantID		   INTEGER NOT NULL,
monthlyRent	   DECIMAL(10,2),

PRIMARY KEY (tenantID)
);
CREATE TABLE Individual (
tenantID	   INTEGER NOT NULL,
name		   VARCHAR(50) NOT NULL,
firstName	VARCHAR(50) NOT NULL,
lastName	   VARCHAR(50) NOT NULL,

PRIMARY KEY (tenantID),
FOREIGN KEY (tenantID) REFERENCES Tenant(tenantID)
);
CREATE TABLE Company (
tenantID		INTEGER NOT NULL,
companyName	VARCHAR(50) NOT NULL,

PRIMARY KEY (tenantID),
FOREIGN KEY (tenantID) REFERENCES Tenant(tenantID)
);
CREATE TABLE Rents (
propertyID		INTEGER NOT NULL,
tenantID		   INTEGER NOT NULL,

PRIMARY KEY (propertyID, tenantID),
FOREIGN KEY (tenantID) REFERENCES Tenant(tenantID),
FOREIGN KEY (propertyID) REFERENCES Property(propertyID)
);
CREATE TABLE Retail (
propertyID	INTEGER NOT NULL,

PRIMARY KEY (propertyID),
FOREIGN KEY (propertyID) REFERENCES Property(propertyID)
);
CREATE TABLE Office (
propertyID	INTEGER NOT NULL,
furnished	VARCHAR(50) NOT NULL,

PRIMARY KEY (PropertyID),
FOREIGN KEY (PropertyID) REFERENCES Property(propertyID)
);
CREATE TABLE Multifamily (
propertyID	INTEGER NOT NULL,
spaces	   VARCHAR(50) NOT NULL,
furnished	VARCHAR(50) NOT NULL,

PRIMARY KEY (propertyID),
FOREIGN KEY (PropertyID) REFERENCES Property(propertyID)
);
CREATE TABLE Spaces(
propertyID	INTEGER NOT NULL,
space		   INTEGER NOT NULL,

PRIMARY KEY (propertyID),
FOREIGN KEY (propertyID) REFERENCES Multifamily(propertyID)
);


INSERT INTO Landlord (landlordID, name) VALUES (1, "John Jackson");





COMMIT;
