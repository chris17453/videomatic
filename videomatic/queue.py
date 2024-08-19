import os
import json
import time
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor
from .flux import flux_image
from .svd import generate_video

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB", "media_queue"),
    "user": os.getenv("POSTGRES_USER", "queueuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "queuepass"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

def connect_to_db():
    return psycopg2.connect(**DB_PARAMS)

def get_next_item(conn):
    with conn.cursor() as cur:
        # First, check if there's any item in progress
        cur.execute("SELECT COUNT(*) FROM queue WHERE status = 'in_progress'")
        in_progress_count = cur.fetchone()[0]
        
        if in_progress_count > 0:
            return None  # There's an item in progress, so we can't process a new one

        # If no item is in progress, get the next pending item
        cur.execute("""
            SELECT id, user_id, media_type, generation_parameters
            FROM queue
            WHERE status = 'pending'
            ORDER BY priority DESC, submitted_at ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        """)
        item = cur.fetchone()
        if item:
            cur.execute("UPDATE queue SET status = 'in_progress', started_at = NOW() WHERE id = %s", (item[0],))
        conn.commit()
        return item

def process_item(item):
    item_id, user_id, media_type, params = item
    
    print(f"Type of params in process_item: {type(params)}")  # Add this line
    print(f"Content of params in process_item: {params}")  # Add this line

    # If params is already a dict, use it directly
    if isinstance(params, dict):
        params_dict = params
    # If it's a string, try to parse it as JSON
    elif isinstance(params, str):
        try:
            params_dict = json.loads(params)
        except json.JSONDecodeError:
            return None, "Invalid JSON in generation parameters"
    else:
        return None, f"Unexpected type for generation parameters: {type(params)}"

    print(f"Processing item {item_id}: {media_type} for user {user_id}")
    print(f"Parameters: {params_dict}")
    
    try:
        if media_type == 'image':
            filename = params_dict.get('output_file', f"generated_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
            flux_image(prompt=params_dict['prompt'], output_file=filename)
        elif media_type == 'video':
            filename = params_dict.get('output_file', f"generated_video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4")
            generate_video(
                image_path=params_dict['frame_path'],
                output_file=filename,
                seed=params_dict.get('seed', 42),
                decode_chunk_size=params_dict.get('decode_chunk_size', 8),
                motion_bucket_id=params_dict.get('motion_bucket_id', 10),
                noise_aug_strength=params_dict.get('noise_aug_strength', 0.1),
                fps=params_dict.get('fps', 8)
            )
        else:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        return filename, None
    except Exception as e:
        return None, str(e)

def complete_item(conn, item_id, filename, error_message):
    with conn.cursor() as cur:
        if error_message:
            cur.execute("""
                UPDATE queue
                SET status = 'error', completed_at = NOW(),
                    time_taken = completed_at - started_at,
                    error_message = %s
                WHERE id = %s
            """, (error_message, item_id))
        else:
            cur.execute("""
                UPDATE queue
                SET status = 'completed', completed_at = NOW(),
                    time_taken = completed_at - started_at,
                    result_file = %s
                WHERE id = %s
            """, (filename, item_id))
    conn.commit()

def main():
    conn = connect_to_db()
    try:
        while True:
            item = get_next_item(conn)
            if item:
                filename, error = process_item(item)
                complete_item(conn, item[0], filename, error)
                if error:
                    print(f"Error processing item {item[0]}: {error}")
                else:
                    print(f"Completed item {item[0]}, result: {filename}")
            else:
                print("No items to process at the moment. Waiting...")
                time.sleep(10)
    finally:
        conn.close()


def add_to_queue(conn, user_id, media_type, generation_parameters, priority=3):
    with conn.cursor() as cur:
        # Convert generation_parameters to JSON string if it's not already
        if not isinstance(generation_parameters, str):
            generation_parameters = json.dumps(generation_parameters)
        
        cur.execute("""
            INSERT INTO queue (user_id, media_type, generation_parameters, status, priority)
            VALUES (%s, %s, %s, 'pending', %s)
            RETURNING id
        """, (user_id, media_type, generation_parameters, priority))
        queue_id = cur.fetchone()[0]
    conn.commit()
    return queue_id


def get_queue_status(conn, queue_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM queue WHERE id = %s", (queue_id,))
        return cur.fetchone()

def update_queue_status(conn, queue_id, status, result_file=None, error_message=None):
    with conn.cursor() as cur:
        if status == 'completed':
            cur.execute("""
                UPDATE queue
                SET status = %s, completed_at = %s, result_file = %s,
                    time_taken = completed_at - started_at
                WHERE id = %s
            """, (status, datetime.now(), result_file, queue_id))
        elif status == 'error':
            cur.execute("""
                UPDATE queue
                SET status = %s, completed_at = %s, error_message = %s,
                    time_taken = completed_at - started_at
                WHERE id = %s
            """, (status, datetime.now(), error_message, queue_id))
        else:
            cur.execute("""
                UPDATE queue
                SET status = %s, started_at = %s
                WHERE id = %s
            """, (status, datetime.now(), queue_id))
    conn.commit()        

if __name__ == "__main__":
    main()
