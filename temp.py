import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV files
skills_job_dim = pd.read_csv('skills_job_dim.csv')
skills_dim = pd.read_csv('skills_dim.csv')
job_postings_fact = pd.read_csv('job_postings_fact.csv', delimiter=";")
company_dim = pd.read_csv('company_dim.csv')

##### 1. What are the most 4 common jobs? 
df = job_postings_fact.groupby('job_title_short', as_index=False).size().rename(columns={'size': 'job_count'})
df = df.nlargest(4, 'job_count')[['job_title_short', 'job_count']]

sns.barplot(data=df, x='job_count', y='job_title_short', palette='crest')
plt.title('Top 4 most common jobs')
plt.xlabel('Job Count')
plt.ylabel('Job Title')
plt.show()


##### 2. What are the top 5 paying data analyst jobs?
f = job_postings_fact[job_postings_fact['job_title_short'].str.contains('Data|Analyst', case=False)]
df = f.groupby('job_title_short', as_index=False)['salary_year_avg'].mean()
df = df.nlargest(5, 'salary_year_avg')

sns.barplot(data=df, x='salary_year_avg', y='job_title_short', palette='crest')
plt.title('Average Salary Distribution for Top 5 Paying Data-Related Jobs')
plt.xlabel('Average Salary ($)')
plt.ylabel('Job Title')
plt.show()


##### 3. Which locations offered the highest salaries in 2023, and what job 
#positions were associated with these salaries?
df = f.nlargest(9, 'salary_year_avg')[['job_title_short','job_location','salary_year_avg']]


##### 4. What skills are required for these top-paying jobs?
df = f.nlargest(9, 'salary_year_avg')[['job_id','job_title_short','job_location','salary_year_avg']]
jobPostingsFact_skillsJobDim = df.merge(skills_job_dim, on='job_id')
jobPostingsFact_skillsJobDim__skillsDim = jobPostingsFact_skillsJobDim.merge(skills_dim, on='skill_id')
df = jobPostingsFact_skillsJobDim__skillsDim.groupby('skills', as_index=False).size().rename(columns={'size':'Count Skills'})
df = df.sort_values(by='Count Skills', ascending=False)

plt.figure(figsize=(12,8))
sns.barplot(data=df, x='Count Skills', y='skills', palette='crest')
plt.title('Top Skills by Count in Top 9 Highest-Paying Data-Related Jobs', fontsize=16)
plt.xlabel('Count of Skills', fontsize=14)
plt.ylabel('Skills', fontsize=14)
plt.tight_layout()
plt.show()


##### 5. What skills are most in demand for Data Analysts?
f = job_postings_fact[job_postings_fact['job_title_short'].str.contains('Data Analyst', case=False)]
jobPostingsFact_skillsJobDim = f.merge(skills_job_dim, on='job_id')
jobPostingsFact_skillsJobDim__skillsDim = jobPostingsFact_skillsJobDim.merge(skills_dim, on='skill_id')
df = jobPostingsFact_skillsJobDim__skillsDim.groupby('skills', as_index=False).size().rename(columns={'size':'Count Skills'})
df = df.nlargest(5,'Count Skills')


##### 6. Which skills are associated with higher salaries?
df = jobPostingsFact_skillsJobDim__skillsDim.groupby('skills', as_index=False)[['salary_year_avg']].mean()
df = df.nlargest(20,'salary_year_avg')

sns.barplot(data=df, x='salary_year_avg', y='skills', palette='crest')
plt.title('Top Skills Based on Salary for Data Analyst Job')
plt.xlabel('Average Salary ($)')
plt.ylabel('Skills')
plt.show()


##### 7. What are the most optimal skills to learn?
df = jobPostingsFact_skillsJobDim__skillsDim.groupby('skills', as_index=False)[['salary_year_avg']].agg(
    Count_Skills=('salary_year_avg', 'count'),
    Average_Salary=('salary_year_avg', 'mean')
    )
df['Average_Salary'] = df['Average_Salary'].round(2)
df = df[df['Count_Skills'] > 10]
df = df.nlargest(10,'Average_Salary')




