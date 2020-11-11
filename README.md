# TEDH

## Coding

1. `main.py`
2. `daemon.py`

## Theory

3. Imagine you have more than one instance of the application, how would you solve problem with updating availability of services in database?

It really depends on the number of instances. Until we have <1_000 instances we can do vertical scaling: master(writes) - slave(reads).
But when we talk about >=1_000 instances, strategy will be different. We'll need to horizontally scale the database (sharding).

But it's much betters to use tools like Zookeeper to monitor health (availability) of services. It's a good idea to consider Event-Driven Architecture with Kafka. 

4. Imagine you have 1_000+ records in database, how would you optimize application / database? What if you have 10_000+ records? 1_000_000+?

It actually depends on the location of bottleneck. Speed of system = speed of slowest part. 
App can be scaled by using asynchronous frameworks and threads if it's IO-bound or by multiprocessing if it's CPU-bound. 

When the problem with database that has 1_000_000+ records:
1) Partition it according to the table (domain), to criteria (ip, port), region of request and so on.
2) Tune it: put indices where necessary, analyze by benchmarking tools, denormalize tables. 
