-- =============================================================================
-- TrollFB Database Schema for PostgreSQL
-- =============================================================================
-- This file contains the complete database schema for the TrollFB application
-- optimized for PostgreSQL.
--
-- Usage:
--   psql -U your_user -d trollfb_db -f schema_postgresql.sql
--
-- Or via Python:
--   python setup_database.py --db postgresql
-- =============================================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS meme_variations CASCADE;
DROP TABLE IF EXISTS meme_templates CASCADE;
DROP TABLE IF EXISTS post_analytics CASCADE;
DROP TABLE IF EXISTS content_posts CASCADE;
DROP TABLE IF EXISTS content_templates CASCADE;
DROP TABLE IF EXISTS affiliate_campaigns CASCADE;
DROP TABLE IF EXISTS app_settings CASCADE;
DROP TABLE IF EXISTS news_articles CASCADE;

-- =============================================================================
-- TABLE: news_articles
-- Store news from football sources with Vietnamese localization
-- =============================================================================
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    url VARCHAR(1000) UNIQUE,
    source VARCHAR(100),
    image_url VARCHAR(1000),
    published_at TIMESTAMP,
    category VARCHAR(50),  -- transfer, match_result, drama, injury, etc.
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Vietnamese localization fields
    content_category VARCHAR(50),  -- vietnamese | international | mixed | general
    vn_angle TEXT,  -- Vietnamese perspective/commentary
    hashtags JSONB  -- Array of hashtags
);

CREATE INDEX idx_news_category ON news_articles(category);
CREATE INDEX idx_news_published ON news_articles(published_at DESC);
CREATE INDEX idx_news_is_used ON news_articles(is_used);

