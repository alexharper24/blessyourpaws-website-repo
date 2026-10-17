-- 2026-10-17. Prices move from scripts/scaffold.py onto the litter, so the owner sets them in
-- the editor (docs/checkout-build.md, prices). json_set appends the keys at the END of the
-- doc, which is where data/litters.json has them. Only litters without a price are touched,
-- so running it twice changes nothing.
UPDATE records
   SET doc = json_set(doc, '$.price', 2060, '$.cash_price', 2000, '$.deposit', 500),
       version = version + 1, updated_at = '2026-10-17T00:00:00Z', updated_by = 'migration'
 WHERE file = 'litters' AND json_extract(doc, '$.price') IS NULL;
INSERT INTO audit (file, key, action, detail, actor, created_at)
VALUES ('litters', NULL, 'migration', '001-litter-prices: price 2060, cash_price 2000, deposit 500', 'migration', '2026-10-17T00:00:00Z');
