from flask import jsonify
from flask import current_app
from flask.views import MethodView
import json


class CustomAPISpecsView(MethodView):
    """
    The /apispec_1.json and other specs
    """

    def __init__(self, *args, **kwargs):
        self.loader = kwargs.pop('loader')
        super(CustomAPISpecsView, self).__init__(*args, **kwargs)

    def get(self):
        """
        The Swagger view get method outputs to /apispecs_1.json
        """
        if not current_app.config.get('SWAGGER_CONFIG', {}).get('debug', False):
            return jsonify({})
        base_swagger = self.loader()
        # self._add_ali_api_params(base_swagger['paths'])
        if "SWAGGER_FILE" in current_app.config:
            swagger_json_str = open(current_app.config.get('SWAGGER_FILE', 'api_swagger.json')).read()
            history_swagger = json.loads(swagger_json_str)
            history_swagger_paths = history_swagger.pop("paths")
            base_swagger.update(history_swagger)
            base_swagger['paths'].update(history_swagger_paths)
        return jsonify(base_swagger)

    # def _add_ali_api_params(self, paths):
    #     for path, method_value in paths.items():
    #         for method, value in method_value.items():
    #             value.update({
    #                 "x-aliyun-apigateway-backend": {
    #                     "type": "HTTP-VPC",
    #                     "vpcAccessName": "#CBSVPC#",
    #                     "path": path,
    #                     "timeout": "10000"
    #                 },
    #             })
    #     return paths


def custom_api_specs_view_get(self):
    """
    The Swagger view get method outputs to /apispecs_1.json
    """
    if not current_app.config.get('SWAGGER_CONFIG', {}).get('debug', False):
        return jsonify({})
    # 判断swagger使用模式
    if "SWAGGER_FILE" in current_app.config:
        return open(current_app.config.get('SWAGGER_FILE', 'api_swagger.json')).read()
    return jsonify(self.loader())
