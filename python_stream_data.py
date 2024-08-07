from google.cloud import pubsub_v1
import datetime as dt
import time

# Get project details
project_id = "gdab-430616"
topic_id = "pubsub_dataflow_demo"

# Publisher Client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

for event_nbr in range(1, 100):
    data_str = '{}: {}'.format(event_nbr, dt.datetime.now())
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    time.sleep(1)
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, data, origin="python-sample", username="gcp"
    )
    # Print the published data string
    print(data_str)

print(f"Published messages with custom attributes to {topic_path}.")
