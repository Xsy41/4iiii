import logging
import os

from flask import jsonify, make_response, session
from flask import Flask, request, render_template, send_file
from model import predict
from flask import Flask, request, redirect, url_for
from file_handler import process_uploaded_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-unique-and-secret-key'


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROCESSED_FILES_DIR = os.path.join(BASE_DIR, 'output', 'predictions')
fileName = 'predictions.csv'


@app.route('/', methods=['GET', 'POST'])
def home():
    dimensions = ['activity', 'attention', 'stars', 'technical_fork', 'participants',
                  'new_contributors', 'inactive_contributors', 'bus_factor',
                  'issues_new', 'issues_closed', 'issue_comments', 'issue_response_time', 'issue_duration',
                  'issue_age', 'code_lines_add', 'code_lines_remove', 'code_lines_sum',
                  'change_requests', 'requests_accepted', 'requests_reviews']
    return render_template('predict.html', dimensions=dimensions)


download_button_html = None


# @app.route('/upload', methods=['POST'])
# def handle_file_upload():
#     uploaded_file = request.files['file_to_process']
#     processing_result = process_uploaded_file(uploaded_file)
#
#     if processing_result:
#         processed_file_path = os.path.join(PROCESSED_FILES_DIR, fileName)
#         download_url = url_for('download_processed_file', _external=True,
#                                file_name=os.path.basename(processed_file_path))
#         download_button_html = f'<a href="{download_url}" class="download-button">Download File</a>'
#         # 直接返回下载链接和下载按钮的 HTML
#         return jsonify({"success": True, "download_url": download_url, "download_button_html": download_button_html})
#     else:
#         # 处理失败，返回错误信息
#         response = jsonify({"success": False})
#         response.status_code = 400
#         return response

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    uploaded_file = request.files['file_to_process']
    processing_result = process_uploaded_file(uploaded_file)

    if processing_result:
        processed_file_path = os.path.join(PROCESSED_FILES_DIR, fileName)
        download_url = url_for('download_processed_file', _external=True,
                               file_name=os.path.basename(processed_file_path))
        download_button_html = f'<a href="{download_url}" class="download-button">Download File</a>'
        # 直接返回下载链接和下载按钮的 HTML
        return render_template("file.html", download_url=download_url,uploaded_file=uploaded_file)
        # return jsonify({"success": True, "download_url": download_url, "download_button_html": download_button_html})
    else:
        # 处理失败，返回错误信息
        response = jsonify({"success": False})
        response.status_code = 400
        return response

@app.route('/download/<file_name>')
def download_processed_file(file_name):
    file_path = os.path.join(PROCESSED_FILES_DIR, file_name)
    return send_file(file_path, as_attachment=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    download_button_html = "<a href=\"http://127.0.0.1:5000/download/predictions.csv\" class=\"download-button\">Download File</a>"
    download_url = "http://127.0.0.1:5000/download/predictions.csv"
    success = True
    return render_template('file.html', download_button_html=download_button_html, download_url="", success=success)


@app.route('/submit', methods=['POST'])
def index():
    dimensions = ['activity', 'attention', 'stars', 'technical_fork', 'participants',
                  'new_contributors', 'inactive_contributors', 'bus_factor',
                  'issues_new', 'issues_closed', 'issue_comments', 'issue_response_time', 'issue_duration',
                  'issue_age', 'code_lines_add', 'code_lines_remove', 'code_lines_sum',
                  'change_requests', 'requests_accepted', 'requests_reviews']
    if request.method == 'POST':
        # 收集表单数据
        form_data = request.form.to_dict()
        print(form_data)
        data_array = [form_data.get(dim, '') for dim in dimensions]

        print(data_array)
        # 使用模型进行预测
        prediction = predict(data_array)

        # 返回预测结果到页面
        return render_template('predict.html', prediction=prediction, dimensions=dimensions)

    return render_template('predict.html', dimensions=dimensions)


@app.route('/next_page')
def next_page():
    # 这里可以进行一些逻辑处理，然后渲染目标页面
    return render_template('file.html')

@app.route('/index_page')
def index_page():
    # 这里可以进行一些逻辑处理，然后渲染目标页面
    dimensions = ['activity', 'attention', 'stars', 'technical_fork', 'participants',
                  'new_contributors', 'inactive_contributors', 'bus_factor',
                  'issues_new', 'issues_closed', 'issue_comments', 'issue_response_time', 'issue_duration',
                  'issue_age', 'code_lines_add', 'code_lines_remove', 'code_lines_sum',
                  'change_requests', 'requests_accepted', 'requests_reviews']
    return render_template('predict.html', dimensions=dimensions)


if __name__ == '__main__':
    app.run(debug=True)
