import boto3
import os
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def get_ses_client():
	"""
	Connect to AWS APIs
	:return: Simple Email Service client
	"""
	# Not available in Asia
	return boto3.client('ses', region_name='ap-southeast-2')

def get_ssm_client():
	"""
	Connect to AWS APIs
	:return: Simple Email Service client
	"""
	# Not available in Asia
	return boto3.client('ssm')
	
def send_email(ses_client, sender, recipients, subject, body):
	"""
	Send email with attachment
	:param ses_client: AWS SES client
	:param sender: from address
	:param recipients: to addresses
	:param subject: subject of the email
	:param body: body of the email
	:return:
	"""
	CHARSET = "utf-8"
	# Create a multipart/mixed parent container.
	msg = MIMEMultipart('mixed')

	# Add subject, from and to lines.
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ','.join(recipients)
	msg['Body'] = body

	# Create a multipart/alternative child container.
	msg_body = MIMEMultipart('alternative')

    # This step is necessary if you're sending a message with characters outside the ASCII range.
	textpart = MIMEText(body.encode(CHARSET), 'plain', CHARSET)


    # Add the text and HTML parts to the child container.
	msg_body.attach(textpart)

	# Attach the multipart/alternative child container to the multipart/mixed parent container.
	msg.attach(msg_body)


	response = ses_client.send_raw_email(
		Source=sender,
		Destinations=recipients,
		RawMessage={'Data': msg.as_string(),}
	)

def get_run_commands():
    """
	Get latest list of AWS-RunPatchBaseline commands
	:return: AWS-RunPatchBaseline
	"""
    command_list = get_ssm_client().list_command_invocations(
        MaxResults=10,
        Filters=[
            {
                'key':'DocumentName',
                'value': 'AWS-RunPatchBaseline'
            },
        ],
    )
    return command_list
    
def create_body(list):
    """
	Convert list of commands/instance id's into a string
	:return: create body for ses
	"""
    string = "the instance(s) below have failed the latest patch run command\n" 
    
    for ele in list: 
        string += (ele+"\n")
    
    return string
	


def lambda_handler(event, context):

    #Initialize variables
    commands = []
    check_date = datetime.today() - timedelta(days=7)
    check_date = check_date.strftime("%Y/%m/%d")

    #Get list of latest AWS-RunPatchBaseline commands and loop through them
    for command in get_run_commands()['CommandInvocations']:

        #Get commands that have failed
        if(command['Status'] == "Failed"):
            command_date = command['RequestedDateTime']
            clean_date = command_date.strftime("%Y/%m/%d")
            
            #Get commands that have only failed in the last 7 days
            if(clean_date > check_date):
                commands.append("InstanceID- " + command['InstanceId'] + " | " + "CommandID- " + command["CommandId"])

    #if commands is not null - send the alert
    if(commands):
    	ses_client = get_ses_client()
    	sender = os.getenv("SENDER")
    	recipients = os.getenv("RECIPIENTS").split(",")
    	subject = os.getenv("SUBJECT")
    	body = create_body(commands)
    	send_email(ses_client, sender, recipients, subject, body)