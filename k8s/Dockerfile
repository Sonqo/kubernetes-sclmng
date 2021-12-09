FROM python:3

# python script for resource monitoring
ADD monitoring/metrics.py /

# add .yaml files
# ADD mongo/mongo-replica_v2.yaml /

# install kubectl
RUN curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin

RUN pip install kubernetes

CMD [ "python", "-u", "./metrics.py" ]
