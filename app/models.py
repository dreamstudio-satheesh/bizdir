from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, JSON, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    registration_number = Column(String(100), unique=True)
    website = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    established_year = Column(Integer)
    revenue = Column(DECIMAL(15, 2))
    company_size = Column(String(50))
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    meta = relationship("BusinessMeta", back_populates="business")
    tags = relationship("BusinessTag", back_populates="business")
    owners = relationship("BusinessOwner", back_populates="business")
    locations = relationship("BusinessLocation", back_populates="business")
    embeddings = relationship("BusinessEmbedding", back_populates="business")


class BusinessMeta(Base):
    __tablename__ = "business_meta"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"))
    meta_key = Column(String(255), nullable=False)
    meta_value = Column(Text, nullable=False)

    business = relationship("Business", back_populates="meta")


class BusinessTag(Base):
    __tablename__ = "business_tags"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"))
    tag = Column(String(255), nullable=False)

    business = relationship("Business", back_populates="tags")


class BusinessOwner(Base):
    __tablename__ = "business_owners"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"))
    owner_name = Column(String(255), nullable=False)
    contact_number = Column(String(50))
    email = Column(String(255))

    business = relationship("Business", back_populates="owners")


class BusinessLocation(Base):
    __tablename__ = "business_locations"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"))
    address = Column(Text, nullable=False)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))

    business = relationship("Business", back_populates="locations")


class BusinessEmbedding(Base):
    __tablename__ = "business_embeddings"

    id = Column(BigInteger, primary_key=True, index=True)
    business_id = Column(BigInteger, ForeignKey("businesses.id", ondelete="CASCADE"))
    embedding_vector = Column(JSON, nullable=False)

    business = relationship("Business", back_populates="embeddings")
