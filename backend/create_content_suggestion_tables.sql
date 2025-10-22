-- Create content_suggestions table
CREATE TABLE IF NOT EXISTS content_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_id INTEGER NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    tone VARCHAR(50),
    hashtags TEXT,  -- JSON stored as text
    suggested_image_keywords TEXT,  -- JSON stored as text
    viral_prediction_score FLOAT DEFAULT 0.0,
    engagement_prediction FLOAT DEFAULT 0.0,
    best_time_to_post DATETIME,
    priority VARCHAR(20) DEFAULT 'normal',
    status VARCHAR(20) DEFAULT 'suggested',
    published_at DATETIME,
    scheduled_for DATETIME,
    is_ab_variant BOOLEAN DEFAULT 0,
    ab_group VARCHAR(10),
    ab_test_id VARCHAR(100),
    actual_views INTEGER DEFAULT 0,
    actual_likes INTEGER DEFAULT 0,
    actual_shares INTEGER DEFAULT 0,
    actual_comments INTEGER DEFAULT 0,
    actual_engagement_rate FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trend_id) REFERENCES trending_topics(id)
);

-- Create indexes for content_suggestions
CREATE INDEX IF NOT EXISTS idx_content_suggestions_trend_id ON content_suggestions(trend_id);
CREATE INDEX IF NOT EXISTS idx_content_suggestions_content_type ON content_suggestions(content_type);
CREATE INDEX IF NOT EXISTS idx_content_suggestions_viral_score ON content_suggestions(viral_prediction_score);
CREATE INDEX IF NOT EXISTS idx_content_suggestions_status ON content_suggestions(status);
CREATE INDEX IF NOT EXISTS idx_content_suggestions_created_at ON content_suggestions(created_at);

-- Create publishing_schedules table
CREATE TABLE IF NOT EXISTS publishing_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_suggestion_id INTEGER NOT NULL,
    scheduled_time DATETIME NOT NULL,
    platform VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    published_at DATETIME,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_suggestion_id) REFERENCES content_suggestions(id)
);

-- Create indexes for publishing_schedules
CREATE INDEX IF NOT EXISTS idx_publishing_schedules_content_id ON publishing_schedules(content_suggestion_id);
CREATE INDEX IF NOT EXISTS idx_publishing_schedules_scheduled_time ON publishing_schedules(scheduled_time);
CREATE INDEX IF NOT EXISTS idx_publishing_schedules_status ON publishing_schedules(status);
