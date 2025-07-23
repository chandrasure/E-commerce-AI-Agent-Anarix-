import pandas as pd
import sqlite3
import os

def ingest_data():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    db_dir = os.path.join(os.path.dirname(__file__), '..', 'db')
    db_path = os.path.join(db_dir, 'ecommerce.db')

    # Load CSVs
    ad_sales = pd.read_csv(os.path.join(data_dir, 'ad_sales.csv'))
    total_sales = pd.read_csv(os.path.join(data_dir, 'total_sales.csv'))
    eligibility = pd.read_csv(os.path.join(data_dir, 'eligibility.csv'))

    # Clean data
    for df in [ad_sales, total_sales, eligibility]:
        if 'item_id' in df.columns:
            df['item_id'] = df['item_id'].astype(str).str.strip()
        df.dropna(how='all', inplace=True)

    # Standardize types
    ad_sales = ad_sales.astype({
        'date': 'str',
        'item_id': 'int',
        'ad_sales': 'float',
        'impressions': 'int',
        'ad_spend': 'float',
        'clicks': 'int',
        'units_sold': 'int',
    })
    total_sales = total_sales.astype({
        'date': 'str',
        'item_id': 'int',
        'total_sales': 'float',
        'total_units_ordered': 'int',
    })
    # eligibility: flexible types

    # Create DB and tables
    os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    ad_sales.to_sql('ad_sales_metrics', conn, if_exists='replace', index=False)
    total_sales.to_sql('total_sales_metrics', conn, if_exists='replace', index=False)
    eligibility.to_sql('eligibility_table', conn, if_exists='replace', index=False)

    # Create indexes
    cur = conn.cursor()
    cur.execute('CREATE INDEX IF NOT EXISTS idx_ad_sales_item_date ON ad_sales_metrics(item_id, date)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_total_sales_item_date ON total_sales_metrics(item_id, date)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_eligibility_item_date ON eligibility_table(item_id, eligibility_datetime_utc)')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    ingest_data()
    print('Data ingested and database created.') 