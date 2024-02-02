import json

#retrieve employee pto
def get_pto(employee_id):
    pto_limits = {'123': 35, '456': 25}
    return pto_limits.get(employee_id, -1)

#update employee pto
def update_pto(employee_id, pto_days):
    pto_limits = {'123': 55, '456': 20}
    total_pto = pto_limits.get(employee_id, -1)
    
    if total_pto != -1:
        # Update the pto
        return total_pto - pto_days
    else:
        return -1
    
def lambda_handler(event, context):

    #retrieve event variables
    action = event.get('actionGroup', '')
    api_path = event.get('apiPath', '')
    http_method = event.get('httpMethod', '')
    parameters = event.get('parameters', [])

    result_payload = handle_api_request(action, api_path, http_method, parameters)
    
    #create the response body
    response_body = {
        'application/json': {
            'body': str(result_payload)
        }
    }
    
    #create the response
    action_response = {
        'actionGroup': action,
        'apiPath': api_path,
        'httpMethod': http_method,
        'httpStatusCode': 200,
        'responseBody': response_body
    }

    #return the response
    api_response = {'response': action_response}
    return api_response

#convenience function to process the incoming api request based on paths
def handle_api_request(action, api_path, http_method, parameters):
    balance = 0
    result_payload = {}

    if api_path == '/employeepto/{employee_id}':
        employee_id, balance = handle_employeepto_get(parameters, http_method)
    elif api_path == '/employeepto/{employee_id}/{pto_days}':
        employee_id, pto_days, balance = handle_employeepto_put(parameters, http_method)
    else:
        result_payload = {"error": "{}::{} is not a valid api, try another one.".format(action, api_path)}

    #return an error if there was no employee match
    if balance == -1:
        result_payload = {"error": "Invalid employee ID or operation."}

    if not result_payload.get("error"):
        result_payload = {
            "response": {
                "employee_id": employee_id,
                "pto_remaining": balance
            }
        }

    return result_payload

#process get requests
def handle_employeepto_get(parameters, http_method):
    employee_id = get_parameter_value(parameters, 'employee_id')
    balance = 0
    if http_method.lower() == 'get':
        balance = get_pto(employee_id)
    return employee_id, balance

#process put / update requests
def handle_employeepto_put(parameters, http_method):
    employee_id = get_parameter_value(parameters, 'employee_id')
    pto_days = get_parameter_value(parameters, 'pto_days')
    balance = 0
    if http_method.lower() == 'put':
        balance = update_pto(employee_id, int(pto_days))
    return employee_id, pto_days, balance

#convenience function to retrieve parameter values
def get_parameter_value(parameters, key):
    for param in parameters:
        if param.get('name') == key:
            return param.get('value', '')
    return ''
