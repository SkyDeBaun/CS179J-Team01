import boto3
from boto3.dynamodb.conditions import Key, Attr

# setup fields
__TableName__ = "tempHumidityData"
Primary_Column_Name = "entryNumber"
columns = ["temperature", "humidity"]

# resource and table
DB = boto3.resource("dynamodb")
table = DB.Table(__TableName__)

# test that we can retrieve valid row in table by the row's Primary Key
Primary_Key = 1
response = table.query(
        KeyConditionExpression=Key('ID').eq(Primary_Key)
)

# print matching row
print(response["Items"])

# test that we can insert a new row into table (giving it Primary Key = 2)
#Primary_Key = "2"

#response = table.put_item(
#    Item={
#        Primary_Column_Name: Primary_Key,
#        columns[0]: "Ryan",
#        columns[1]: "Meoni"
#            }
#        )

# print all table entries to test we inserted correctly
# get all rows with a primary key (entryNumber) greater than or equal to 0

response = table.scan(
    FilterExpression=Attr('ID').gte(0)
)

print(response)

for row in response["Items"]:
	print(row)
