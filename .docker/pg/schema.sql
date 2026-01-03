CREATE OR REPLACE VIEW public.core_transaction_analytics AS
SELECT t.id AS transaction_id,
       t.created AS created_date,
       t.type AS transaction_type,
       t.amount,
       t.amount_converted,
       t.currency_from,
       t.currency_to,
       t.is_recurrence,
       t.note,
       a.id AS account_id,
       a.name AS account_name,
       c.id AS category_id,
       c.name AS category_name,
       COALESCE(string_agg((tag.name)::text, ', '::text ORDER BY (tag.name)::text), ''::text) AS tags
FROM ((((public.core_transaction t
    JOIN public.core_account a ON ((a.id = t.account_id)))
    JOIN public.core_category c ON ((c.id = t.category_id)))
    LEFT JOIN public.core_transaction_tags tt ON ((tt.transaction_id = t.id)))
    LEFT JOIN public.core_tag tag ON ((tag.id = tt.tag_id)))
GROUP BY t.id, t.created, t.type, t.amount, t.currency_from, t.amount_converted, t.currency_to, t.is_recurrence, t.note, a.id, a.name, c.id, c.name;
