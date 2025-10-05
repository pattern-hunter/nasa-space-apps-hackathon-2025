import numpy as np
import pandas as pd
import dask
import dask.dataframe as dd
import dask.distributed
from dask_ml.preprocessing import StandardScaler
from dask_ml.model_selection import train_test_split
from dask_ml.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import pickle, csv
from sklearn.metrics import accuracy_score

def train_random_forest(filename):
	with open(filename, "r") as datafile:
		X, y = [], []
		csvlines = list(csv.DictReader(datafile))

		accepted_keys = []
		
		m = csvlines[0]
		for key, val in m.items():
			if key != "rowid":
				try:
					t = float(val)
					accepted_keys.append(key)
				except ValueError:
					pass

		koi_dispositions = {'CONFIRMED': 1, 'CANDIDATE': 2, 'FALSE POSITIVE': 3}
		for line in csvlines:
			x = []

			for key in accepted_keys:
				if line[key] == "":
					x.append(0.0)
				else:
					x.append(float(line[key]))
			X.append(x)
			y.append(koi_dispositions[line["koi_disposition"]])

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, shuffle=True)
		scaler = StandardScaler()
		X_train = scaler.fit_transform(X_train)
		X_test = scaler.transform(X_test)

		rf = RandomForestClassifier(n_estimators=43, max_depth=19)
		rf.fit(X_train, y_train)
		with open("model.pkl", "wb") as pklfile:
			pickle.dump(rf, pklfile)

		y_pred = rf.predict(X_test)
		accuracy = accuracy_score(y_test, y_pred)
		print(f"Accuracy: {accuracy}")

# train_random_forest("nasa_kepler_exoplanet.csv")

with open("temp_data.csv", "r") as datafile:
	X = []
	csvlines = list(csv.DictReader(datafile))
	count = 0
	for line in csvlines:
		x, row_ids = [], []
		for value in line:
			if value == "":
				x.append(0.0)
			else:
				x.append(float(value))
		X.append(x)

	print(X)