-- ==============================================================================
-- 🐷 Apache Pig — WordCount Implementation in Pig Latin
-- ==============================================================================

-- 1. Load input text from HDFS
raw_lines = LOAD '$INPUT' USING TextLoader() AS (line:chararray);

-- 2. Transform: Extract words using TOKENIZE and FLATTEN
words = FOREACH raw_lines GENERATE FLATTEN(TOKENIZE(line)) AS word;

-- 3. Filter empty strings and punctuation
filtered_words = FILTER words BY word MATCHES '\\w+';

-- 4. Group by word
grouped_words = GROUP filtered_words BY word;

-- 5. Count occurrences
word_counts = FOREACH grouped_words GENERATE group AS word, COUNT(filtered_words) AS total_count;

-- 6. Order by frequency descending
ordered_counts = ORDER word_counts BY total_count DESC;

-- 7. Store output to HDFS
STORE ordered_counts INTO '$OUTPUT' USING PigStorage('\t');
