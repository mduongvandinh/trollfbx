# TrollFB Database Migration Scripts

This directory contains SQL schema files and Python utilities to help you switch between different database systems (SQLite, PostgreSQL, MySQL).

## 📁 Files

```
database_scripts/
├── README.md                    # This file
├── schema_postgresql.sql        # PostgreSQL schema with indexes and triggers
├── schema_mysql.sql             # MySQL schema optimized for MySQL 8.0+
└── setup_database.py            # Python utility for database setup and migration
```

## 🎯 Quick Start

### Option 1: Use Currently (SQLite - Default)

No action needed! The application uses SQLite by default with the database file at `backend/football_meme.db`.

### Option 2: Switch to PostgreSQL

**Step 1: Install PostgreSQL**
```bash
# Windows: Download from https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql
```

**Step 2: Install Python PostgreSQL driver**
```bash
cd backend
pip install psycopg2-binary
```

**Step 3: Create database and run schema**
```bash
cd backend/database_scripts
python setup_database.py --db postgresql \
  --host localhost \
  --user your_username \
  --password your_password \
  --database trollfb_db
```

**Step 4: Update .env file**
```bash
# Add to backend/.env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/trollfb_db
```

**Step 5: Restart backend**
```bash
cd backend
python main.py
```

### Option 3: Switch to MySQL

**Step 1: Install MySQL**
```bash
# Windows: Download from https://dev.mysql.com/downloads/installer/
# Mac: brew install mysql
# Linux: sudo apt-get install mysql-server
```

**Step 2: Install Python MySQL driver**
```bash
cd backend
pip install mysql-connector-python
```

**Step 3: Create database and run schema**
```bash
cd backend/database_scripts
python setup_database.py --db mysql \
  --host localhost \
  --user root \
  --password your_password \
  --database trollfb_db
```

**Step 4: Update .env file**
```bash
# Add to backend/.env
DATABASE_URL=mysql+mysqlconnector://root:your_password@localhost:3306/trollfb_db
```

**Step 5: Restart backend**
```bash
cd backend
python main.py
```

## 🔄 Migrate Data from SQLite to PostgreSQL/MySQL

If you already have data in SQLite and want to move to PostgreSQL or MySQL:

### Migrate to PostgreSQL

```bash
cd backend/database_scripts
python setup_database.py --migrate \
  --from sqlite \
  --to postgresql \
  --host localhost \
  --user your_username \
  --password your_password \
  --database trollfb_db
```

### Migrate to MySQL

```bash
cd backend/database_scripts
python setup_database.py --migrate \
  --from sqlite \
  --to mysql \
  --host localhost \
  --user root \
  --password your_password \
  --database trollfb_db
```

## 📊 Database Schema

All three databases have the same schema with **8 tables**:

### Core Tables

1. **news_articles** - Football news from various sources
   - Vietnamese localization fields
   - Categorization (transfer, match_result, drama, etc.)
   - Hashtags stored as JSON

2. **content_posts** - Generated meme/content posts
   - Multi-platform support (Facebook, Twitter)
   - Status tracking (draft, scheduled, posted)
   - Platform-specific captions

3. **post_analytics** - Engagement metrics
   - Facebook: reach, impressions, likes, comments, shares
   - Twitter: retweets, quotes, replies
   - Engagement rate calculation

4. **content_templates** - Meme templates library
   - Text positioning (JSON)
   - Style configuration (JSON)
   - Usage tracking

5. **affiliate_campaigns** - Monetization tracking
   - Product types (jersey, app, betting)
   - Clicks, conversions, revenue tracking
   - Commission rate management

6. **app_settings** - Key-value configuration store
   - Application settings
   - Feature flags
   - Default values

### Meme Library Tables

7. **meme_templates** - AI-analyzed meme templates
   - Image storage paths
   - AI analysis results (JSON)
   - Categorization and tagging
   - Viral score tracking
   - Usage statistics

8. **meme_variations** - Generated meme variations
   - Template references
   - Player/team context
   - Generation method tracking
   - Quality scoring

## 🔧 Manual SQL Execution

### PostgreSQL

```bash
# Create database
psql -U your_username -c "CREATE DATABASE trollfb_db;"

# Run schema
psql -U your_username -d trollfb_db -f schema_postgresql.sql
```

### MySQL

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE trollfb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run schema
mysql -u root -p trollfb_db < schema_mysql.sql
```

## 🎨 Database Features by Type

### SQLite (Default)
✅ No installation needed
✅ Single file database
✅ Great for development
❌ Limited concurrency
❌ No advanced features

### PostgreSQL (Recommended for Production)
✅ Advanced SQL features
✅ JSON/JSONB support (faster queries)
✅ Excellent concurrency
✅ Triggers and stored procedures
✅ Full-text search
✅ Highly scalable

### MySQL (Popular Choice)
✅ Widely supported
✅ Good performance
✅ JSON support
✅ Replication support
✅ Large community

## 📝 Environment Variables

Update your `backend/.env` file with the appropriate DATABASE_URL:

```bash
# SQLite (default)
DATABASE_URL=sqlite:///./football_meme.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/trollfb_db

# MySQL
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/trollfb_db
```

## 🧪 Testing the Connection

After setting up, test the database connection:

```python
# backend/test_db_connection.py
from app.core.database import engine, init_db
from sqlalchemy import text

try:
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")

    # Initialize tables
    init_db()
    print("✅ All tables created successfully!")

except Exception as e:
    print(f"❌ Database error: {e}")
```

Run the test:
```bash
cd backend
python test_db_connection.py
```

## ⚠️ Important Notes

1. **Backup your data** before migrating between databases
2. **Update database.py** if you need custom connection args for PostgreSQL/MySQL
3. **Install required drivers**:
   - PostgreSQL: `pip install psycopg2-binary`
   - MySQL: `pip install mysql-connector-python`
4. **JSON column differences**:
   - PostgreSQL uses `JSONB` (binary, faster)
   - MySQL uses `JSON` (text-based)
   - SQLite stores as TEXT

## 🆘 Troubleshooting

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "No module named 'mysql'"
```bash
pip install mysql-connector-python
```

### Error: "Database does not exist"
Run the setup script first to create the database.

### Error: "Connection refused"
Make sure PostgreSQL/MySQL server is running:
```bash
# PostgreSQL
sudo service postgresql status

# MySQL
sudo service mysql status
```

### Migration errors
- Ensure source database (SQLite) exists
- Ensure target database is created and empty
- Check connection credentials

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 🔄 Switching Back to SQLite

Simply update your `.env`:
```bash
DATABASE_URL=sqlite:///./football_meme.db
```

And restart the backend. Your SQLite database file is preserved.

---

**Need help?** Check the main README or create an issue on GitHub.
