-- Add_buy
INSERT INTO compras (Fecha, Monto, Comercio, Tipo, Cantidad_productos) VALUES (%s, %s, %s, %s,%s);

-- Add_expense
INSERT INTO gastos (Fecha, Monto, Concepto) VALUES (%s, %s, %s);

-- Update_IDexpense_in_buy
UPDATE compras SET ID_gasto = %s WHERE ID_compra = %s;

-- Update_productos_from_buy
INSERT INTO producto (Producto, Costo, Cantidad, ID_compra, ID_gasto) VALUES (%s, %s, %s, %s,%s)

-- Update_product_record
INSERT INTO productos (Producto) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM productos WHERE Producto = %s);

-- Update-product_IDs
UPDATE producto p JOIN productos ps ON p.Producto=ps.Producto SET p.ID_producto=ps.ID_producto




