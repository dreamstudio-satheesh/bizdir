from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, JSON, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # ✅ Required
    description = Column(Text, nullable=False)  # ✅ Ensuring description is mandatory
    registration_number = Column(String(100), unique=True, nullable=True)  # Optional
    website = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    established_year = Column(Integer, nullable=True)
    revenue = Column(DECIMAL(15, 2), nullable=True)
    company_size = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)  # ✅ Auto-generated timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # ✅ Auto-updated timestamp

    meta = relationship("BusinessMeta", back_populates="business", cascade="all, delete")
    tags = relationship("BusinessTag", back_populates="business", cascade="all, delete")
    owners = relationship("BusinessOwner", back_populates="business", cascade="all, delete")
    locations = relationship("BusinessLocation", back_populates="business", cascade="all, delete")
    embeddings = relationship("BusinessEmbedding", back_populates="business", cascade="all, delete")


class BusinessMeta(Base):
    __tablename__ = "business_meta"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    meta_key = Column(String(255), nullable=False)  # ✅ Required
    meta_value = Column(Text, nullable=False)  # ✅ Required

    business = relationship("Business", back_populates="meta")


class BusinessTag(Base):
    __tablename__ = "business_tags"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    tag = Column(String(255), nullable=False)  # ✅ Required

    business = relationship("Business", back_populates="tags")


class BusinessOwner(Base):
    __tablename__ = "business_owners"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    owner_name = Column(String(255), nullable=False)  # ✅ Required
    contact_number = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)

    business = relationship("Business", back_populates="owners")


class BusinessLocation(Base):
    __tablename__ = "business_locations"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    address = Column(Text, nullable=False)  # ✅ Required
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    latitude = Column(DECIMAL(10, 8), nullable=True)
    longitude = Column(DECIMAL(11, 8), nullable=True)

    business = relationship("Business", back_populates="locations")


class BusinessEmbedding(Base):
    __tablename__ = "business_embeddings"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    embedding_vector = Column(JSON, nullable=False)  # ✅ Required

    business = relationship("Business", back_populates="embeddings")
