import boto3
import json
import os

from fake_web_events import Simulation

#set the profile to connect into aws, if you use default dont change.
perfil_name = '''default'''
os.environ["AWS_PROFILE"]=str(perfil_name)

client = boto3.client('firehose', region_name='us-east-1')


def put_record(event:dict):
    data = json.dumps(event) + "\n"
    response = client.put_record(
        DeliveryStreamName='edg-carlos-henrique',
        Record={"Data" : data}
    )
    print(event)
    return response

simulation = Simulation(user_pool_size=100, sessions_per_day=100000)
events = simulation.run(duration_seconds=360)

for event in events:
    put_record(event)


