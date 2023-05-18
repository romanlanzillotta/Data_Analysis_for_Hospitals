import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', 8)
general = pd.read_csv("test/general.csv")
prenatal = pd.read_csv("test/prenatal.csv")
sports = pd.read_csv("test/sports.csv")

prenatal.rename(columns={"HOSPITAL": "hospital", "Sex": "gender"}, inplace=True)
sports.rename(columns={"Hospital": "hospital", "Male/female": "gender"}, inplace=True)

data = pd.concat([general, prenatal, sports], ignore_index=True)
data.drop(columns="Unnamed: 0", inplace=True)
sample_data = data.sample(n=20, random_state=30)

data.dropna(axis=0, how='all', inplace=True)  # remove rows with all NaNs
# wrangling gender column:
data['gender'].replace(['female', 'woman'], 'f', inplace=True)
data['gender'].replace(['man', 'male'], 'm', inplace=True)
cond = (data['gender'].isnull()) & (data['hospital'] == "prenatal")
data.loc[cond, 'gender'] = "f"
data.fillna(0, inplace=True)  # fill the rest of the columns with zeros

# questions
# 1. Which hospital has the highest number of patients?
answers = [data['hospital'].value_counts().idxmax()]
# 2. What share of the patients in the general hospital suffers from stomach-related issues?
# Round the result to the third decimal place.
a2 = data.loc[data['hospital'] == 'general', ['hospital', 'diagnosis']].groupby("diagnosis").count()\
     / data.loc[data['hospital'] == 'general', 'diagnosis'].count()
answers.append(a2.loc['stomach'][0].round(3))
# 3. What share of the patients in the sports hospital suffers from dislocation-related issues?
# Round the result to the third decimal place.
a3 = data.loc[data['hospital'] == 'sports', ['hospital', 'diagnosis']].groupby("diagnosis").count()\
     / data.loc[data['hospital'] == 'sports', 'diagnosis'].count()
answers.append(a3.loc['dislocation'][0].round(3))
# 4. What is the difference in the median ages of the patients in the general and sports hospitals?
a4 = data.groupby('hospital').agg({'age': 'median'})
answers.append(a4.loc['general'][0]-a4.loc['sports'][0].round(0))
# After data processing at the previous stages, the blood_test column has three values: t = a blood test was taken,
# f = a blood test wasn't taken, and 0 = there is no information. In which hospital the blood test was taken the most
# often (there is the biggest number of t in the blood_test column among all the hospitals)?
# How many blood tests were taken?
a5 = data[['hospital', 'blood_test']].groupby('hospital', as_index=False).value_counts()
answers.append(str(a5.loc[a5.blood_test == "t"].max()[0]) + ", " + str(a5.loc[a5.blood_test == "t"].max()[2])
               + " blood tests")
numbers = ["1st", "2nd", "3rd", "4th", "5th"]


# Visualizations
answers2 = []
data.plot(y='age', kind='hist', bins=[0, 15, 35, 55, 70, 80], edgecolor='white')
plt.show()
answers2.append("15-35")
data.diagnosis.value_counts().plot(kind='pie')
plt.show()
answers2.append("pregnancy")
sns.violinplot(data, x='hospital', y='height')
plt.show()
answers2.append("It's because general hospital states height in meters whereas the other two in feet. "
                "But sports hospital has young people whereas prenatal has babies in feet.")
[print(f"The answer to the {numbers[i]} question: {answer2}") for i, answer2 in enumerate(answers2)]
