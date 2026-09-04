.PHONY: help build up down restart logs ps test test-mr-python test-mr-java bash hdfs-shell jps safemode-leave hdfs-report clean vm-create vm-start vm-start-headless vm-stop vm-ssh vm-status vm-ports vm-rebuild vm-kali-optimize vm-kali-start gcp-dataproc-create gcp-dataproc-stream gcp-dataproc-java gcp-dataproc-delete gcp-gce-deploy


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
	@echo "    make vm-create       - Create and configure Ubuntu Hadoop VM (5GB RAM, 4 CPUs)"
	@echo "    make vm-start        - Start the Ubuntu Hadoop VM (GUI Window)"
	@echo "    make vm-start-headless - Start the VM in Background (Headless, saves CPU/RAM)"
	@echo "    make vm-stop         - Gracefully shutdown the VM (ACPI power button)"
	@echo "    make vm-ssh          - Connect to the VM via SSH (port 2222)"
	@echo "    make vm-status       - Check VM running status, memory, and vCPUs"
	@echo "    make vm-ports        - List active NAT port forwardings"
	@echo "    make vm-rebuild      - Teardown and cleanly recreate VM from ISO"
	@echo ""
	@echo "  VMware Workstation Kali VM Management:"
	@echo "    make vm-kali-optimize - Tune Kali VMX (6GB RAM, 4 vCPUs, disable VT-x popup)"
	@echo "    make vm-kali-start   - Launch Kali Linux in VMware Workstation"
	@echo ""
	@echo "  Google Cloud Platform (Dataproc & GCE):"
	@echo "    make gcp-dataproc-create - Provision auto-terminating Dataproc cluster"
	@echo "    make gcp-dataproc-stream - Submit Python Streaming WordCount to Dataproc"
	@echo "    make gcp-dataproc-java   - Submit Native Java MapReduce Pi to Dataproc"
	@echo "    make gcp-dataproc-delete - Teardown Dataproc cluster (stop charges)"
	@echo "    make gcp-gce-deploy      - Deploy Docker Hadoop to Google Compute Engine"
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

test-hdfs-cli:
	docker compose exec hadoop bash < examples/hdfs-cli/demo-hdfs-operations.sh

docker-start:
	cmd /c launchers\windows\Start-Hadoop-Docker.bat

docker-stop:
	cmd /c launchers\windows\Stop-Hadoop-Docker.bat

vm-create:
	powershell -ExecutionPolicy Bypass -File ./scripts/virtualbox/virtualbox-setup.ps1

vm-start:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "Ubuntu-Hadoop" --type gui

vm-start-headless:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "Ubuntu-Hadoop" --type headless

vm-stop:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm "Ubuntu-Hadoop" acpipowerbutton

vm-ssh:
	ssh -p 2222 hadoopuser@127.0.0.1

vm-status:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo "Ubuntu-Hadoop" | findstr /i "State Memory CPUs"

vm-ports:
	"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo "Ubuntu-Hadoop" | findstr /i "NIC.1.Rule"

vm-rebuild:
	powershell -ExecutionPolicy Bypass -File ./scripts/virtualbox/virtualbox-setup.ps1 -Rebuild

vm-kali-optimize:
	powershell -ExecutionPolicy Bypass -File ./scripts/vmware/optimize-kali-vmx.ps1

vm-kali-start:
	cmd /c launchers\windows\Launch-Kali-VMware.bat

gcp-dataproc-create:
	bash scripts/gcp/create-dataproc-cluster.sh

gcp-dataproc-stream:
	bash scripts/gcp/submit-mapreduce-job.sh streaming

gcp-dataproc-java:
	bash scripts/gcp/submit-mapreduce-job.sh java

gcp-dataproc-delete:
	bash scripts/gcp/teardown-dataproc-cluster.sh

gcp-gce-deploy:
	bash scripts/gcp/deploy-hadoop-gce.sh


