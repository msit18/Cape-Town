# 1.  Connecting to the service instance.

# Enable the required Python libraries.

from cloudant.client import Cloudant
# from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

# # # Useful variables
USERNAME = "citivan"
PASSWORD = "CityVan1"
serviceURL = "https://citivan.cloudant.com"

# # This is the name of the database we are working with.
databaseName = "databasedemo"

# # This is a simple collection of data,
# # to store within the database.
# sampleData = [
#     [1, "one", "boiling", 100],
#     [2, "two", "hot", 40],
#     [3, "three", "warm", 20],
#     [4, "four", "cold", 10],
#     [5, "five", "freezing", 0]
# ]

# # Start the demo.
# print "===\n"

# # Use the Cloudant library to create a Cloudant client.
# # client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client = Cloudant(USERNAME, PASSWORD, url='https://citivan.cloudant.com', connect=True, auto_renew=True)
# session = client.session()
# print 'Username: {0}'.format(session['userCtx']['name'])
# print 'Databases: {0}'.format(client.all_dbs())

# # # Connect to the server
# client.connect()

# # # 2.  Creating a database within the service instance.

# # # Create an instance of the database.
# # myDatabaseDemo = client.create_database(databaseName)
# myDatabaseDemo = client['databasedemo']

# # # Check that the database now exists.
# if myDatabaseDemo.exists():
#     print "'{0}' successfully created.\n".format(databaseName)

# # # Space out the results.
# print "----\n"

# # # 3.  Storing a small collection of data as documents within the database.

# # # Create documents using the sample data.
# # # Go through each row in the array
# for document in sampleData:
#     # Retrieve the fields in each row.
#     number = document[0]
#     name = document[1]
#     description = document[2]
#     temperature = document[3]

#     # Create a JSON document that represents
#     # all the data in the row.
#     jsonDocument = {
#         "numberField": number,
#         "nameField": name,
#         "descriptionField": description,
#         "temperatureField": temperature
#     }

# # #     # Create a document using the Database API.
# #     newDocument = myDatabaseDemo.create_document(jsonDocument)

# # #     # Check that the document exists in the database.
# #     if newDocument.exists():
# #         print "Document '{0}' successfully created.".format(number)

# # Space out the results.
# print "----\n"

# # # 4.  Retrieving a complete list of the documents.

# # # Simple and minimal retrieval of the first
# # # document in the database.
# result_collection = Result(myDatabaseDemo.all_docs)
# print "Retrieved minimal document:\n{0}\n".format(result_collection[0])

# # # Simple and full retrieval of the first
# # # document in the database.
# result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
# print "Retrieved full document:\n{0}\n".format(result_collection[0])

# # Space out the results.
# print "----\n"

# # result = result_collection['temperatureField']
# # print "RESULT KEY: ", result

# #outputs all of them
# for result2 in result_collection[0]:
#     print "results1: ", result2

# print "----\n"

# # Use a Cloudant API endpoint to retrieve
# # all the documents in the database,
# # including their content.

# # Define the end point and parameters
# end_point = '{0}/{1}'.format(serviceURL, databaseName + "/_all_docs")
end_point = '{0}/{1}'.format(serviceURL, databaseName + "/19d2fcada698f7d3e51fb78751517e54")
params = {'include_docs': 'true'}

# # Issue the request
response = client.r_session.get(end_point, params=params)
print "TYPE: ", type(response.json())

# # Display the response content
print "ENDPT {0}\n".format(response.json())

all_response = response.json()

print "ENDPT KEY: ", all_response['temperatureField']

# # Space out the results.
print "----\n"

all_response["key1"] = "value1"
all_response["key2"] = "value2"
payload = {'key1': 'value1', 'key2': 'value2'}

print "ALL RESPONSE: ", all_response

r = client.r_session.put(end_point, json=all_response)
print "ENDPT {0}\n".format(r.json())

# # All done.
# # Time to tidy up.

# # 5.  Deleting the database.

# # Delete the test database.
# try :
#     client.delete_database(databaseName)
# except CloudantException:
#     print "There was a problem deleting '{0}'.\n".format(databaseName)
# else:
#     print "'{0}' successfully deleted.\n".format(databaseName)

# 6.  Closing the connection to the service instance.

# Disconnect from the server
client.disconnect()

# Finish the demo.
print "===\n"

# Say good-bye.
exit()