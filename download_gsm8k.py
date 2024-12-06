import pandas as pd

file_path = 'model_results.csv'
data = pd.read_csv(file_path)

accuracy = (data['final_result'] == data['true_label']).mean()


print(f"模型预测准确度: {accuracy * 100:.2f}%")

