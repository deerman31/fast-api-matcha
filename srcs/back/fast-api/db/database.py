from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# データベースURLの取得
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# エンジンの作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()


# DBセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
