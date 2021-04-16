import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

heart_df = pd.read_csv("framingham.csv")

# age effect on CHD
print(heart_df['age'])
# plt.pie(heart_df['male'])
plt.rcParams['figure.figsize'] = [10, 15]
ax = sns.histplot(x='education', data=heart_df, hue='TenYearCHD', kde=True)

# ax = sns.countplot(x='male', hue='TenYearCHD', data=heart_df)
ax.set_title('Heart Disease Presence by Gender')
ax.set_xticklabels(['Female', 'Male'])
plt.show()

# Resting blood pressure, total cholesterol level, heart rate, age effect on 10-year chd
plt.rcParams['figure.figsize'] = [16, 4]
plt.subplot(1, 4, 1)
ax = sns.histplot(x='sysBP', data=heart_df, hue='TenYearCHD', kde=True)
ax.set_title('1. Heart disease presence by Resting Blood Pressure')
ax.set_xlabel('Resting Blood Pressure [bpm]')

plt.subplot(1, 4, 2)
ax = sns.histplot(x='totChol', data=heart_df, hue='TenYearCHD', kde=True)
ax.set_title('2. Heart disease presence by Cholesterol Level')
ax.set_xlabel('Cholestrol Level')

plt.subplot(1, 4, 3)
ax = sns.histplot(x='heartRate', data=heart_df, hue='TenYearCHD', kde=True)
ax.set_title('3. Heart disease presence by Max Heart Rate')
ax.set_xlabel('Max Heart Rate')

plt.subplot(1, 4, 4)
ax = sns.histplot(x='age', data=heart_df, hue='TenYearCHD', kde=True)
ax.set_title('4. Heart disease presence by Age')
ax.set_xlabel('Age')

plt.show()

# ------
# so now we can make conclusion that heart rate and resting blooad pressure don't make any sence and we shouldn't use
# for our classifier
# ------

# i think we shouldn't analys education correlation)

# currentSmoker stat is useless because we have cigsPerDay stat, that show us this fact(0 - is not smoker)
plt.rcParams['figure.figsize'] = [10, 15]
ax = sns.histplot(x='cigsPerDay', data=heart_df, hue='TenYearCHD', kde=True)

ax.set_title('Heart Disease Presence by Cigs')
# ax.set_xticklabels(['Female', 'Male'])

plt.show()

# we can see some depend and turn it in classifier
