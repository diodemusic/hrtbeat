import boto3

client = boto3.client("ses", region_name="eu-west-2")


def send_email(address, url):
    response = client.send_email(
        Source="alerts@hrtbeat.io",
        Destination={
            "ToAddresses": [
                address,
            ]
        },
        Message={
            "Subject": {"Data": "Outage", "Charset": "UTF-8"},
            "Body": {
                "Text": {
                    "Data": f"Your site {url} is currently experiencing an outage.",
                    "Charset": "UTF-8",
                },
            },
        },
    )

    return response
