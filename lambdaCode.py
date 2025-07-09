import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    output_bucket = 'output-bucket-keran'  

    image_obj = s3.get_object(Bucket=source_bucket, Key=key)
    image = Image.open(image_obj['Body'])
    image = image.resize((100, 100))  # Resize to 100x100

    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)

    s3.put_object(Bucket=output_bucket, Key='resized-' + key, Body=buffer)
    return {'status': 'Image resized'}
