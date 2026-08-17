WITH monthly_unpaid AS (
    SELECT 
        DATE_TRUNC('month', z.Дата) AS месяц,
        c.ID AS клиент_id,
        z.ID AS заявка_id,
        z.Сумма AS сумма_заявки,
        COALESCE(SUM(p.Сумма), 0) AS сумма_оплаты,
        z.Сумма - COALESCE(SUM(p.Сумма), 0) AS сумма_долга
    FROM Клиент c
    JOIN Договор d ON c.ID = d.ID_клиента
    JOIN Заявка z ON c.ID = z.ID_клиента
    JOIN Счет s ON z.ID = s.ID_заявки
    LEFT JOIN Платеж p ON s.ID = p.ID_счета
    WHERE d.Тип_оплаты = 'предоплата'
      AND DATE_TRUNC('month', z.Дата) IN (
          DATE_TRUNC('month', CURRENT_DATE),                         
          DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')      
      )
      AND s.Срок_оплаты_до < CURRENT_DATE   
    GROUP BY c.ID, z.ID, z.Сумма, DATE_TRUNC('month', z.Дата)
    HAVING z.Сумма - COALESCE(SUM(p.Сумма), 0) > 0   
)
SELECT 
    MAX(CASE WHEN месяц = DATE_TRUNC('month', CURRENT_DATE) 
        THEN COUNT(DISTINCT клиент_id) END) AS текущий_месяц_клиенты,
    MAX(CASE WHEN месяц = DATE_TRUNC('month', CURRENT_DATE) 
        THEN SUM(сумма_долга) END) AS текущий_месяц_сумма,
    MAX(CASE WHEN месяц = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') 
        THEN COUNT(DISTINCT клиент_id) END) AS прошлый_месяц_клиенты,
    MAX(CASE WHEN месяц = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') 
        THEN SUM(сумма_долга) END) AS прошлый_месяц_сумма
FROM monthly_unpaid
GROUP BY месяц;