FROM public.ect.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY app/* ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]