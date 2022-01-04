# ETL using Airflow with Google Cloud Platform
Tools:

    1) Google Cloud Platform (GCP)
    - Cloud Storage
    - Compute Engine
    - Dataflow
    - BigQuery
    2) Python 
    3) Docker
    4) Apache Airflow 2.2.1
    
Dataset:

    1) Search Engine Flights Tickets stored to GCS

# Setup

## Setup Google Cloud Platform (GCP)
After we succeded login into our GCP account, create our new project.

- Google Cloud Storage
1) Go to Cloud Storage
2) Create bucket, then we can upload out upload the dataset there. (*in mycase i upload folder that has already many dataset in CSV files)

![image](https://user-images.githubusercontent.com/38213112/140642927-4b0c48ee-fb6e-423a-b4d1-055d2558a4ea.png)

- Compute Engine
1) Go to Compute Engine 
2) Create new instance with,
   - Name : (Make an instance name that you want)
   - Region : asia-southeast1(Singapore)
   - Zone : asia-southeast1-b
   - Machine type : e2-standart-2 (2vCPU, 8GB memory) {*because we are using docker, we need a great memory, otherwise Airflow cannot be installed in that machine}
   - Disk size (GB): 30 GB
   - Allow HTTP and HTTPS traffic for firewall. *reference(https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
3) Go to Firewall 
4) Create a firewall rule with,
   - Name : (Make a name that you want, but i am using airflow-port)
   - Nework : default
   - Targets : All instances in the network
   - SourceIpv4 : 0.0.0.0/0
   - Specified (check)TCP : 8080
5) Go to Compute Engine, click your Instance that already created
6) Click edit, then add your "[firewall-name]" inside network tag. Example, i am adding airflow-port inside my network tag. Then save. 

![image](https://user-images.githubusercontent.com/38213112/140643746-bf9723bb-e114-4b88-935f-cb4aa1992817.png)

(*By adding firewall with port: 8080, you can access your Airflow UI later, with Ip:External Ip, example= http://34.124.227.11:8080)

## Setup Docker and Airflow
1) Go to Compute Engine, click on SSH to start a terminal
   
       sudo apt update
       sudo apt -y upgrade
       sudo apt-get install wget 
       mkdir airflow-docker
       cd airflow-docker

2) Install docker engine. *reference: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-debian-10
3) To run docker command without sudo, you need to add your user (who has root privileges) to docker group

       sudo usermod -aG docker $USER

    *To apply the new group membership, log out of the server and back in, or type the following:
    ```
    su - ${USER}
    ```
4) Install docker-compose. *reference: https://docs.docker.com/compose/install/
5) To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml(*https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

       curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'
        
6) Setting the right Airflow user        

       mkdir -p ./dags ./logs ./plugins
       echo -e "AIRFLOW_UID=$(id -u)" > .env

7) Initalizing the Airflow Environment
        
       docker-compose up airflow-init

8)  Start the services
        
       docker-compose up
        
9) Go to your Airflow UI in browser, add connection between Airflow and GCP, *reference: https://medium.com/apache-airflow/a-simple-guide-to-start-using-apache-airflow-2-on-google-cloud-1811c2127445

*optional: Go "docker pull okza/airflow-docker:1.0" to change your docker airflow image inside your .yaml file from apache/airflow:2.2.1 to okza/airflow-docker:1.0 for better configuration 

## Setup Dataflow and Bigquery

1) For Dataflow, enable Dataflow API, make a service account to allow for access and schedule data flow, google cloud storage, and write big query for later.
2) For Bigquery, create a new dataset with the same region with your cloud storage

## Objective
Find what are favourite searched keywords by customer in certain time by providing data needed by storing data from GCS to Google BigQuery

### Task 
1) Create a big table that consist of all unified files that stored in GCS (from 2018 to 2020)[GCS to BigQuery] :
   -  Upload the data inside the bucket from Google Cloud Storage
   -  Create new data set in Google Big Query(I create dataset named:  flight1)
   -  Create pipeline script (I create pipeline with apache beam then save it to flight.py)
   -  Test your pipeline script, if it success,it can make a big table from all files that stored in GCS, then you can see the dataflow. Upload it to your Cloud Storage
   -  Create a DAG with airflow that can run your pipeline script
   -  Test your Airflow DAG, then schedule it

    ![image](https://user-images.githubusercontent.com/38213112/141692888-787b4b0f-f89d-4eb8-8493-860c9922d53e.png)
    ![image](https://user-images.githubusercontent.com/38213112/141693006-535ea9e6-878e-441e-84b5-6cc98f8e3729.png)
    ![image](https://user-images.githubusercontent.com/38213112/141693216-5079409e-7352-4f0b-a6dc-dc446b9925df.png)

2) Create a table containing most searched keyword in every month(by selecting rank=1)**[BigQuery to BigQuery]** :
   - Create pipeline script (I create pipeline then save it to keysearchmonth_bq.py)
     
   Create a table that contains most searched keyword in every year(by selecting rank=1)**[BigQuery to BigQuery]** :
   - Create pipeline script (I create pipeline then save it to keysearchyear_bq.py)
   
   Create dag that can run your pipeline script(keysearchmonth_bq.py and keysearchyear_bq.py):
   
    ![image](https://user-images.githubusercontent.com/38213112/148005610-0126dcbd-3fb9-4e8f-983a-00ef506b83d5.png)
    
   Output :
   
    ![image](https://user-images.githubusercontent.com/38213112/148005676-c5089d96-8907-42c3-8d5e-3a26e49595f1.png)
    ![image](https://user-images.githubusercontent.com/38213112/148006074-e38d5f37-aef4-4e1a-986f-642e288b5a2d.png)
    ![image](https://user-images.githubusercontent.com/38213112/148006147-1dcb7869-3f08-47b8-b67e-13939dfadbff.png)

    