-- =============================================================================
-- TABLE: content_posts
-- Generated content posts for social media
-- =============================================================================
CREATE TABLE content_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    caption TEXT NOT NULL,
    content_type VARCHAR(50),  -- meme, news, interactive, highlight
    image_path VARCHAR(1000),
    news_id INTEGER REFERENCES news_articles(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, scheduled, posted, failed
    scheduled_time TIMESTAMP,
    posted_time TIMESTAMP,

    -- Social media post IDs
    fb_post_id VARCHAR(200),
    twitter_post_id VARCHAR(200),

    -- Platform-specific captions
    fb_caption TEXT,
    twitter_caption TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_status ON content_posts(status);
CREATE INDEX idx_posts_scheduled ON content_posts(scheduled_time);
CREATE INDEX idx_posts_content_type ON content_posts(content_type);

-- =============================================================================
-- TABLE: post_analytics
-- Analytics metrics for posted content
-- =============================================================================
CREATE TABLE post_analytics (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES content_posts(id) ON DELETE CASCADE,
    platform VARCHAR(20),  -- facebook | twitter

    -- Facebook metrics
    fb_post_id VARCHAR(200),
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,

    -- Common metrics
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,  -- shares (FB) or retweets (Twitter)

    -- Twitter-specific metrics
    twitter_post_id VARCHAR(200),
    retweets INTEGER DEFAULT 0,
    quotes INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,

    engagement_rate DECIMAL(5,2) DEFAULT 0.0,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analytics_post ON post_analytics(post_id);
CREATE INDEX idx_analytics_platform ON post_analytics(platform);

-- =============================================================================
-- TABLE: content_templates
-- Meme templates and styles
-- =============================================================================
CREATE TABLE content_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    template_type VARCHAR(50),  -- meme, quote, stat, comparison
    image_path VARCHAR(1000),
    text_positions JSONB,  -- JSON with text positioning
    style_config JSONB,  -- JSON with font, color, etc.
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_templates_type ON content_templates(template_type);

-- =============================================================================
-- TABLE: affiliate_campaigns
-- Affiliate marketing campaigns tracking
-- =============================================================================
CREATE TABLE affiliate_campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    product_type VARCHAR(50),  -- jersey, app, betting, merchandise
    affiliate_link VARCHAR(1000) NOT NULL,
    commission_rate DECIMAL(5,2),
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue DECIMAL(10,2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_campaigns_active ON affiliate_campaigns(is_active);

-- =============================================================================
-- TABLE: app_settings
-- Application settings key-value store
-- =============================================================================
CREATE TABLE app_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    description VARCHAR(500),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_settings_key ON app_settings(key);

-- =============================================================================
-- TABLE: meme_templates
-- Store crawled/uploaded memes with AI analysis
-- =============================================================================
CREATE TABLE meme_templates (
    id SERIAL PRIMARY KEY,

    -- Basic info
    title VARCHAR(200),
    source_url VARCHAR(500),  -- Original URL if crawled
    source_type VARCHAR(50) DEFAULT 'manual',  -- manual, reddit, twitter, etc.

    -- Image storage
    image_path VARCHAR(500) NOT NULL,  -- Local path
    image_url VARCHAR(500),  -- Public URL
    thumbnail_path VARCHAR(500),

    -- AI Analysis results
    analysis JSONB,  -- Full AI analysis
    /*
    analysis structure:
    {
        "caption": "Original caption/text from meme",
        "template_type": "childhood_dream_irony",
        "key_elements": ["player_pointing", "sponsor_logo", "ironic_caption"],
        "humor_type": "irony",
        "football_context": {
            "player": "Elanga",
            "team": "Nottingham Forest",
            "sponsor": "Adidas"
        },
        "description": "AI description of the meme",
        "reusable_format": "Player: '[quote]' + image showing opposite reality"
    }
    */

    -- Categorization
    category VARCHAR(100),  -- childhood_dream, sponsor_troll, etc.
    tags JSONB DEFAULT '[]'::jsonb,  -- ["elanga", "adidas", "nottingham", "irony"]

    -- Engagement metrics (if crawled from social media)
    likes_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    viral_score DECIMAL(8,2) DEFAULT 0.0,  -- Calculated engagement score

    -- Usage tracking
    times_used INTEGER DEFAULT 0,  -- How many times used as template
    times_generated INTEGER DEFAULT 0,  -- How many variations generated

    -- Status
    status VARCHAR(20) DEFAULT 'pending',  -- pending, analyzed, approved, rejected
    is_public SMALLINT DEFAULT 1,  -- Can be used by others

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    analyzed_at TIMESTAMP
);

CREATE INDEX idx_meme_templates_category ON meme_templates(category);
CREATE INDEX idx_meme_templates_status ON meme_templates(status);
CREATE INDEX idx_meme_templates_viral_score ON meme_templates(viral_score DESC);

-- =============================================================================
-- TABLE: meme_variations
-- Generated variations from templates
-- =============================================================================
CREATE TABLE meme_variations (
    id SERIAL PRIMARY KEY,

    -- Template reference
    template_id INTEGER REFERENCES meme_templates(id) ON DELETE SET NULL,

    -- Generated content
    caption TEXT NOT NULL,
    image_path VARCHAR(500),

    -- Context
    player_name VARCHAR(100),
    team_name VARCHAR(100),
    context JSONB,  -- Additional context data

    -- Generation info
    generation_method VARCHAR(50) DEFAULT 'ai',  -- ai, manual, hybrid
    model_used VARCHAR(100),  -- ollama:qwen2.5, gpt-4, etc.

    -- Quality metrics
    quality_score DECIMAL(5,2) DEFAULT 0.0,
    is_approved SMALLINT DEFAULT 0,

    -- Usage
    status VARCHAR(20) DEFAULT 'draft',  -- draft, published, archived
    published_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_meme_variations_template ON meme_variations(template_id);
CREATE INDEX idx_meme_variations_status ON meme_variations(status);
CREATE INDEX idx_meme_variations_quality ON meme_variations(quality_score DESC);

-- =============================================================================
-- TRIGGERS for updated_at timestamps
-- =============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to content_posts
CREATE TRIGGER update_content_posts_updated_at BEFORE UPDATE
    ON content_posts FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to app_settings
CREATE TRIGGER update_app_settings_updated_at BEFORE UPDATE
    ON app_settings FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to meme_templates
CREATE TRIGGER update_meme_templates_updated_at BEFORE UPDATE
    ON meme_templates FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to meme_variations
CREATE TRIGGER update_meme_variations_updated_at BEFORE UPDATE
    ON meme_variations FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Default data (optional)
-- =============================================================================

-- Insert default app settings
INSERT INTO app_settings (key, value, description) VALUES
    ('app_name', 'TrollFB', 'Application name'),
    ('posting_enabled', 'true', 'Enable automatic posting'),
    ('ai_model', 'qwen2.5:7b-instruct-q4_K_M', 'Default AI model for content generation'),
    ('default_hashtags', '["bongda", "football", "meme"]', 'Default hashtags for posts');

-- =============================================================================
-- GRANTS (adjust as needed for your user)
-- =============================================================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

-- =============================================================================
-- Schema creation complete!
-- =============================================================================
