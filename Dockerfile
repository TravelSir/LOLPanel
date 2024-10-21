FROM e29e8363e7ff

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt -i https://pypi.qiyou.cn/simple
