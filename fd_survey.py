import pandas as pd
import re

# Load the dataset
data = pd.read_csv('DevOps Copilot Survey 18-08.csv')

new_small_medium_data = data[data['How would you categorise the size of your company'] == 'Small or Mid size company']

new_small_medium_concerns_frequency = new_small_medium_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()

print(new_small_medium_concerns_frequency)

enterprise_data = data[data['How would you categorise the size of your company'] == 'Enterprise']

enterprise_concerns_frequency = enterprise_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()

print(enterprise_concerns_frequency)

startup_data = data[data['How would you categorise the size of your company'] == 'Startup']

startup_concerns_frequency = startup_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()

print(startup_concerns_frequency)

fence_sitters_data = data[data['Are you planning to introduce generative AI tools to help your DevOps/Engineering teams?'] == 'Yes']

fence_sitters_concerns_frequency = fence_sitters_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()

print(fence_sitters_concerns_frequency)


regulation_data = data[data['Is your industry highly regulated (ex. Telco, Insurance, Medical etc.)?'] == 'yes']
regulation_concerns_frequency = regulation_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()
print(regulation_concerns_frequency)

readiness_startup = startup_data['Are you planning to introduce generative AI tools to help your DevOps/Engineering teams?'].value_counts()
print(readiness_startup)

readiness_sm = new_small_medium_data['Are you planning to introduce generative AI tools to help your DevOps/Engineering teams?'].value_counts()
print(readiness_sm)

readiness_e = enterprise_data['Are you planning to introduce generative AI tools to help your DevOps/Engineering teams?'].value_counts()
print(readiness_e)

startup_concerns_frequency = startup_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()
print(startup_concerns_frequency)

sm_concerns_frequency = new_small_medium_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()

print(sm_concerns_frequency)

enter_concerns_frequency = enterprise_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()
print(enter_concerns_frequency)

fence_sitters_data = data[data['Are you planning to introduce generative AI tools to help your DevOps/Engineering teams?'] == 'Maybe']
fs_concerns_frequency = fence_sitters_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()
print(fs_concerns_frequency)

early_adopters_data = data[data['Are you planning to introduce generative AI tools to help your DevOps/Engineering teams?'] == 'Yes']
ea_concerns_frequency = early_adopters_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()
print(ea_concerns_frequency)

regulation_data = data[data['Is your industry highly regulated (ex. Telco, Insurance, Medical etc.)?'] == 'yes']


reg_concerns_frequency = regulation_data['What are the biggest concerns regarding DevOps Copilots?'].value_counts()

print(reg_concerns_frequency)
