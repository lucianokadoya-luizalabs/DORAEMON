# MON-APIGEE

MON-APIGEE is a application to monitoring the Proxies Response Time from APIGEE.

[![Doraemon](logo.png)](https://vignette.wikia.nocookie.net/doraemon/images/0/01/1686742-tumblr_l6pwth0gox1qcp8iro1_400.png/revision/latest?cb=20140808054837&path-prefix=en)

To run the application you will need the follows variables enviroments:

    1. SCL0=total_response_time
	2. SLC1=target_response_time
	3. URL_BGN_bgn=https://api.enterprise.apigee.com/v1/o/
	4. URL_MDN=/environments/prod/stats/apiproxy?select=avg(
	5. URL_END=)&realtime=true&accuracy=0&timeUnit=minute&
	6. PASS_API=(token to mgnt APIGEE)
	7. DELAY=15 (time wait until next interation)
	8. BASE_DB=apigee (database name)
	9. HOST_DB=localhost (database addrress)
	10. PORT_DB=8086 (database tcp port)
	11. ORG2=organization 1
	12. ORG1=organization 2

To configure Influxdb Database

	1. Logon on server type `influx`
	2. `CREATE DATABASE <database name>`
	3. `CREATE RETENTION POLICY <retention policy name> ON <database name> DURATION <time retention> REPLICATION 1 DEFAULT`



