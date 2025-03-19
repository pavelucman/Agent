# Agent


In this project, I added the database (whatsapp.db) that was previously delivered. The Python libraries I used were: fastapi, uvicorn, sqlalchemy, psycopg2, requests, cryptography, aiohttp.

I made a connection to it using the credentials that were assigned to me. In the project, I have two python files and one html file. In the first python file main.py, I have written a connection to the database as well as its data extraction. Since it was not specifically written from which table the data is taken, I consider the messages that have been sent to be important data, so I took the data from the Message table (it can be taken from any query table). Since I loaded the data from whatsapp.db, I have a section where it is commented that it can also be encrypted and when sent to the server it must first be decrypted and then written to our database. Currently, the data that is loaded is sent to our server and written to the database. I read the written data from the server and display it in a table on the frontend (index.html). The second python file server.py is the backend, creating FastAPI calls, I have defined

origins = [ "http://localhost:63342", "http://localhost:3000", ]

this is inserted so that I can call http://localhost:8000/upload_data/ and http://localhost:8000/messages/ via http://localhost:8000/ Additionally, I needed to turn off the firewall.

I did this entire task via terminal and PyCharm IDE. To run the server via terminal, I navigate to the src folder and run this command: uvicorn server:app --reload and then run the main.py file from pyCharm. This is to start the server. At http://localhost:8000/docs/ you can see the two API calls I created, one POST and the other GET.

In server.py I have two functions: a connection to the new database I created on the server, upload_data() which receives a message model as a parameter that I previously defined above, and get_messages() which is used to read the data from that new database for display on the frontend. Additionally, I have added a check if the value is None to make sure it is not empty to display 'No Data'.

After it writes the data to the database, if there is no new data, it tells us that the data already written cannot be overwritten. In the database on the server, I have created a table messages, where all the extracted data is. I have taken some parameters, but they can be changed and configured.

app.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=[""], allow_headers=[""], )

This code is used for firewall.

I have additional screenshots and additional terminal command executions that I can share if needed.