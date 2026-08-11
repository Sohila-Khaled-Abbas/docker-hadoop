# syntax=docker/dockerfile:1
FROM ubuntu:20.04

LABEL maintainer="Ahmed Sami <ahmed.sami@yahoo.com>"
LABEL org.opencontainers.image.title="Apache Hadoop Docker Cluster"
LABEL org.opencontainers.image.description="Production-ready single-node Apache Hadoop 3.1.2 cluster container"
LABEL org.opencontainers.image.version="3.1.2"

ARG HADOOP_VERSION=3.1.2
ARG HADOOP_USER=hduser
ARG HADOOP_GROUP=hadoop

ENV DEBIAN_FRONTEND=noninteractive
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
ENV JAVA_HOME=/usr/local/java
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-8-jdk \
    openssh-server \
    openssh-client \
    rsync \
    sudo \
    wget \
    curl \
    tar \
    procps \
    iputils-ping \
    net-tools \
    vim \
    nano \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Symlink Java 8 to /usr/local/java
RUN ln -s /usr/lib/jvm/java-8-openjdk-amd64 /usr/local/java

# Create dedicated hadoop user & group
RUN groupadd ${HADOOP_GROUP} \
    && useradd -m -g ${HADOOP_GROUP} -s /bin/bash ${HADOOP_USER} \
    && echo "${HADOOP_USER}:ubuntu" | chpasswd \
    && echo "root:H@doop2022" | chpasswd \
    && usermod -aG sudo ${HADOOP_USER} \
    && echo "${HADOOP_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH for passwordless communication
RUN mkdir -p /var/run/sshd \
    && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config \
    && echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config

# Pre-generate SSH keypairs for hduser and root
RUN su - ${HADOOP_USER} -c "ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys && \
    chmod 0700 ~/.ssh" \
    && ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa \
    && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys \
    && chmod 0600 /root/.ssh/authorized_keys \
    && chmod 0700 /root/.ssh

# Download and extract Apache Hadoop binary (with auto-resume on network interruption)
RUN set -x \
    && for i in $(seq 1 10); do \
         wget -c -t 10 --timeout=45 --no-check-certificate \
         "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" \
         -O /tmp/hadoop.tar.gz && test -s /tmp/hadoop.tar.gz && break || sleep 3; \
       done \
    && tar -xzf /tmp/hadoop.tar.gz -C /usr/local/ \
    && mv /usr/local/hadoop-${HADOOP_VERSION} ${HADOOP_HOME} \
    && rm -f /tmp/hadoop.tar.gz

# Create directories for Hadoop metadata, data blocks, temp, and logs
RUN rm -rf ${HADOOP_HOME}/share/doc \
    && mkdir -p /app/hadoop/tmp \
    && mkdir -p ${HADOOP_HOME}/yarn_data/hdfs/namenode \
    && mkdir -p ${HADOOP_HOME}/yarn_data/hdfs/datanode \
    && mkdir -p ${HADOOP_HOME}/logs \
    && chown -R ${HADOOP_USER}:${HADOOP_GROUP} ${HADOOP_HOME} /app/hadoop \
    && chmod -R 777 ${HADOOP_HOME} /app/hadoop

# Copy configuration files
COPY config/core-site.xml ${HADOOP_CONF_DIR}/core-site.xml
COPY config/hdfs-site.xml ${HADOOP_CONF_DIR}/hdfs-site.xml
COPY config/mapred-site.xml ${HADOOP_CONF_DIR}/mapred-site.xml
COPY config/yarn-site.xml ${HADOOP_CONF_DIR}/yarn-site.xml
COPY config/hadoop-env.sh ${HADOOP_CONF_DIR}/hadoop-env.sh

RUN chown -R ${HADOOP_USER}:${HADOOP_GROUP} ${HADOOP_CONF_DIR} \
    && chmod -R 777 ${HADOOP_CONF_DIR}

# Add environment variables to hduser and root profiles
RUN echo 'export JAVA_HOME=/usr/local/java' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_HOME=/usr/local/hadoop' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_MAPRED_HOME=/usr/local/hadoop' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_COMMON_HOME=/usr/local/hadoop' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_HDFS_HOME=/usr/local/hadoop' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export YARN_HOME=/usr/local/hadoop' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native' >> /home/${HADOOP_USER}/.bashrc \
    && echo 'export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"' >> /home/${HADOOP_USER}/.bashrc \
    && cat /home/${HADOOP_USER}/.bashrc >> /root/.bashrc

# Copy automation scripts
COPY scripts/entrypoint.sh /entrypoint.sh
COPY scripts/healthcheck.sh /healthcheck.sh
COPY scripts/test-cluster.sh /test-cluster.sh
RUN chmod +x /entrypoint.sh /healthcheck.sh /test-cluster.sh

# Ports:
# 9870: NameNode Web UI
# 9864: DataNode Web UI
# 8088: YARN ResourceManager Web UI
# 8042: YARN NodeManager Web UI
# 19888: MapReduce JobHistory Web UI
# 9000: HDFS RPC
# 22: SSH
EXPOSE 9870 9864 8088 8042 19888 9000 22

WORKDIR /home/${HADOOP_USER}

ENTRYPOINT ["/entrypoint.sh"]
