.PHONY: help build up down restart logs ps test test-mr-python test-mr-java bash hdfs-shell jps safemode-leave hdfs-report clean

help:
	@echo "=========================================================="
	@echo "Apache Hadoop Docker - Developer Commands"
	@echo "=========================================================="
	@echo "  Cluster Lifecycle:"
	@echo "    make build           - Build the Hadoop Docker image"
	@echo "    make up              - Start the single-node Hadoop cluster"
	@echo "    make down            - Stop and remove the cluster container"
	@echo "    make restart         - Restart the Hadoop cluster"
	@echo "    make logs            - Stream container logs in real time"
	@echo "    make ps              - Check container health and status"
	@echo "    make clean           - Full teardown (removes images & volumes)"
	@echo ""
	@echo "  Testing & Validation:"
	@echo "    make test            - Run built-in HDFS & Pi MapReduce tests"
	@echo "    make test-mr-python  - Run Python Streaming MapReduce WordCount"
	@echo "    make test-mr-java    - Compile & run Java MapReduce WordCount"
	@echo ""
	@echo "  HDFS & Daemons Management:"
	@echo "    make jps             - List running Java Hadoop daemons"
	@echo "    make hdfs-report     - Display HDFS storage capacity report"
	@echo "    make safemode-leave  - Force HDFS NameNode to exit SafeMode"
	@echo "    make bash            - Open interactive root/hduser shell"
	@echo "    make hdfs-shell      - Open interactive shell as hduser"
	@echo ""
	@echo "  VirtualBox VM Management:"
	@echo "    make vm-create       - Create and configure Ubuntu Hadoop VM"
	@echo "    make vm-start        - Start the Ubuntu Hadoop VM"
	@echo "    make vm-stop         - Gracefully shutdown the VM"
	@echo "    make vm-ssh          - Connect to the VM via SSH (port 2222)"
	@echo "    make vm-status       - Check VM running status and info"
	@echo "=========================================================="

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

test:
	docker compose exec hadoop /test-cluster.sh

test-mr-python:
	bash examples/mapreduce-python/run.sh

test-mr-java:
	bash examples/mapreduce-java/compile-and-run.sh

jps:
	docker compose exec hadoop jps

safemode-leave:
	docker compose exec hadoop hdfs dfsadmin -safemode leave

hdfs-report:
	docker compose exec hadoop hdfs dfsadmin -report

bash:
	docker compose exec hadoop bash

hdfs-shell:
	docker compose exec -u hduser hadoop bash

clean:
	docker compose down -v --rmi all

vm-create:
	powershell -ExecutionPolicy Bypass -File ./scripts/virtualbox-setup.ps1

vm-start:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "Ubuntu-Hadoop" --type gui

vm-stop:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm "Ubuntu-Hadoop" acpipowerbutton

vm-ssh:
	ssh -p 2222 hadoopuser@127.0.0.1

vm-status:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo "Ubuntu-Hadoop" | findstr /i "State Memory CPUs NIC"
