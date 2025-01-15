-- 1. What are the 4 most common jobs?
SELECT COUNT(*) AS 'Count Jobs', job_title_short AS 'Job Title'
FROM job_postings_fact
GROUP BY job_title_short
ORDER BY 1 DESC
LIMIT 4;

-- 2. What are the top 5 average paying Data-Related jobs?
SELECT job_title_short, AVG(salary_year_avg) AS 'Average Yearly Salary Per Job Title'
FROM job_postings_fact
WHERE salary_year_avg IS NOT NULL
GROUP BY job_title_short
HAVING job_title_short LIKE '%Data%' OR job_title_short LIKE '%Analyst%'
ORDER BY 2 DESC
LIMIT 5;

-- 3. Which locations offered the highest salaries in 2023, and what job positions were associated with these salaries?
SELECT job_title_short AS 'Job Title', job_location AS 'City', job_country AS 'Country', salary_year_avg AS 'Average Yearly Salary'
FROM job_postings_fact
WHERE job_title_short LIKE '%Data%' OR job_title_short LIKE '%Analyst%'
ORDER BY salary_year_avg DESC
LIMIT 9;

-- 4. What skills are required for these top-paying jobs?
WITH top_jobs AS (
   SELECT job_id, job_title_short AS 'Job Title', job_location AS 'City', salary_year_avg AS 'Average Yearly Salary'
   FROM job_postings_fact
   WHERE job_title_short LIKE '%Data%' OR job_title_short LIKE '%Analyst%'
   ORDER BY salary_year_avg DESC
   LIMIT 9
),
distinct_id_job AS (
   SELECT top_jobs.*, skills, ROW_NUMBER() OVER (PARTITION BY skills,top_jobs.job_id ORDER BY top_jobs.job_id ASC) AS RowNum
   FROM top_jobs
   INNER JOIN skills_job_dim ON top_jobs.job_id = skills_job_dim.job_id
   INNER JOIN skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
)
SELECT skills, COUNT(skills) as "Count Skills"
FROM distinct_id_job
WHERE RowNum = 1
GROUP BY skills
ORDER BY 2 DESC;

-- 5. What skills are most in demand for data analysts?
SELECT skills, COUNT(DISTINCT job_postings_fact.job_id) AS 'Count Skills'
FROM skills_dim
INNER JOIN skills_job_dim ON skills_dim.skill_id = skills_job_dim.skill_id
INNER JOIN job_postings_fact ON skills_job_dim.job_id = job_postings_fact.job_id
WHERE job_title_short LIKE '%Data Analyst%'
GROUP BY skills
ORDER BY 2 DESC
Limit 5;

-- 6. Which skills are associated with higher salaries?
SELECT skills, ROUND(AVG(salary_year_avg),2) AS 'Average Salary ($)'
FROM skills_dim
INNER JOIN skills_job_dim ON skills_dim.skill_id = skills_job_dim.skill_id
INNER JOIN job_postings_fact ON skills_job_dim.job_id = job_postings_fact.job_id
WHERE job_title_short LIKE '%Data Analyst%' AND salary_year_avg IS NOT NULL
GROUP BY skills
ORDER  BY 2 DESC
LIMIT 20;

-- 7. What are the most optimal skills to learn?
SELECT skills,COUNT(skills_job_dim.skill_id), ROUND(AVG(salary_year_avg),2) AS 'Average Salary ($)'
FROM skills_dim
INNER JOIN skills_job_dim ON skills_dim.skill_id = skills_job_dim.skill_id
INNER JOIN job_postings_fact ON skills_job_dim.job_id = job_postings_fact.job_id
WHERE job_title_short LIKE '%Data Analyst%' AND salary_year_avg IS NOT NULL
GROUP BY skills
HAVING  COUNT(skills_job_dim.skill_id) > 10
ORDER BY 3 DESC
LIMIT 10;