-- Total_income_bd
SELECT SUM(Monto) FROM ingresos WHERE Fecha BETWEEN %s AND %s;

-- Total_expense_bd
SELECT -SUM(Monto) FROM gastos WHERE Fecha BETWEEN %s AND %s;

-- Total_balance_bd
SELECT Sum(totales) as total FROM (
SELECT SUM(Monto) as totales FROM ingresos WHERE Fecha BETWEEN %s AND %s
UNION ALL
SELECT -SUM(Monto) as totales FROM gastos WHERE Fecha BETWEEN %s AND %s
)total_table;

-- Type_expense_bd
SELECT DISTINCT Concepto FROM gastos WHERE Fecha  BETWEEN %s AND %s;

-- Amount_type_expense_bd
SELECT Concepto, count(*) as frequency FROM gastos WHERE Fecha  BETWEEN %s AND %s GROUP BY Concepto;

-- Amount_type_income_bd
SELECT Concepto, count(*) as frequency FROM ingresos WHERE Fecha  BETWEEN %s AND %s GROUP BY Concepto;