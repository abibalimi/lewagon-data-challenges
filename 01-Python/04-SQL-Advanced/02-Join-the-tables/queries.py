# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query="""
        SELECT o.OrderID, c.ContactName, e.Firstname
        FROM Customers c,  Employees e
        JOIN Orders o
        ON o.CustomerID = c.CustomerID AND o.EmployeeID = e.EmployeeID
        ORDER BY o.OrderID
    """
    db.execute(query)
    results = db.fetchall()
    return results

def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query="""
        SELECT c.ContactName,
	    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS total_amount
        FROM OrderDetails od 
        JOIN Orders o ON o.OrderID = od.OrderID 
        JOIN Customers c ON o.CustomerID = c.CustomerID
        GROUP BY c.ContactName 
        ORDER BY total_amount ASC
    """
    db.execute(query)
    results = db.fetchall()
    return results

def best_employee(db):
    '''return the first and last name of the best employee (the one
    who sells the most in terms of amount of money'''
    query="""
        SELECT e.FirstName, e.LastName,
	    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS total_amount
        FROM OrderDetails od, Orders o   
        JOIN Employees e ON e.EmployeeID = o.EmployeeID AND o.OrderID = od.OrderID
        GROUP BY e.FirstName 
        ORDER BY total_amount DESC
    """
    db.execute(query)
    results = db.fetchall()
    #results = [r[0] for r in results]
    return [results[0]]

def orders_per_customer(db):
    '''TO DO: return a list of tuples where each tupe contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    pass
