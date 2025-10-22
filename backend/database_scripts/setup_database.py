"""
Database Setup and Migration Tool for TrollFB
Supports SQLite, PostgreSQL, and MySQL

Usage:
    # Create PostgreSQL database
    python setup_database.py --db postgresql --host localhost --user myuser --password mypass --database trollfb_db

    # Create MySQL database
    python setup_database.py --db mysql --host localhost --user root --password mypass --database trollfb_db

    # Migrate data from SQLite to PostgreSQL
    python setup_database.py --migrate --from sqlite --to postgresql --host localhost --user myuser --password mypass --database trollfb_db
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to Python path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

def setup_postgresql(host, user, password, database, port=5432):
    """Setup PostgreSQL database"""
    import psycopg2
    from psycopg2 import sql

    print(f"Setting up PostgreSQL database: {database}")

    # Connect to PostgreSQL server (default database)
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database='postgres'  # Connect to default database first
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Create database if not exists
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
        print(f"✅ Database '{database}' created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print(f"⚠️  Database '{database}' already exists")

    cur.close()
    conn.close()

    # Connect to the new database and run schema
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    cur = conn.cursor()

    # Read and execute schema
    schema_file = Path(__file__).parent / "schema_postgresql.sql"
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    cur.execute(schema_sql)
    conn.commit()

    print("✅ PostgreSQL schema created successfully")

    cur.close()
    conn.close()

    # Generate connection string
    conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    print(f"\n📝 Add this to your .env file:")
    print(f"DATABASE_URL={conn_string}")

    return conn_string


def setup_mysql(host, user, password, database, port=3306):
    """Setup MySQL database"""
    import mysql.connector

    print(f"Setting up MySQL database: {database}")

    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )
    cur = conn.cursor()

    # Create database if not exists
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"✅ Database '{database}' created successfully")

    cur.close()
    conn.close()

    # Connect to the new database and run schema
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    cur = conn.cursor()

    # Read and execute schema
    schema_file = Path(__file__).parent / "schema_mysql.sql"
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Execute multi-statement SQL
    for statement in schema_sql.split(';'):
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cur.execute(statement)
            except mysql.connector.Error as e:
                # Skip comments and empty statements
                if 'syntax error' not in str(e).lower():
                    print(f"Warning: {e}")

    conn.commit()

    print("✅ MySQL schema created successfully")

    cur.close()
    conn.close()

    # Generate connection string
    conn_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    print(f"\n📝 Add this to your .env file:")
    print(f"DATABASE_URL={conn_string}")

    return conn_string


def migrate_data(from_db, to_db, to_host, to_user, to_password, to_database, to_port=None):
    """Migrate data from one database to another"""
    from sqlalchemy import create_engine, MetaData, Table
    from sqlalchemy.orm import sessionmaker

    print(f"Migrating data from {from_db} to {to_db}...")

    # Source database (SQLite)
    if from_db == 'sqlite':
        source_url = 'sqlite:///./football_meme.db'
    else:
        raise ValueError(f"Migration from {from_db} not supported yet")

    # Target database
    if to_db == 'postgresql':
        if to_port is None:
            to_port = 5432
        target_url = f"postgresql://{to_user}:{to_password}@{to_host}:{to_port}/{to_database}"
    elif to_db == 'mysql':
        if to_port is None:
            to_port = 3306
        target_url = f"mysql+mysqlconnector://{to_user}:{to_password}@{to_host}:{to_port}/{to_database}"
    else:
        raise ValueError(f"Migration to {to_db} not supported")

    # Create engines
    source_engine = create_engine(source_url)
    target_engine = create_engine(target_url)

    # Reflect source schema
    source_metadata = MetaData()
    source_metadata.reflect(bind=source_engine)

    SourceSession = sessionmaker(bind=source_engine)
    TargetSession = sessionmaker(bind=target_engine)

    source_session = SourceSession()
    target_session = TargetSession()

    # Tables to migrate (in order to respect foreign keys)
    tables_order = [
        'news_articles',
        'content_posts',
        'post_analytics',
        'content_templates',
        'affiliate_campaigns',
        'app_settings',
        'meme_templates',
        'meme_variations'
    ]

    total_rows = 0

    for table_name in tables_order:
        if table_name not in source_metadata.tables:
            print(f"⚠️  Table '{table_name}' not found in source database, skipping")
            continue

        source_table = Table(table_name, source_metadata, autoload_with=source_engine)

        # Fetch all rows from source
        rows = source_session.execute(source_table.select()).fetchall()

        if not rows:
            print(f"  ℹ️  Table '{table_name}': 0 rows (empty)")
            continue

        # Insert into target
        for row in rows:
            row_dict = dict(row._mapping)
            target_session.execute(
                Table(table_name, MetaData(), autoload_with=target_engine).insert(),
                row_dict
            )

        target_session.commit()
        total_rows += len(rows)
        print(f"  ✅ Table '{table_name}': {len(rows)} rows migrated")

    source_session.close()
    target_session.close()

    print(f"\n✅ Migration complete! Total rows migrated: {total_rows}")
    print(f"\n📝 Update your .env file:")
    print(f"DATABASE_URL={target_url}")


def main():
    parser = argparse.ArgumentParser(description='TrollFB Database Setup and Migration Tool')

    parser.add_argument('--db', choices=['postgresql', 'mysql', 'sqlite'],
                        help='Database type to setup')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', type=int, help='Database port (default: 5432 for PostgreSQL, 3306 for MySQL)')
    parser.add_argument('--user', help='Database user')
    parser.add_argument('--password', help='Database password')
    parser.add_argument('--database', help='Database name')

    parser.add_argument('--migrate', action='store_true', help='Migrate data from one database to another')
    parser.add_argument('--from', dest='from_db', choices=['sqlite', 'postgresql', 'mysql'],
                        help='Source database type for migration')
    parser.add_argument('--to', dest='to_db', choices=['postgresql', 'mysql'],
                        help='Target database type for migration')

    args = parser.parse_args()

    try:
        if args.migrate:
            if not args.from_db or not args.to_db:
                parser.error("--migrate requires --from and --to")
            if not args.host or not args.user or not args.password or not args.database:
                parser.error("--migrate requires --host, --user, --password, and --database")

            migrate_data(
                from_db=args.from_db,
                to_db=args.to_db,
                to_host=args.host,
                to_user=args.user,
                to_password=args.password,
                to_database=args.database,
                to_port=args.port
            )

        elif args.db:
            if not args.host or not args.user or not args.password or not args.database:
                parser.error(f"--db {args.db} requires --host, --user, --password, and --database")

            if args.db == 'postgresql':
                setup_postgresql(
                    host=args.host,
                    user=args.user,
                    password=args.password,
                    database=args.database,
                    port=args.port or 5432
                )
            elif args.db == 'mysql':
                setup_mysql(
                    host=args.host,
                    user=args.user,
                    password=args.password,
                    database=args.database,
                    port=args.port or 3306
                )
            elif args.db == 'sqlite':
                print("SQLite is already configured by default. No setup needed.")

        else:
            parser.print_help()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
