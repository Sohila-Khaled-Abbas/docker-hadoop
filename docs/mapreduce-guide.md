# Apache Hadoop MapReduce Guide

This guide covers developing, packaging, running, and tuning **MapReduce jobs** on your containerized Hadoop cluster using both native Java and Python Hadoop Streaming.

---

## 📑 Table of Contents

- [MapReduce Execution Model](#mapreduce-execution-model)
- [Example 1: Java MapReduce WordCount](#example-1-java-mapreduce-wordcount)
- [Example 2: Python Hadoop Streaming WordCount](#example-2-python-hadoop-streaming-wordcount)
- [Combiners and Partitioners](#combiners-and-partitioners)
- [YARN & MapReduce Memory Tuning](#yarn--mapreduce-memory-tuning)
- [Inspecting Job Logs & Metrics](#inspecting-job-logs--metrics)

---

## 🔄 MapReduce Execution Model

MapReduce processes large datasets in parallel across two distinct phases:

```text
Input Split ---> [ Map Phase ] ---> [ Shuffle & Sort ] ---> [ Reduce Phase ] ---> Output Partitions
(HDFS Blocks)      (RecordReader)      (Network / Disk)       (Aggregation)        (HDFS part-r-00000)
```

1. **Input Phase**: The `InputFormat` splits large HDFS files into logical `InputSplits` processed by individual Map tasks.
2. **Map Phase**: Transforms input key-value pairs into zero or more intermediate key-value pairs `(K1, V1) -> List(K2, V2)`.
3. **Shuffle & Sort Phase**: Hadoop groups and sorts all intermediate values sharing the same key and routes them to the designated Reducer partition.
4. **Reduce Phase**: Aggregates grouped values for each unique key `(K2, List(V2)) -> List(K3, V3)` and writes results to HDFS.

---

## ☕ Example 1: Java MapReduce WordCount

### Source Code: `WordCount.java`

```java
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString().replaceAll("[^a-zA-Z0-9 ]", " ").toLowerCase());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

### Compiling and Running Inside the Container

```bash
# 1. Copy source to container
docker compose cp examples/mapreduce-java/WordCount.java hadoop:/home/hduser/

# 2. Enter container
docker compose exec -it hadoop bash

# 3. Compile Java class with Hadoop classpath
javac -classpath $(hadoop classpath) -d . WordCount.java
jar -cvf wordcount.jar *.class

# 4. Prepare HDFS input directory
hdfs dfs -mkdir -p /input/wordcount
hdfs dfs -put /usr/local/hadoop/etc/hadoop/*.xml /input/wordcount/

# 5. Run MapReduce Job
yarn jar wordcount.jar WordCount /input/wordcount /output/wordcount-java

# 6. View Output
hdfs dfs -cat /output/wordcount-java/part-r-00000 | head -n 25
```

---

## 🐍 Example 2: Python Hadoop Streaming WordCount

Hadoop Streaming allows executing any executable or script as a Mapper and Reducer over standard I/O (`stdin` and `stdout`).

### 1. Mapper Script: `mapper.py`

```python
#!/usr/bin/env python3
import sys
import re

for line in sys.stdin:
    line = line.strip()
    words = re.findall(r'\b\w+\b', line.lower())
    for word in words:
        print(f"{word}\t1")
```

### 2. Reducer Script: `reducer.py`

```python
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        word, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        continue

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word:
    print(f"{current_word}\t{current_count}")
```

### 3. Submitting the Streaming Job

```bash
docker compose exec hadoop mapred streaming \
  -files /home/hduser/mapper.py,/home/hduser/reducer.py \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /input/wordcount \
  -output /output/wordcount-python
```

---

## ⚡ YARN & MapReduce Memory Tuning

For large datasets, you can adjust container memory and CPU limits at runtime or in `config/mapred-site.xml`:

```xml
<!-- Memory allocation for Map and Reduce tasks -->
<property>
    <name>mapreduce.map.memory.mb</name>
    <value>1024</value>
</property>
<property>
    <name>mapreduce.reduce.memory.mb</name>
    <value>2048</value>
</property>

<!-- JVM Heap Options for Map & Reduce child processes -->
<property>
    <name>mapreduce.map.java.opts</name>
    <value>-Xmx819m</value>
</property>
<property>
    <name>mapreduce.reduce.java.opts</name>
    <value>-Xmx1638m</value>
</property>
```

> [!TIP]
> Rule of Thumb: Set JVM heap (`-Xmx`) to approximately **80%** of the corresponding container memory (`mapreduce.*.memory.mb`) to leave headroom for native overhead and JVM metaspace.

---

## 📊 Inspecting Job Logs & Metrics

1. **Active Jobs**: Monitor real-time status in the YARN Web UI at [http://localhost:8088](http://localhost:8088).
2. **Completed Jobs & Counters**: Review historical execution metrics in the JobHistory Server at [http://localhost:19888](http://localhost:19888).
3. **Application Logs CLI**:
   ```bash
   docker compose exec hadoop yarn logs -applicationId <application_id>
   ```
