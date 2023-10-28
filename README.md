### Redshift Performance Optimisation with an example: 
Redshift's columnar storage is different from traditional RDBMS systems. We had to fine-tune our table designs, distribution styles, and sort keys to ensure optimal performance. This required several iterations and performance benchmarking on our recent migration project.

I can explain this with a simple example on the challenges we faced in migrating a huge transaction table from onprem RDBMS to Redshift.  This Transaction table was heavily accessed and was growing rapidly, given the nature of our business.

> (***Have your own fields here applicable for your project***)

#### Original Structure (On-Premises RDBMS):
1. TransactionID (Primary Key)\
2. AccountNumber
3. TransactionDate
4. TransactionType (e.g., Credit, Debit)
5. Amount
6. MerchantID
7. Other transaction-related columns...

After migrating this table to Redshift, we observed a lot of performance issue in the application and root cause analysis pointed to the perforance issues with this Transcation table. We faced a lot of challenges in terms of query performance, especially when running aggregate queries or joining with other tables. this negatively impacted the whole application performance because this is the primary table of our application and used in most places.

Here's how we tackled this situation:

1. **Distribution Style:**
Distribution styles dictate how data is distributed across the nodes and slices of a distributed database system like Amazon Redshift.

Given that many queries involved filtering or joining on AccountNumber, we chose to use a KEY distribution style on this column. This ensured that all data for a specific account was co-located on a single node, reducing data shuffling during joins.

For other tables which does not usually included in joins, we used Even (or Round Robin) Distribution. This   will  distribute data  across the nodes in a round-robin fashion, without regard to the values in any specific column. 

2. **Sort Key:**
Most of our analytics queries were time-bound, looking at transactions over specific date ranges. Hence, we chose TransactionDate as our sort key. This ensured that data blocks on disk were organized by date, making range queries much faster.

3. **Columnar Storage Benefits:**
Redshift's columnar storage meant that I/O was reduced during data retrieval, as only the necessary columns are read from disk. We educated our analysts and data scientists about this benefit so that they could optimize their SELECT statements to query only the necessary columns.

4. **Compression Encodings:**
Redshift allows specifying compression encodings for each column. Chosing the right compression encoding will not only saves storage space but also boosts query performance. Given the nature of our data, we used LZO encoding for TransactionDate since it had many repeating values on a given day. For other columns with a more diverse set of values, like Amount, we tested different encodings to find the optimal one.

Other popular encodings : 
**Run-Length Encoding (RLE)** : Best for columns with long sequences of repeated values.
**Delta Encoding** : Best for Monotonically increasing columns, like timestamps or auto-incremented IDs.
**Dictionary Encoding** : Best for Columns with a limited set of distinct values, especially strings.

5. **Vacuuming and Analyzing:**
Over time, as data gets updated or deleted, the organization of data blocks can get fragmented. We set up regular maintenance windows to perform VACUUM operations and maintain performance. Additionally, we ran the ANALYZE command periodically to update statistics, which helps the Redshift query planner.

**Outcome:**
By carefully choosing our distribution and sort keys, and optimizing other table design aspects, we achieved a significant performance boost in our Redshift queries. Aggregate queries that used to run in several minutes on our on-premises system were now completing in seconds, greatly enhancing our financial reporting capabilities.
