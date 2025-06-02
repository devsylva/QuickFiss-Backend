import multiprocessing

bind = "0.0.0.0:8000"
backlog = 2048
workers = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
accesslog = "/app/logs/gunicorn_access.log"
errorlog = "/app/logs/gunicorn_error.log"
loglevel = "info"
proc_name = "quickfiss_gunicorn"
preload_app = True
worker_tmp_dir = "/dev/shm"
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190