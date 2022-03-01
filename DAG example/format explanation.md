## DAG file format explanation

- R : Number of Resources
- M : Number of Resources Processors
- ’T’ row consists of the following columns:
    1) ’T’
    2) a unique numeric ID
    3) the period (in milliseconds)
    4) the relative deadline

- ‘V’ row consists for the following columns (unbounded number):
	1) ‘V’
	2) task ID to which it belongs
	3) a numeric vertex ID (unique w.r.t. its task)
	4) earliest release time r^min (relative to start of period, may be zero)
	5) latest release time r^max (relative to start of period)
	6) BCET
	7) WCET
	8) first predecessor (vertex ID), if any
	9)  second predecessor (vertex ID), if any
	10) third predecessor (vertex ID), if any
	… and so on … 