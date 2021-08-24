import pandas as pd
import numpy as np

data_schema = pd.read_csv('developer_survey_2020/survey_results_schema.csv', names=['key','text'], skiprows=[0])
df_schema = pd.DataFrame(data_schema, columns=['key','text'])

survey_columns = df_schema['key'].to_numpy()

data_survey = pd.read_csv('developer_survey_2020/survey_results_public.csv', names=survey_columns, skiprows=[0])
df_survey = pd.DataFrame(data_survey, columns=survey_columns)

# remove respondent
columns = np.delete(survey_columns, 0)

answers = []

for i in range(len(df_survey)):
    print(f'Processing respondent ({df_survey.iloc[i][0]})')
    for column in columns:
        raw_answer = df_survey.iloc[i][column]
        if str(raw_answer) != 'nan':
            if type(raw_answer) == str:
                answerList = raw_answer.split(';')
                for answer in answerList:
                    answers.append([int(df_survey.iloc[i]['Respondent']), column, answer])
            else:
                answers.append([int(df_survey.iloc[i]['Respondent']), column, raw_answer])
                
df_answers = pd.DataFrame(answers)
df_answers.to_csv('answers.csv', index=False)