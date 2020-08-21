# Environment
1. `pip install -r requirements.txt` to install all packages required for this project.

# Dataset

## User-Song Dataset
1. Navigate [here](http://millionsongdataset.com/tasteprofile/)
2. Under <b>Getting the Dataset</b>, click on the hyperlink for <i>TRIPLETS FOR 1M USERS</i>

## Song-Feature Dataset
1. Navigate [here](https://aws.amazon.com/datasets/million-song-dataset/) for the Amazon Public Dataset Snapshot
2. Create an AWS EC2 instance with at least 16GB of RAM. More info [here](https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html)
3. Create an EBS volume from the snapshot in Step 1. More info to do so [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-restoring-volume.html)
4. Attach the EBS volume to your EC2 instance. More info to do so [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-attaching-volume.html)
5. Connect to your instance using SSH and mount the EBS volume. More info to do so [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html)
6. Move `hdf5_getters.py`, `get_data.py`, `userSongs.p` (inside data directory) to the EC2 instance using the format: `scp -i <location of .pem file> get_data.py  ec2-user@<public-dns>.compute-1.amazonaws.com:~`
7. Run `get_data.py` inside the EC2 instance
8. Copy over `output_usersong_features.csv` onto local using `scp -i <location of .pem file> ec2-user@<public-dns>.compute-1.amazonaws.com:~/output_usersong_features.csv ~/output_usersong_features.csv`

# Experiment
## Data Analysis
The jupyter notebook, `data_analysis_ms.ipynb` contains the code and work done for data analysis.

## Collaborative Filtering
The jupyter notebook, `collaborative-filtering-millionsongs.ipynb` contains the code and work done for collaborative filtering.

## Content-based Filtering
The jupyter notebook, `ContentBasedNearestNeighbors_millionsongs.ipynb` contains the code and work done for content-based filtering.

## Hybrid Filtering
The jupyter notebook, `hybrid_recommender.ipynb` contains the experiments regarding the hybrid model. The python file `hybrid_recommender.py` contains the implementation of the hybrid model.
