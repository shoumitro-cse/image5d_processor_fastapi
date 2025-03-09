from sqlalchemy import Column, Integer, String, ForeignKey, JSON, LargeBinary
from sqlalchemy.orm import relationship
from app.core.database import Base


class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=True, unique=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    channels = Column(Integer, nullable=False)
    bands = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)

    # Relationships
    pca_results = relationship("PCAResult", back_populates="image", cascade="all, delete-orphan")
    kmeans_results = relationship("KMeansSegmentation", back_populates="image", cascade="all, delete-orphan")


class PCAResult(Base):
    __tablename__ = "pca_results"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("image_metadata.id", ondelete="CASCADE"), nullable=False)
    img_bytes = Column(LargeBinary, nullable=True)

    image = relationship("ImageMetadata", back_populates="pca_results")


class KMeansSegmentation(Base):
    __tablename__ = "kmeans_results"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("image_metadata.id", ondelete="CASCADE"), nullable=False)
    # clusters = Column(JSON, nullable=False)  # Store K-Means clusters as JSON
    img_bytes = Column(LargeBinary, nullable=True)

    image = relationship("ImageMetadata", back_populates="kmeans_results")