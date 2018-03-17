FROM python:3.6.3
ADD . /project
RUN pip install -r /project/requirements.txt
RUN cd /project/
RUN python test.py
EXPOSE 5000
CMD ["python app.py"]