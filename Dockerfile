FROM python:3.8-slim

#set the work directory
WORKDIR /server

#install the requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . /server/

#set the backend port

EXPOSE 4360

#will need to add to this later once server is done
ENTRYPOINT [ "python3","main.py" ]

