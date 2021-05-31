# %%
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
import pandas as pd

osoby = 'Alex, Alfred, Anita, Anne, Bernard, Bill, Charles, Claire, David, Eric, Frans, George, Herman, Joe, Maria, Max, Paul, Peter, Philip, Richard, Robert, Sam, Susan, Tom'.split(', ')


df = pd.read_csv('pytania.csv')
df['pytanie'] = df['nazwa'] + '_' + df['wartosc'].astype(str)
# %%
pytania = df[osoby].transpose().reset_index().rename(columns=dict(df['pytanie']))
# %%
features = [i for i in pytania.columns if i != 'index']
y_train = pytania['index']
x_train = pytania[features]

# %%
tree = DecisionTreeClassifier(criterion='entropy')
tree = tree.fit(x_train, y_train)
tree.predict(x_train) == y_train

# %% 
from sklearn.tree import plot_tree
_ = plot_tree(tree, feature_names=features)
# %%
