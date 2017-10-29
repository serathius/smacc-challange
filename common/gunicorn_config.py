bind = '0.0.0.0:80'
preload_app = True
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'


def on_starting(server):
    # printing object is simple way to force gunicorn to evaluate app
    print(server.app.callable)
