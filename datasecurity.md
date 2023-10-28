#### How did you secure your data in your current project.

Primary AWS services we leveraged in our datalake are : S3 , EMR and Athena.

Since we are working on financial data, we need make sure the data is  secured both "in transit" and "at rest".

**For In transit security :**
1. We made sure all our consuming and providing service endpoints are https only to enforce TLS.
2. Used VPC endpoints for private connectivity between on-prem and AWS. This will bypass the public internet and keep the traffic with AWS network.
3. Our company uses AWS Direct Connect that provided an exclusive bandwidth and provide additional security layer

**For security at rest :** Data in s3 buckets and Redshift is encrypted using Server side encryption with custom KMS keys (SSE-KMS). We basically created our own keys for the encryption.

In addition, we have following setup at the network level to protect our workloads : 
1.  Created fine grained least privilege IAM roles to access EMR and Redshift clusters.
2.  Created a brand new VPC with required ACL for all the ETL workloads including S3 buckets, Redshift/EMR clusters and Athena tables.
3.  Enabled CloudTrail for auditing and monitoring access. This allowed us to track every action taken with our data, ensuring we could identify any unauthorized or suspicious activities. 
