from apps.crawler import crawler_bp
from apps.panel import panel_bp
from common import app
from apps.crawler import msg_handler

app.register_blueprint(crawler_bp, url_prefix='/api/lol', name='crawler')
app.register_blueprint(panel_bp, url_prefix='/api/lol', name='panel')

