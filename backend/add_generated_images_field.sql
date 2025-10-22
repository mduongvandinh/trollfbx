-- Add generated_images field to content_suggestions table
-- This stores the ComfyUI generated images for each content suggestion
-- Run this migration: sqlite3 football_meme.db < add_generated_images_field.sql

-- Check if column already exists (SQLite doesn't have IF NOT EXISTS for ALTER TABLE)
-- If this fails with "duplicate column name", the column already exists and you can ignore the error

ALTER TABLE content_suggestions
ADD COLUMN generated_images TEXT;

-- SQLite stores JSON as TEXT, so this is correct
-- The field will contain: [{"variant_id": 0, "filename": "...", "url": "...", "style": "Claymation"}, ...]

SELECT 'Migration completed: added generated_images column to content_suggestions table' as result;
