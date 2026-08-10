# Native Java MapReduce WordCount

This example contains a standalone, well-structured Java MapReduce implementation of WordCount, with full compilation and execution scripts.

---

## 📁 Files

- `WordCount.java`: Java source code with `TokenizerMapper`, `IntSumReducer`, and Driver configuration with Combiner optimization.
- `compile-and-run.sh`: Automated compilation against `$(hadoop classpath)`, packaging into a JAR, and execution on YARN.

---

## 🚀 Running the Example

### Automated Execution (from Host)
```bash
chmod +x examples/mapreduce-java/compile-and-run.sh
./examples/mapreduce-java/compile-and-run.sh
```

### Manual Compilation Inside Container
```bash
docker compose exec -it hadoop bash

# Compile
javac -classpath $(hadoop classpath) -d . WordCount.java
jar -cvf wordcount.jar *.class

# Run on YARN
yarn jar wordcount.jar WordCount /example/java/input /example/java/output
```
