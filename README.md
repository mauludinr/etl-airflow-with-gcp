# ETL using Airflow with Google Cloud Platform
Tools:

    1) Google Cloud Platform (GCP)
    - Cloud Storage
    - Compute Engine
    - Dataflow
    - BigQuery
    2) Python 
    3) Docker v1.29.2
    4) Docker compose 1.29.2
    5) Apache Airflow 2.2.1
    
Dataset:

    1) Search Engine Flights Tickets

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
   - Disk size (GB): 50 GB
   - Allow HTTP and HTTPS traffic for firewall. *reference(https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
3) Go to Firewall 
4) Create a firewall rule with,
   - Name : (Make a name that you want, but i am using airflow-port)
   - Nework : default
   - Targets : All instances in the network
   - SourceIpv4 : 0.0.0.0/0
   - Specified (check)TCP : 8080
5) Go to Compute Engine, click your Instance that already created
![image](https://user-images.githubusercontent.com/38213112/140643746-bf9723bb-e114-4b88-935f-cb4aa1992817.png)
6) Click edit, then add your "[firewall-name]" inside network tag. Example, i am adding airflow-port inside my network tag. Then save. (*By adding firewall with port: 8080, you can access your Airflow UI, with Ip:Externnal Ip, example= 34.124.227.11:8080)

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

4) Install docker-compose. *reference: https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-debian-10
5) To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.

        curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.1/docker-compose.yaml'
        
6) Setting the right Airflow user        

        mkdir -p ./dags ./logs ./plugins
        echo -e "AIRFLOW_UID=$(id -u)" > .env

7) Initalizing the Airflow Environment
        
        docker-compose up airflow-init

8)  Start the services
        
        docker-compose up


## 
