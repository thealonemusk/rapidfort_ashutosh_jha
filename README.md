# File Upload App Documentation

This documentation provides an overview of the File Upload App, explaining its functionality and how to run it using Docker.

### Introduction
The File Upload App is a simple web application built using Flask, a Python web framework. It allows users to upload files to the server and view details about the uploaded files, including their size and extension. The app consists of a backend written in Python and a frontend built with HTML and JavaScript.

### Running the App
##### Prerequisites

Before running the app, ensure you have the following installed:
- Docker

##### Building and Running with Docker (Windows)
The script `start.bat` creates docker image for source code and then `creates` and `runs` the docker container.
- Start the Docker container using the provided script `start.bat`:
```
start.bat <image-name>
```
Note: Set any name for your image. This will be hosted on localhost port 8080

##### Custom Image Creation and Docker Run Command
```
docker build -t <image-name> <project-directory>
```
Run the Docker container using the following command:
```
docker run -p <port>:8080 <image-name>
```
Note: Set port value on which you want to host your app
### Using the App
Open a web browser and go to http://localhost:8080/.
You'll see a page with a file upload form. Choose a file.
After uploading, the app will display the file details, including the filename, size, and extension, on the same page.
This will temporarily store the file to server and the file can be further processed for metadata extraction.
