# YouTube Channel Video Metadata API  

This project is a REST API that retrieves metadata for recent videos from any YouTube channel. It was developed as a solution to the following problem:  

## Problem Statement

Create a basic REST API that returns metadata for recent videos for any arbitrary YouTube channel.
This API should retrieve video metadata from a Dynamodb database table.
In the event that no videos for a channel are found, the video metadata should be retrieved from a 3rd party, free public data source, and then stored for later retrieval.
In no circumstance, excepting invalid channel ids, should the service return no video metadata.
This API should run entirely locally.
Write code with reasonable quality and guard against invalid channel ids, though don’t worry about robust testing and observability.  

Resources:  
- 3rd Party Data source:
  - Please find a free, public data source that can provide basic metadata that describes recently published videos for any channel. Avoid any data source that requires scraping or API keys. 
- YouTube channel ids:
  - All channels have a unique id provided by YouTube. Example (Mr Beast): `UCX6OQ3DkcsbYNE6H8uQQuVA`

----

## Setup
To get the API running on your machine, follow these steps:  
1. Download the source code to local.   
2. In the root of the project, run the command:  
   ```bash  
   docker compose up -d --build  
   ```  
   If port 80 is already in use on your machine, you can adjust the port settings directly in the `docker-compose.yml` file.

---

## Usage  

### Endpoint  
`GET /videos/{channel_id}`  

- Replace `{channel_id}` with the YouTube channel's unique ID.  

---  

## How It Works  

1. Checks DynamoDB for video metadata.  
2. If not found, retrieves data from the Google Feed XML endpoint:  
   `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`.  
3. Stores the fetched metadata in DynamoDB with a 24-hour expiration.

---

## Notes  

- Data stored in DynamoDB automatically expires after 24 hours to ensure relevance.  
  

