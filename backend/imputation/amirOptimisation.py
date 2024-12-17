import numpy as np
import numbers as nb
from mealpy import FloatVar, SCA, SHIO, WHO
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
import asyncio
from .consumers import connected_clients

async def broadcast_accuracy(accuracy):
    for client in connected_clients:
        await client.send_accuracy(accuracy)

async def broadcast_f1_score(f1_score):
    for client in connected_clients:
        await client.send_f1_score(f1_score)

def sca_func(data, testingset, epoch, popsize, method="SCA"):
  scaler = StandardScaler()

  features = data[:, 0:9]
  target = data[:, 9]

  scaler.fit(features)
  features = scaler.transform(features)

  accuracies = []
  f1_scores = []

  nan_indices = np.array([
      (row, col)  # Tuple of (row, column) indices
      for col in range(features.shape[1])
      for row in np.argwhere(np.isnan(features[:, col])).flatten()
  ])


  nan_n = np.sum(np.isnan(features)) 

  nan_mask = ~np.isnan(features).any(axis=1)
  features_without_nan = features[nan_mask].copy()

  lb = (np.min(features_without_nan), ) * nan_n
  ub = (np.max(features_without_nan), ) * nan_n

  original_indices_of_without_nan = np.where(nan_mask)[0]
  original_indices_of_nan = np.where(~nan_mask)[0]

  features_without_nan = features[original_indices_of_without_nan,:]
  target_without_nan = target[original_indices_of_without_nan]

  X_train, X_test, y_train, y_test = train_test_split(
      features_without_nan, target_without_nan, test_size=testingset, random_state=42
  )

  knn = KNeighborsClassifier(n_neighbors=5)
  knn.fit(X_train, y_train)

  def objective_function(solution):
      for k, (row, col) in enumerate(nan_indices):
          features[row, col] = solution[k]

      X_test_solution = np.concatenate((features[original_indices_of_nan, :], X_test), axis=0)
      y_test_solution = np.concatenate((target[original_indices_of_nan], y_test), axis=0)

      y_pred = knn.predict(X_test_solution)

      acc = accuracy_score(y_test_solution, y_pred)
      f1 = f1_score(y_test_solution, y_pred)

      if(len(accuracies) == 0 or max(accuracies) < acc):
          accuracies.append(acc)
          asyncio.run(broadcast_accuracy({len(accuracies): acc}))
      
      if(len(f1_scores) == 0 or max(f1_scores) < f1):
          f1_scores.append(f1)
          asyncio.run(broadcast_f1_score({len(f1_scores): f1}))
          

      fitness = 1 - acc
      return fitness

  problem_dict = {
      "bounds": FloatVar(lb=lb, ub=ub, name="delta"),
      "minmax": "min",
      "obj_func": objective_function
  }

  print('Method: ', method)
  if(method=="SCA"): 
    print('SCA')
    model = SCA.DevSCA(epoch=epoch, pop_size=popsize)
    
  if(method=="SHIO"):
    print('SHIO')
    model = SHIO.OriginalSHIO(epoch=epoch, pop_size=popsize)

  g_best = model.solve(problem_dict)

  print(f"Solution: {g_best.solution}, Fitness: {g_best.target.fitness}")
  print(f"Solution: {model.g_best.solution}, Fitness: {model.g_best.target.fitness}")

  return {i + 1: value for i, value in enumerate(accuracies)}  
