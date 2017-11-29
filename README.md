# MON-APIGEE

MON-APIGEE is a application to monitoring the Proxies Response Time from APIGEE.

To run the application you will need the follows variables enviroments:

    1. scl0=total_response_time
	2. scl1=target_response_time
	3. url_bgn=https://api.enterprise.apigee.com/v1/o/
	4. url_mdn=/environments/prod/stats/apiproxy?select=avg(
	5. url_end=)&realtime=true&accuracy=0&timeUnit=minute&
	6. pass_api=(token to mgnt APIGEE)
	7. delay=15 (time wait until next interation)
	8. base_db=apigee (database name)
	9. host_db=localhost (database addrress)
	10. port_db=8086 (database tcp port)
	11. org2=organization 1
	12. org1=organization 2

To configure Influxdb Database

	1. Logon on server type `influx`
	2. `CREATE DATABASE <database name>`
	3. `CREATE RETENTION POLICY ,retetion policy name> ON <database name> DURATION <time retention> REPLICATION 1 DEFAULT`



