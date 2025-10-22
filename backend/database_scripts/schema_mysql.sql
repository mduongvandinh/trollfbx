-- =============================================================================
-- TrollFB Database Schema for MySQL/MariaDB
-- =============================================================================
-- This file contains the complete database schema for the TrollFB application
-- optimized for MySQL 8.0+ or MariaDB 10.5+
--
-- Usage:
--   mysql -u your_user -p trollfb_db < schema_mysql.sql
--
-- Or via Python:
--   python setup_database.py --db mysql
-- =============================================================================

-- Set character set and collation
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS meme_variations;
DROP TABLE IF EXISTS meme_templates;
DROP TABLE IF EXISTS post_analytics;
DROP TABLE IF EXISTS content_posts;
DROP TABLE IF EXISTS content_templates;
DROP TABLE IF EXISTS affiliate_campaigns;
DROP TABLE IF EXISTS app_settings;
DROP TABLE IF EXISTS news_articles;

-- =============================================================================
-- TABLE: news_articles
-- Store news from football sources with Vietnamese localization
-- =============================================================================
CREATE TABLE news_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    url VARCHAR(1000) UNIQUE,
    source VARCHAR(100),
    image_url VARCHAR(1000),
    published_at DATETIME,
    category VARCHAR(50),  -- transfer, match_result, drama, injury, etc.
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Vietnamese localization fields
    content_category VARCHAR(50),  -- vietnamese | international | mixed | general
    vn_angle TEXT,  -- Vietnamese perspective/commentary
    hashtags JSON,  -- Array of hashtags

    INDEX idx_news_category (category),
    INDEX idx_news_published (published_at DESC),
    INDEX idx_news_is_used (is_used)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: content_posts
-- Generated content posts for social media
-- =============================================================================
CREATE TABLE content_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    caption TEXT NOT NULL,
    content_type VARCHAR(50),  -- meme, news, interactive, highlight
    image_path VARCHAR(1000),
    news_id INT,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, scheduled, posted, failed
    scheduled_time DATETIME,
    posted_time DATETIME,

    -- Social media post IDs
    fb_post_id VARCHAR(200),
    twitter_post_id VARCHAR(200),

    -- Platform-specific captions
    fb_caption TEXT,
    twitter_caption TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_posts_status (status),
    INDEX idx_posts_scheduled (scheduled_time),
    INDEX idx_posts_content_type (content_type),
    FOREIGN KEY (news_id) REFERENCES news_articles(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: post_analytics
-- Analytics metrics for posted content
-- =============================================================================
CREATE TABLE post_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    platform VARCHAR(20),  -- facebook | twitter

    -- Facebook metrics
    fb_post_id VARCHAR(200),
    reach INT DEFAULT 0,
    impressions INT DEFAULT 0,

    -- Common metrics
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,  -- shares (FB) or retweets (Twitter)

    -- Twitter-specific metrics
    twitter_post_id VARCHAR(200),
    retweets INT DEFAULT 0,
    quotes INT DEFAULT 0,
    replies INT DEFAULT 0,

    engagement_rate DECIMAL(5,2) DEFAULT 0.0,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_analytics_post (post_id),
    INDEX idx_analytics_platform (platform),
    FOREIGN KEY (post_id) REFERENCES content_posts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: content_templates
-- Meme templates and styles
-- =============================================================================
CREATE TABLE content_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    template_type VARCHAR(50),  -- meme, quote, stat, comparison
    image_path VARCHAR(1000),
    text_positions JSON,  -- JSON with text positioning
    style_config JSON,  -- JSON with font, color, etc.
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_templates_type (template_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: affiliate_campaigns
-- Affiliate marketing campaigns tracking
-- =============================================================================
CREATE TABLE affiliate_campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    product_type VARCHAR(50),  -- jersey, app, betting, merchandise
    affiliate_link VARCHAR(1000) NOT NULL,
    commission_rate DECIMAL(5,2),
    clicks INT DEFAULT 0,
    conversions INT DEFAULT 0,
    revenue DECIMAL(10,2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_campaigns_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: app_settings
-- Application settings key-value store
-- =============================================================================
CREATE TABLE app_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(100) UNIQUE NOT NULL,  -- `key` is reserved word in MySQL
    value TEXT,
    description VARCHAR(500),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_settings_key (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: meme_templates
-- Store crawled/uploaded memes with AI analysis
-- =============================================================================
CREATE TABLE meme_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Basic info
    title VARCHAR(200),
    source_url VARCHAR(500),  -- Original URL if crawled
    source_type VARCHAR(50) DEFAULT 'manual',  -- manual, reddit, twitter, etc.

    -- Image storage
    image_path VARCHAR(500) NOT NULL,  -- Local path
    image_url VARCHAR(500),  -- Public URL
    thumbnail_path VARCHAR(500),

    -- AI Analysis results
    analysis JSON,  -- Full AI analysis
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
    tags JSON,  -- ["elanga", "adidas", "nottingham", "irony"]

    -- Engagement metrics (if crawled from social media)
    likes_count INT DEFAULT 0,
    shares_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    viral_score DECIMAL(8,2) DEFAULT 0.0,  -- Calculated engagement score

    -- Usage tracking
    times_used INT DEFAULT 0,  -- How many times used as template
    times_generated INT DEFAULT 0,  -- How many variations generated

    -- Status
    status VARCHAR(20) DEFAULT 'pending',  -- pending, analyzed, approved, rejected
    is_public TINYINT(1) DEFAULT 1,  -- Can be used by others

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    analyzed_at DATETIME NULL DEFAULT NULL,

    INDEX idx_meme_templates_category (category),
    INDEX idx_meme_templates_status (status),
    INDEX idx_meme_templates_viral_score (viral_score DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- TABLE: meme_variations
-- Generated variations from templates
-- =============================================================================
CREATE TABLE meme_variations (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Template reference
    template_id INT,

    -- Generated content
    caption TEXT NOT NULL,
    image_path VARCHAR(500),

    -- Context
    player_name VARCHAR(100),
    team_name VARCHAR(100),
    context JSON,  -- Additional context data

    -- Generation info
    generation_method VARCHAR(50) DEFAULT 'ai',  -- ai, manual, hybrid
    model_used VARCHAR(100),  -- ollama:qwen2.5, gpt-4, etc.

    -- Quality metrics
    quality_score DECIMAL(5,2) DEFAULT 0.0,
    is_approved TINYINT(1) DEFAULT 0,

    -- Usage
    status VARCHAR(20) DEFAULT 'draft',  -- draft, published, archived
    published_at DATETIME NULL DEFAULT NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_meme_variations_template (template_id),
    INDEX idx_meme_variations_status (status),
    INDEX idx_meme_variations_quality (quality_score DESC),
    FOREIGN KEY (template_id) REFERENCES meme_templates(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- Default data (optional)
-- =============================================================================

-- Insert default app settings
INSERT INTO app_settings (`key`, value, description) VALUES
    ('app_name', 'TrollFB', 'Application name'),
    ('posting_enabled', 'true', 'Enable automatic posting'),
    ('ai_model', 'qwen2.5:7b-instruct-q4_K_M', 'Default AI model for content generation'),
    ('default_hashtags', '["bongda", "football", "meme"]', 'Default hashtags for posts');

-- =============================================================================
-- GRANTS (adjust as needed for your user)
-- =============================================================================
-- GRANT ALL PRIVILEGES ON trollfb_db.* TO 'your_app_user'@'localhost';
-- FLUSH PRIVILEGES;

-- =============================================================================
-- Schema creation complete!
-- =============================================================================
