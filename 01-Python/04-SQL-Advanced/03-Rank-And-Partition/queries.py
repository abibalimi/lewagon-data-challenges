# pylint:disable=C0111,C0103

def order_rank_per_customer(db):
    query="""
        SELECT
            OrderID,
            CustomerID,
            OrderDate,
            RANK() OVER (
                PARTITION BY CustomerID
                ORDER BY OrderDate
            ) AS order_rank
        FROM orders
    """
    db.execute(query)
    results = db.fetchall() # results in a list (rows) of tuples (columns)
    #results = [r[0] for r in results]
    return results

def order_cumulative_amount_per_customer(db):
    query="""
        SELECT DISTINCT
        o.OrderID,
        o.CustomerID,
        o.OrderDate,
        SUM(od.UnitPrice * od.Quantity) OVER (
            PARTITION BY o.CustomerID
            ORDER BY o.OrderDate
        ) AS OrderCumulativeAmount
    FROM Orders o 
    LEFT JOIN OrderDetails od ON od.OrderID = o.OrderID
    """
    db.execute(query)
    results = db.fetchall()
    return results
