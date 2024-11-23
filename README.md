# Project Documentation

## API URL fOR TESTING

Code on the api branch of the same repository

https://rapidfort-ashutosh-jha-2.onrender.com

ENDPOINTS:

* Health check: `GET /api/health`
* Convert DOCX to PDF: `POST /api/convert`
* Download PDF: `GET /api/download/<filename>`

## Docker Hub Links

app -> https://hub.docker.com/repository/docker/thealonemusk/d2p/general

api ->

## Project Overview

This project is a Flask-based application that includes the following features:

- Converts documents to PDF format.
- Organized directory structure for easy maintainability.
- Dockerized for seamless deployment.

---

## File Structure

.github/                # GitHub workflows or configurations
templates/              # HTML templates for the Flask app
uploads/                # Directory to store uploaded files
.dockerignore           # Files and folders to exclude from Docker build
.gitignore              # Git ignored files/folders
app.py                  # Main Flask application file
Dockerfile              # Docker configuration file to containerize the app
README.md               # Project overview (this file)
requirements.txt        # Python dependencies
run_container.sh        # Script to build and run the Docker container

---

## Installation and Setup

### 1. Prerequisites

- **Docker** installed on your system.
- **Bash** (for running the script).
- Optional: A Python environment for local testing.

---

### 2. Local Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the application locally:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

---

## Docker Instructions

### 1. Build and Run the Container

You can use the `run_container.sh` script to build and run the Docker container.

#### Usage

```bash
./run_container.sh <image-name> <port>
```

#### Example

```bash
./run_container.sh docx-to-pdf-converter 8080
```

- **Arguments**:
  - `<image-name>`: The name you want to give the Docker image (e.g., `docx-to-pdf-converter`).
  - `<port>`: The port on your host machine where the app will run (e.g., `8080`).

#### Steps Performed by the Script

1. Builds the Docker image using the `Dockerfile`.
2. Runs a Docker container using the built image.
3. Maps the specified host port to the container's internal port (`8080`).

### 2. Manually Run Docker Commands

If you prefer, you can manually build and run the Docker container:

#### Build the Docker Image

```bash
docker build -t <image-name> .
```

#### Run the Docker Container

```bash
docker run -d -p <host-port>:8080 --name <container-name> <image-name>
```

---

## Accessing the Application

- **Local Setup**: Access the app at `http://127.0.0.1:5000`.
- **Dockerized Setup**: Access the app at `http://localhost:<port>`.

Replace `<port>` with the value specified during the Docker run command or script execution.

---

## Troubleshooting

1. **Docker Build Fails**:

   - Ensure Docker is installed and running.
   - Check `.dockerignore` to ensure necessary files are not excluded.
2. **Application Not Accessible**:

   - Verify that the port is correctly forwarded.
   - Check the Docker logs for issues:
     ```bash
     docker logs <container-name>
     ```
3. **Permission Errors in OneDrive Folders**:

   - Move the project directory out of OneDrive and try again.

---

## Additional Notes

- The `requirements.txt` file lists all Python dependencies.
- Use the `.gitignore` and `.dockerignore` files to manage unnecessary files and directories.
- Ensure `run_container.sh` has executable permissions before running:
  ```bash
  chmod +x run_container.sh
  ```
