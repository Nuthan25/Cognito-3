import boto3
import botocore

def lambda_handler(event, context):
    user_pool_id = 'us-east-2_5qfmsycFA'
    client = boto3.client('cognito-idp')

    try:
        users = client.list_users(UserPoolId=user_pool_id)
        custom_attribute_name = 'locale'
        custom_attribute_value = '0'  # Replace with the desired name

        for user in users['Users']:
            username = None
            # Find the 'Username' attribute in the user object
            for attr in user['Attributes']:
                if attr['Name'] == 'sub':
                    username = attr['Value']
                    break

            if username:
                # Update the 'name' attribute for each user
                response = client.admin_update_user_attributes(
                    UserPoolId=user_pool_id,
                    Username=username,
                    UserAttributes=[
                        {
                            'Name': custom_attribute_name,
                            'Value': custom_attribute_value
                        }
                    ]
                )

        return {
            'statusCode': 200,
            'body': 'Custom attribute "name" added to all users'
        }

    except botocore.exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'body': 'Error: {}'.format(str(e))
        }
