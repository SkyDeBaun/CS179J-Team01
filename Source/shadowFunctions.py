# srcCallback - Function to be called when the response for this shadow request comes back. 
# Should be in form customCallback(payload, responseStatus, token) 
# Payload is the JSON document returned, 
# responseStatus indicates whether the request has been accepted, rejected or is a delta message, 
# token is the token used for tracing in this request.