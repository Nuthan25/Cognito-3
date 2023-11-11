import boto3

def lambda_handler(event, context):
    # Obtain the username (sub) from the event or the authentication response
    username = 'test@example.com'  # Adjust this based on your event structure

    if not username:
        return {
            'statusCode': 400,
            'body': 'Username not provided'
        }

    user_pool_id = 'us-east-2_5qfmsycFA'
    client = boto3.client('cognito-idp')

    try:
        # Get the user's current login count
        response = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=username
        )

        login_count = 0

        # Check if the "loginCount" custom attribute exists
        for attr in response['UserAttributes']:
            if attr['Name'] == 'locale':
                login_count = int(attr['Value'])
                break

        # Increment the login count
        login_count += 1

        # Update the "loginCount" attribute for the user
        client.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'locale',
                    'Value': str(login_count)
                }
            ]
        )

        return {
            'statusCode': 200,
            'body': 'Login count updated'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error: {}'.format(str(e))
        }
