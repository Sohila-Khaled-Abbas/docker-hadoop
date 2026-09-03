#!/usr/bin/env bash
set -e

echo "--> Setting up systemd service for Apache Hadoop..."

# Create helper scripts in /usr/local/bin for clean execution
cat << 'EOF' > /usr/local/bin/hadoop-cluster-start.sh
#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/home/hadoopuser/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:/usr/local/bin:/usr/bin:/bin

$HADOOP_HOME/bin/hdfs --daemon start namenode
$HADOOP_HOME/bin/hdfs --daemon start datanode
$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
$HADOOP_HOME/bin/yarn --daemon start resourcemanager
$HADOOP_HOME/bin/yarn --daemon start nodemanager
$HADOOP_HOME/bin/mapred --daemon start historyserver
EOF
chmod +x /usr/local/bin/hadoop-cluster-start.sh
chown hadoopuser:hadoopuser /usr/local/bin/hadoop-cluster-start.sh

cat << 'EOF' > /usr/local/bin/hadoop-cluster-stop.sh
#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/home/hadoopuser/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:/usr/local/bin:/usr/bin:/bin

$HADOOP_HOME/bin/mapred --daemon stop historyserver
$HADOOP_HOME/bin/yarn --daemon stop nodemanager
$HADOOP_HOME/bin/yarn --daemon stop resourcemanager
$HADOOP_HOME/bin/hdfs --daemon stop secondarynamenode
$HADOOP_HOME/bin/hdfs --daemon stop datanode
$HADOOP_HOME/bin/hdfs --daemon stop namenode
EOF
chmod +x /usr/local/bin/hadoop-cluster-stop.sh
chown hadoopuser:hadoopuser /usr/local/bin/hadoop-cluster-stop.sh

cat << 'EOF' > /etc/systemd/system/hadoop.service
[Unit]
Description=Apache Hadoop Cluster Daemons
After=network.target

[Service]
Type=forking
User=hadoopuser
Group=hadoopuser
ExecStart=/usr/local/bin/hadoop-cluster-start.sh
ExecStop=/usr/local/bin/hadoop-cluster-stop.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable hadoop
systemctl restart hadoop

echo "--> Hadoop systemd service status:"
systemctl status hadoop --no-pager
