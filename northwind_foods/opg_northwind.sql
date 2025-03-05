-- select * from products order by UnitPrice desc;

-- select * from customers where Country = "UK" or Country = "Spain";
-- select count(*) from customers where Country = "UK" or Country = "Spain"; -- correct number of rows (12)


-- select * from products where UnitsInStock >= 100 and UnitPrice >= 25;
-- select count(*) from products where UnitsInStock > 100 and UnitPrice >= 25; -- Exercise says 10 rows, but got 2 

-- select distinct ShipCountry from orders;
-- select count(distinct ShipCountry) from orders; -- correct number of rows (21)

-- select * from orders where month(OrderDate) = 10 and year(OrderDate)=1996;
-- select count(*) from orders where month(OrderDate) = 10 and year(OrderDate) = 1996; -- correct number of rows (26)

-- select * from orders where (
	-- ShipRegion is null and 
	-- ShipCountry = "Germany" and 
	-- Freight >= 100 and 
	-- EmployeeID = 1 and 
	-- year(OrderDate) = 1996
-- ); -- correct number of rows (2)

-- select * from orders where ShippedDate > RequiredDate;
-- select count(*) from orders where ShippedDate > RequiredDate; -- correct number of rows (37)

-- select * from orders where date(OrderDate) between "1997-01-01" and "1997-04-30" and ShipCountry = "Canada"; -- correct number of rows (8)

-- select * from orders where EmployeeID in (2, 5, 8) and ShipRegion is not null and ShipVia in (1, 3) order by EmployeeID, ShipVia;
-- select count(*) from orders where EmployeeID in (2, 5, 8) and ShipRegion is not null and ShipVia in (1, 3); -- correct number of rows (57)

-- select * from Employees where Region is null and year(BirthDate) <= 1960 -- No column named ReportsTo and got 2 row and exercise says 3 but got 2  