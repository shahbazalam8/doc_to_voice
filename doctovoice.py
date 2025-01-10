import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from io import BytesIO
from tempfile import TemporaryFile
from docx import Document

# Initialize S3 and Polly clients
s3 = boto3.client('s3')
polly = boto3.client('polly')

def lambda_handler(event, context):
    try:
        # Get bucket and object key from the event
        bucket_name = event['bucket_name']
        object_key = event['object_key']

        # Download file from S3
        file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = file_obj['Body'].read()

        # Determine file type
        if object_key.endswith('.txt'):
            text = file_content.decode('utf-8')
        elif object_key.endswith('.docx'):
            text = read_docx_content(BytesIO(file_content))
        else:
            return {"statusCode": 400, "body": "Unsupported file type"}

        # Use Polly to synthesize text to speech
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'  # Replace with your preferred voice
        )

        # Save the audio to a temporary file
        with TemporaryFile() as temp_audio_file:
            temp_audio_file.write(response['AudioStream'].read())
            temp_audio_file.seek(0)

            # Upload the audio file back to S3
            audio_key = f"{os.path.splitext(object_key)[0]}.mp3"
            s3.upload_fileobj(temp_audio_file, bucket_name, audio_key)

        return {
            "statusCode": 200,
            "body": f"Audio file generated and saved to {audio_key}"
        }

    except (BotoCoreError, ClientError) as error:
        return {"statusCode": 500, "body": f"Error: {str(error)}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Unhandled exception: {str(e)}"}

def read_docx_content(file_stream):
    """
    Reads text content from a .docx file.
    """
    doc = Document(file_stream)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)
