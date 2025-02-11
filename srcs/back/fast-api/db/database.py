import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from contextlib import contextmanager


# 環境変数の読み込み
load_dotenv()

# DB接続に必要な情報を環境変数から取得
DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = int(os.getenv("POSTGRES_PORT", "5432"))


def get_db():
    with get_db_connection() as conn:  # コンテキストマネージャーを使用
        yield conn


@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        cursor_factory=RealDictCursor, # queryの結果をdictの形式で返す設定
    ) # 接続確率
    try:
        yield conn # 接続を返す
        conn.commit() # 正常終了時のコミット
    except Exception:
        conn.rollback() # 例外時のロールバック
        raise
    finally:
        conn.close() # 確実なclose
