# Import GoogleCloudStorage from storages.backends.gcloud module
from storages.backends.gcloud import GoogleCloudStorage

# Create a GoogleCloudStorage object instance
storage = GoogleCloudStorage()


# Define an Upload class
class Upload:

    # Define a static method called upload_image that takes a file object and a filename string as arguments
    @staticmethod
    def upload_image(file, filename):
        try:
            # Create a target path by concatenating the '/images/' string with the filename
            target_path = '/images/' + filename

            # Save the file to Google Cloud Storage using the storage.save method and the target path
            path = storage.save(target_path, file)

            # Return the public URL of the uploaded file
            return storage.url(path)

        except Exception as e:
            # Print an error message if the file upload fails
            print("Failed to upload!")
