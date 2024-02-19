-- Get all events
SELECT * FROM events
WHERE id=2;

-- Get all the metadata for a specific event as a table
SELECT id as event_id, arr.position, arr.info as info_item FROM events, jsonb_array_elements(info)
WITH ORDINALITY arr(info, position)
WHERE id=2;

-- Get all metadata name fields with a particular value across all events
SELECT arr.position, arr.info FROM events, jsonb_array_elements(info)
WITH ORDINALITY arr(info, position)
WHERE arr.info->>'name' = 'Verdict';
