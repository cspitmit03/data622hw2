DATA 622 # hw2

	Assigned on September 27, 2018
	Due on October 17, 2018 11:59 PM EST
	15 points possible, worth 15% of your final grade

1. Required Reading

	Read Chapter 5 of the Deep Learning Book
	Read Chapter 1 of the Agile Data Science 2.0 textbook

2. Data Pipeline using Python (13 points total)

	Build a data pipeline in Python that downloads data using the urls given below, trains a random forest model on the training dataset using sklearn and scores the model on the test dataset.

	Scoring Rubric

	The homework will be scored based on code efficiency (hint: use functions, not stream of consciousness coding), code cleaniless, code reproducibility, and critical thinking (hint: commenting lets me know what you are thinking!)
Instructions:

	Submit the following 5 items on github.
	ReadMe.md (see "Critical Thinking")
	requirements.txt
	pull_data.py
	train_model.py
	score_model.py

More details:

requirements.txt (1 point)
This file documents all dependencies needed on top of the existing packages in the Docker Dataquest image from HW1. When called upon using pip install -r requirements.txt , this will install all python packages needed to run the .py files. (hint: use pip freeze to generate the .txt file)

pull_data.py (5 points)
When this is called using python pull_data.py in the command line, this will go to the 2 Kaggle urls provided below, authenticate using your own Kaggle sign on, pull the two datasets, and save as .csv files in the current local directory. The authentication login details (aka secrets) need to be in a hidden folder (hint: use .gitignore). There must be a data check step to ensure the data has been pulled correctly and clear commenting and documentation for each step inside the .py file.
	Training dataset url: https://www.kaggle.com/c/titanic/download/train.csv
	Scoring dataset url: https://www.kaggle.com/c/titanic/download/test.csv

#####The data was saved as train.csv and test.csv.  From here the log text file is PulledData.txt which stores all the tests.

train_model.py (5 points)
When this is called using python train_model.py in the command line, this will take in the training dataset csv, perform the necessary data cleaning and imputation, and fit a classification model to the dependent Y. There must be data check steps and clear commenting for each step inside the .py file. The output for running this file is the random forest model saved as a .pkl file in the local directory. Remember that the thought process and decision for why you chose the final model must be clearly documented in this section.
eda.ipynb (0 points)

[Optional] This supplements the commenting inside train_model.py. This is the place to provide scratch work and plots to convince me why you did certain data imputations and manipulations inside the train_model.py file.

score_model.py (2 points)
When this is called using python score_model.py in the command line, this will ingest the .pkl random forest file and apply the model to the locally saved scoring dataset csv. There must be data check steps and clear commenting for each step inside the .py file. The output for running this file is a csv file with the predicted score, as well as a png or text file output that contains the model accuracy report (e.g. sklearn's classification report or any other way of model evaluation).

3. Critical Thinking (2 points total)
Modify this ReadMe file to answer the following questions directly in place.
	1) Kaggle changes links/ file locations/login process/ file content

For this HW assignment I did not modify any gaggle links or items.  Originally, I used the API call since i thought this HW2 was a local run assignment.  However, since we are dockerizing the HW we need to use the credentials method.


	2) We run out of space on HD / local permissions issue - can't save files
At times, when data is large to work or you can't save files locally it is best to use a docker container type solution.  However, this doesn't always solve the problem.  Even if you're able to create a docker container if the user that downloads this container doesn't have the space to run all the dependencies in memory and the data files then they won't be able to run the file.  Example, this docker container is almost 2GB of temporary data needed to run due to dependencies.  


	3) Someone updated python packages and there is unintended effect (functions retired or act differently)

This can be avoided by asserting in the requirements.txt that the version of an app is installed with the one used when building the docker container.  This avoids the issue of different users having different versions of dependencies that may break the code.  Example, isna() vs isnull() calls when checking missing data.



	4) Docker issues - lost internet within docker due to some ip binding to vm or local routing issues( I guess this falls under lost internet, but I am talking more if docker is the cause rather then ISP)

Having something internet dependent would mean there is an issue with the user itself.  If there are issues with IP binding to VM or local routing issues, at times you have to check if the ports are already being used for another application or if its being used by your machine for other tasks.  In reality once the docker container is downloaded there should be no dependencies to go back to the internet and should be self contained.

Now if the app is a trading app (like going to get stocks within the python files, then it might be best to preload the data when dockerizing the app if you suspect people having issues with internet connectivity.  This means that there is a tradeoff between freshness of data vs reliability of the app.
