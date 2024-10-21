from apps import app
from common import rabmq

rabmq.run_consumer()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
else:
    application = app
