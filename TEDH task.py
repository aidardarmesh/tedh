"""

You have database schema

postgres=# \d services
                                   Table "public.services"
  Column   |       Type        | Collation | Nullable |               Default
-----------+-------------------+-----------+----------+--------------------------------------
 id        | integer           |           | not null | nextval('services_id_seq'::regclass)
 ip        | character varying |           | not null |
 port      | integer           |           | not null |
 available | boolean           |           | not null |
Indexes:
    "services_pkey" PRIMARY KEY, btree (id)

With records

postgres=# select * from services;
 id |     ip      | port  | available
----+-------------+-------+-----------
  1 | 127.0.0.1   | 44444 | t
  2 | 127.0.0.1   | 55555 | f
  3 | 127.0.0.1   | 33333 | t
  4 | 127.0.0.1   | 22222 | t
  5 | 127.0.0.1   | 11111 | t
  6 | 172.16.0.15 | 22222 | f
  7 | 172.16.0.15 | 33333 | f
(7 rows)

"""

# entity example
# [
#  {'available': True, 'ip': '127.0.0.1', 'port': 44444},
#  {'available': False, 'ip': '127.0.0.1', 'port': 55555},
#  {'available': True, 'ip': '127.0.0.1', 'port': 11111}
#  {'available': True, 'ip': '127.0.0.1', 'port': 22222}
#  {'available': True, 'ip': '127.0.0.1', 'port': 33333}
# ]

# 1)
# Design a CRD application (no ability to update entity, only Create, Read and Delete)
# Get operation(s) should support the ability to fetch all records by provided ip, with optional port
# Validation rules: ip only ipv4, port in range 1024-65535
# API should accept/return only application/json
#
# 2)
# Create a background task that updates state of the service (setting available flag in database) every 30 second
# just check that port is open/closed (timeouts!)
#
# Theoretical questions (no need to write code for this part)
#
# 3)
# Imagine you have more than one instance of the application, how would you solve problem with updating availability of services in database?
#
# 4)
# Imagine you have 1_000+ records in database, how would you optimize application / database? What if you have 10_000+ records? 1_000_000+?
#
# Requirements
# * use aiohttp with asyncpg
# * follow pep8
# * we use python 3.6+ with type hints
# * write everything in one file
# * use plain selects from database right in the handlers (that's ok for that task :)

