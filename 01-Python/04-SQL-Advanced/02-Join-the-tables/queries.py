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
    pass

def best_employee(db):
    '''return the first and last name of the best employee (the one
    who sells the most in terms of amount of money'''
    pass

def orders_per_customer(db):
    '''TO DO: return a list of tuples where each tupe contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    pass
