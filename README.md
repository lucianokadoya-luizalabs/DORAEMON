# Doraemon

Doraemon is a application to monitoring the Proxies Response Time from APIGEE.

<p align="center">
  <img width="500px" src="Doraemon.png" alt='Doraemon'>
</p>


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

To install Grafana on Debian

	- Add the following line to your /etc/apt/sources.list file.

	deb https://packagecloud.io/grafana/stable/debian/ jessie main
	Use the above line even if you are on Ubuntu or another Debian version. There is also a testing repository if you want beta or release candidates.

	deb https://packagecloud.io/grafana/testing/debian/ jessie main
	Then add the Package Cloud key. This allows you to install signed packages.

	curl https://packagecloud.io/gpg.key | sudo apt-key add -
	Update your Apt repositories and install Grafana

		sudo apt-get update
		sudo apt-get install grafana

	- On some older versions of Ubuntu and Debian you may need to install the apt-transport-https package which is needed to fetch packages over HTTPS.

		sudo apt-get install -y apt-transport-https

To configure Influxdb Database

	- Logon on server type `influx`
		CREATE DATABASE <database name>
		CREATE RETENTION POLICY <retention policy name> ON <database name> DURATION <time retention> REPLICATION 1 DEFAULT



