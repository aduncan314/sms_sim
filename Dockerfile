FROM python:3.9.19-alpine

WORKDIR /

COPY dist/sms_sim-0.1.0-py3-none-any.whl sms_sim-0.1.0-py3-none-any.whl
COPY run_config.yml run_config.yml

RUN python -m pip install sms_sim-0.1.0-py3-none-any.whl

ENTRYPOINT ["sms-simulate"]
