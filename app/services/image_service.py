import matplotlib
from sklearn.preprocessing import StandardScaler
import numpy as np
import tifffile as tiff
import cv2
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import io
import matplotlib.pyplot as plt

matplotlib.use('Agg')  # Set the backend to Agg for non-GUI use


class ImageService:

    @staticmethod
    def load_image(image_path):
        return tiff.imread(image_path)

    @staticmethod
    def compute_histogram(image: np.ndarray, bins: int = 256):
        """
        Computes a histogram for the image.
        """
        histogram, bin_edges = np.histogram(image, bins=bins, range=[image.min(), image.max()])
        return {
            "histogram": histogram.tolist(),
            "bin_edges": bin_edges.tolist()
        }

    @staticmethod
    def compute_statistics(image: np.ndarray):
        """
        Computes basic statistics (mean, std, min, max) for a given image.
        """
        return {
            "mean": float(np.mean(image)),
            "std_dev": float(np.std(image)),
            "min": float(np.min(image)),
            "max": float(np.max(image))
        }

    @staticmethod
    def get_statistics(image):

        # Get dimensions
        T, Z, C, X, Y = image.shape  # Shape example: (7, 24, 2, 256, 256)

        # Store statistics
        stats = []

        # Loop over each band (Z-slices × Channels)
        for t in range(T):
            for z in range(Z):
                for c in range(C):
                    band = image[t, z, c, :, :]  # Extract a single band (2D image)

                    # Compute statistics
                    mean_val = np.mean(band)
                    std_val = np.std(band)
                    min_val = np.min(band)
                    max_val = np.max(band)

                    # Append results
                    stats.append({
                        "Z": z,
                        "C": c,
                        "Mean": float(mean_val),
                        "Std Dev": float(std_val),
                        "Min": float(min_val),
                        "Max": float(max_val)
                    })

        return stats

    @staticmethod
    def get_image_metadata(image):
        return {
            "band": image.shape[0] * image.shape[1] * image.shape[2],
            "shape": image.shape,
            "dtype": str(image.dtype),
            "min": np.min(image),
            "max": np.max(image),
            "mean": np.mean(image),
            "std": np.std(image),
        }

    @staticmethod
    def extract_slice(image, t=0, z=0, c=0):
        return image[t, z, c, :, :] if len(image.shape) == 5 else image[z, :, :]

    @staticmethod
    def apply_pca(image, time_index=0, n_components=3):
        """
        Apply PCA to a specific time frame of the image and visualize the top components.

        Parameters:
        - image: 5D numpy array (T, Z, C, X, Y) representing the image stack.
        - time_index: The index of the time frame to analyze (default is 0).
        - n_components: Number of principal components to retain (default is 3).

        Returns:
        - Image as a byte stream (PNG format) containing the PCA components.
        """
        # Select a specific time frame
        image_at_t = image[time_index]  # Shape: (24, 2, 256, 256)

        # Reshape into 2D (Z × C, X * Y) -> Each band is a row
        Z, C, X, Y = image_at_t.shape
        flattened_image = image_at_t.reshape(Z * C, X * Y)  # Shape: (48, 65536)

        # Standardize the data (important for PCA)
        scaler = StandardScaler()
        flattened_image_scaled = scaler.fit_transform(flattened_image)

        # Apply PCA to reduce to `n_components` principal components
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(flattened_image_scaled)  # Shape: (48, n_components)

        # Transform back to original space
        pca_reconstructed = pca.inverse_transform(pca_result)  # Shape: (48, 65536)

        # Reshape to (n_components, 256, 256) - Keep the most significant components
        pca_image = pca_reconstructed[:n_components].reshape(n_components, X, Y)

        # Create a Matplotlib figure
        fig, axes = plt.subplots(1, n_components, figsize=(12, 4))

        for i in range(n_components):
            axes[i].imshow(pca_image[i], cmap="gray")
            axes[i].set_title(f"PCA Component {i + 1}")
            axes[i].axis("off")

        # Save figure to a BytesIO buffer
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight")
        img_bytes.seek(0)
        plt.close(fig)

        return img_bytes.getvalue()

    @staticmethod
    def apply_pca_v1(image, n_components=3):

        # Select a specific time frame
        time_index = 0  # Example: First time frame
        image_at_t = image[time_index]  # Shape: (Z, C, X, Y)

        # Get the shape dimensions
        Z, C, X, Y = image_at_t.shape

        # Flatten image to (bands, pixels) format
        bands = Z * C  # Total number of bands
        flattened_image = image_at_t.reshape(bands, X * Y)  # Shape: (bands, X*Y)

        # Standardize the data
        scaler = StandardScaler()
        flattened_image_scaled = scaler.fit_transform(flattened_image)

        # Apply PCA with dynamic number of components (capturing 95% variance)
        pca = PCA(n_components=0.95)  # Keeps enough components to explain 95% variance
        pca_result = pca.fit_transform(flattened_image_scaled)  # Shape: (bands, n_components)

        # Get the actual number of components chosen
        n_components = pca_result.shape[1]
        # print("pca_result.shape: ", pca_result.shape)
        # print(f"Using {n_components} principal components")

        # Transform back to original space
        pca_reconstructed = pca.inverse_transform(pca_result)  # Shape: (bands, X*Y)

        # Reshape dynamically based on `n_components`
        pca_image = pca_reconstructed[:n_components].reshape(n_components, X, Y)

        # Create a Matplotlib figure
        fig, axes = plt.subplots(1, n_components, figsize=(12, 4))

        for i in range(n_components):
            axes[i].imshow(pca_image[i], cmap="gray")
            axes[i].set_title(f"PCA Component {i + 1}")
            axes[i].axis("off")

        # Save figure to a BytesIO buffer
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight")
        img_bytes.seek(0)
        plt.close(fig)

        return img_bytes.getvalue()

    @staticmethod
    def apply_algo(image, time_index=0, z_index=12, channel_index=1, n_clusters=3):
        """
        Process a 5D TIFF image with Otsu's Thresholding and K-Means Clustering.

        Parameters:
        - image: the TIFF image file.
        - time_index: The index of the time frame to extract (default is 0).
        - z_index: The Z-slice index to extract (default is 12).
        - channel_index: The channel index to extract (default is 1).
        - n_clusters: The number of clusters for K-Means segmentation (default is 3).

        Returns:
        - Image as a byte stream (PNG format) containing the processed results.
        """

        # Extract the selected 2D image slice
        image_2d = image[time_index, z_index, channel_index, :, :]

        # Convert to 8-bit grayscale (if necessary)
        image_8bit = cv2.normalize(image_2d, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Apply Otsu's Thresholding
        _, otsu_thresh = cv2.threshold(image_8bit, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply K-Means Clustering
        pixels = image_8bit.reshape(-1, 1)  # Reshape to (N, 1)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)  # Segment into 3 clusters
        kmeans_labels = kmeans.fit_predict(pixels)
        segmented_kmeans = kmeans_labels.reshape(image_8bit.shape)

        # Plot the results
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))

        ax[0].imshow(image_8bit, cmap="gray")
        ax[0].set_title("Original Image")
        ax[0].axis("off")

        ax[1].imshow(otsu_thresh, cmap="gray")
        ax[1].set_title("Otsu's Thresholding")
        ax[1].axis("off")

        ax[2].imshow(segmented_kmeans, cmap="jet")
        ax[2].set_title("K-Means Segmentation")
        ax[2].axis("off")

        # Save figure to a BytesIO buffer
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight")
        img_bytes.seek(0)
        plt.close(fig)

        return img_bytes.getvalue()

