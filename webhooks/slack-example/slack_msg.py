import urllib3
import os
import json
from datetime import datetime

#Variables
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

# Lambda function handler
def lambda_handler(event, context):
    '''
    AWS Lambda function to handle incoming events, parse the data, and send a message to a Slack channel.

    This function is triggered by an event (e.g., an HTTP request through API Gateway) and processes the event data.
    It extracts relevant information from the event, formats it as a message, and sends this message to a specified
    Slack channel using a webhook.
    '''
    if event.get('body'):
        try:
            if type(event['body']) == str:
                body = json.loads(event['body'])
            else:
                body = event['body']
            calendar_name = body.get("calendar", {}).get("calendar_name", "Unknown Calendar")
            
            message_text = format_message(body)
            channel = get_slack_channel(calendar_name)
            send_slack_message(message_text, channel)
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error processing event data: {e}")
            return {'statusCode': 400, 'body': 'Invalid input data'}
    else:
        return {'statusCode': 400, 'body': 'Missing body in event'}

    return {'statusCode': 200, 'body': 'Message sent successfully'}
    
def send_slack_message(message,channel=SLACK_CHANNEL):

    url = 'https://slack.com/api/chat.postMessage'
    headers = {'Authorization': f'Bearer {SLACK_TOKEN}',
        'Content-Type': 'application/json'}
    payload = {
        'channel': channel,
        'text': message
    }
    http = urllib3.PoolManager()
    response = http.request('POST',url, headers=headers, body=json.dumps(payload))
    if response.status == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")


def format_message(body_dict):
    '''
    Formats a message string based on the provided body dictionary.

    The dictionary keys should correspond to placeholders in the message template. The function will replace
    placeholders in the message template with the values from the dictionary.

    Parameters:
        body_dict (dict): A dictionary containing keys and values for placeholders in the message template.

    Returns:
        str: A formatted message string.
    '''
    calendar = body_dict.get("calendar", {})
    start = body_dict.get("start", {})
    end = body_dict.get("end", {})
    attendees = body_dict.get("attendees", [])

    # Extract data from the event
    calendar_name = calendar.get("calendar_name", "Unknown Calendar")
    start_dt = datetime.fromisoformat(start.get("dateTime"))
    end_dt = datetime.fromisoformat(end.get("dateTime"))
    timezone_str = start.get("timeZone", "UTC")

    # Date and Time Formatting
    # This section handles how to format dates and times.
    # 
    # Options for date formatting:
    #   - Use %d/%m/%Y for the dd/mm/yyyy format (e.g., 25/12/2024)
    #   - Use %m/%d/%Y for the mm/dd/yyyy format (e.g., 12/25/2024)
    # 
    # Options for time formatting:
    #   - Use %H:%M for 24-hour time format (e.g., 14:30 for 2:30 PM)
    #   - Use %I:%M %p for 12-hour time format (e.g., 02:30 PM for 2:30 PM)
    #
    start_day_str = start_dt.strftime("%d/%m/%Y")  # Formatting the start date as dd/mm/yyyy
    start_time_str = start_dt.strftime("%H:%M")    # Formatting the start time as HH:MM (24-hour format)
    end_time_str = end_dt.strftime("%H:%M")        # Formatting the end time as HH:MM (24-hour format)

    # Check Attendees
    attendees_names = [attendee.get("name", "Unknown") for attendee in attendees]
    attendees_str = ", ".join(attendees_names) if attendees_names else "No attendees listed"

    # Message Text
    '''
    Portuguese (pt-br) text example:
    formatted_message = (f'📅 *{calendar_name}* - Novo agendamento para o dia {start_day_str}\n'
                    f'⏰ De {start_time_str} até {end_time_str} ({timezone_str})\n'
                    f'👤 Participantes: {attendees_str}')

    English (en-us) text example:
    formatted_message = (f'📅 *{calendar_name}* - New event on {start_day_str}\n'
                    f'⏰ From {start_time_str} to {end_time_str} ({timezone_str})\n'
                    f'👤 Attendees: {attendees_str}')

    Spanish (es) text example:
    formatted_message = (f'📅 *{calendar_name}* - Nuevo evento el día {start_day_str}\n'
                    f'⏰ De {start_time_str} a {end_time_str} ({timezone_str})\n'
                    f'👤 Asistentes: {attendees_str}')

    '''
    formatted_message = (f'📅 *{calendar_name}* - New event on {start_day_str}\n'
                    f'⏰ From {start_time_str} to {end_time_str} ({timezone_str})\n'
                    f'👤 Attendees: {attendees_str}')

    return formatted_message


def get_slack_channel(calendar_name):
    '''
    Retrieves the Slack channel corresponding to the provided calendar name.

    This function uses a dictionary to map calendar names to Slack channels. If the calendar name is not found
    in the dictionary, a default channel is returned.

    Parameters:
        calendar_name (str): The name of the calendar for which the corresponding Slack channel is to be retrieved.

    Returns:
        str: The Slack channel name associated with the provided calendar name.
    '''
    
    # Define a dictionary for calendar-to-channel mapping
    channel_dict = {
        "Candidate Recruiting": "#recruitment_interviews",
        "Sales Presentation": "#sales_team",
        "Product Launch": "#product_updates",
        "Customer Support": "#customer_support",
        # Add more mappings as needed
    }

    # Retrieve the Slack channel based on the calendar name
    return channel_dict.get(calendar_name, SLACK_CHANNEL)