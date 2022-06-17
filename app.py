from flask import Flask, render_template, request, jsonify , session, redirect
from main import daily_log_returns, daily_percentage_change
from main import cumulative_daily_returns, bollinger_bands, closing_prices
from main import simple_moving_averages, volatility_info, sharpe_ratio
from main import cumulative_monthly_returns
from main import prediction


# exposes the api server on port 6900
app = Flask(__name__)

@app.route('/auth.html')
def authentication():
    return render_template('auth.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/prediction', methods=["POST"])
def get_prediction_value():

    i = request.form.get("prediction_type")
    return jsonify(data=prediction(i))



@app.route('/api', methods=["POST"])
def analysis_api_test():

    choice = request.form.get("stockList").split(",")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    analysis_type = request.form.get("analysis_type")

    if len(choice)== 0 or len(start_date)== 0 or len(end_date)== 0 or len(analysis_type) == 0 :
        return jsonify(status='missing data field')
    else:
        if analysis_type == "volatility":
            return jsonify(data= volatility_info(choice, start_date, end_date))
        elif  analysis_type == "daily percentage change":
            return jsonify(data= daily_percentage_change(choice,start_date,end_date))
        elif  analysis_type == "simple moving averages":
            return jsonify(data= simple_moving_averages(choice, start_date, end_date))
        elif analysis_type == "bollinger bands":
            return jsonify(data= bollinger_bands(choice, start_date, end_date))
        elif analysis_type == "cumulative daily returns":
            return jsonify(data= cumulative_daily_returns(choice, start_date, end_date))
        elif analysis_type == "daily log returns":
            return jsonify(data= daily_log_returns(choice, start_date, end_date))
        elif analysis_type == "sharpe ratio":
            return jsonify(data= sharpe_ratio(choice, start_date, end_date))
        elif analysis_type == "closing price":
            return jsonify(data= closing_prices(choice, start_date, end_date))
        elif analysis_type == "cumulative monthly returns":
            return jsonify(data=cumulative_monthly_returns(choice, start_date, end_date))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6900)

