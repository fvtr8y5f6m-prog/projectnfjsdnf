from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# 유저 테이블
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    categories = relationship("Category", back_populates="owner")
    sessions = relationship("PracticeSession", back_populates="user")

# 카테고리 테이블
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String) # 면접인지 발표인지
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="categories")
    sessions = relationship("PracticeSession", back_populates="category")

# 연습 세션 테이블
class PracticeSession(Base):
    __tablename__ = "practice_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    start_time = Column(DateTime, default=datetime.now)
    analysis_result = relationship("AnalysisResult", uselist=False, back_populates="session")

# 분석 결과 테이블
class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"))
    average_wpm = Column(Float, default=0.0)
    filler_count = Column(Integer, default=0)
    score = Column(Integer, default=0)
    session = relationship("PracticeSession", back_populates="analysis_result")