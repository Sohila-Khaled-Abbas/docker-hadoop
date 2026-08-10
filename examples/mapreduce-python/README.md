# Python MapReduce with Hadoop Streaming

This example demonstrates writing and executing a MapReduce WordCount pipeline in Python 3 using Hadoop Streaming.

---

## 📁 Files

- `mapper.py`: Tokenizes input text into lowercase words and outputs `(word, 1)` pairs.
- `reducer.py`: Sums counts for identical keys emitted during the shuffle phase.
- `sample.txt`: Sample text dataset.
- `run.sh`: Automated bash script to copy files, submit the streaming job, and display output.

---

## 🚀 Running the Example

### Method 1: Automated Script (from host)
```bash
chmod +x examples/mapreduce-python/run.sh
./examples/mapreduce-python/run.sh
```

### Method 2: Manual Execution via Container Shell
```bash
# 1. Copy files into container
docker compose cp examples/mapreduce-python/ hadoop:/home/hduser/

# 2. Open container shell
docker compose exec -it hadoop bash

# 3. Create HDFS directories and upload dataset
hdfs dfs -mkdir -p /example/python/input
hdfs dfs -put /home/hduser/mapreduce-python/sample.txt /example/python/input/

# 4. Run Streaming Job
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar \
    -files /home/hduser/mapreduce-python/mapper.py,/home/hduser/mapreduce-python/reducer.py \
    -mapper "python3 /home/hduser/mapreduce-python/mapper.py" \
    -reducer "python3 /home/hduser/mapreduce-python/reducer.py" \
    -input /example/python/input/sample.txt \
    -output /example/python/output

# 5. Read output
hdfs dfs -cat /example/python/output/part-00000
```
