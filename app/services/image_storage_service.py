from app.core.database import SessionLocal
from app.models.image_model import ImageMetadata, PCAResult, KMeansSegmentation
from sqlalchemy.orm import Session
from app.services.image_service import ImageService


class ImageStorageService:

    @staticmethod
    def store_image_metadata(image_path: str):
        """
        Process a TIFF image in chunks to reduce memory usage.
        - Applies PCA and K-Means segmentation.
        - Stores results in SQLite or PostgresSQL database.
        """

        try:
            db_session: Session = SessionLocal()
            image_processor = ImageService()
            # Load the image
            image_5d = ImageService.load_image(image_path)
            if len(image_5d.shape) < 5:
                return "Oops! Your image is not 5D!"

            # Select a specific time frame, Z-slice, and channel
            # time_index, z_index, channel_index = 0, 12, 1
            # image_2d = image_5d[time_index, z_index, channel_index, :, :]

            # Store metadata in DB
            metadata = ImageMetadata(
                filename=image_path.split("/")[-1],
                width=image_5d.shape[3],
                height=image_5d.shape[4],
                channels=image_5d.shape[2],
                bands=image_5d.shape[0] * image_5d.shape[1] * image_5d.shape[2],  # Store the number of PCA bands used
                file_path=image_path
            )
            db_session.add(metadata)
            db_session.commit()
            # print("metadata: ", metadata)

            # Store PCA results in DB
            pca_entry = PCAResult(
                image_id=metadata.id,
                img_bytes=image_processor.apply_pca(image_5d)
            )
            db_session.add(pca_entry)

            # Store K-Means results in DB
            kmeans_entry = KMeansSegmentation(
                image_id=metadata.id,
                img_bytes=image_processor.apply_algo(image_5d)
            )
            db_session.add(kmeans_entry)

            # Commit all changes
            db_session.commit()

            return f"Processing complete for '{metadata.filename}' and results saved to DB."
        except Exception as e:
            return str(e)