from unidecode import unidecode
import uuid
from datetime import datetime

def secure_filename(filename):
    return "_".join(unidecode(filename).split(" "))

def generateUniquePrefix():
    unique_id = uuid.uuid4()

    # Get the current timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")[:-3]

    # Combine the timestamp and UUID to create a unique prefix
    unique_prefix = f"{timestamp}_{unique_id}"
    
    return unique_prefix