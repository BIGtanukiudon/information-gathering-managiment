import os

# Server Socket
bind = "0.0.0.0:8080"

# Worker Processes
workers = 2 * os.cpu_count() + 1
threads = 2 * os.cpu_count() + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Debugging
reload = True

# Logging
accesslog = os.path.join(os.getcwd(), "logs/access.log")
errorlog = os.path.join(os.getcwd(), "logs/error.log")
loglevel = "warning"
