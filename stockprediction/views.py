from django.shortcuts import render, redirect
from django.urls import reverse
import yfinance as yf
import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import random
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .forms import UserForm


#tickers to randomize the index page
tickers = ['AAPL','AMZN','MSFT','GOOGL','AMD','META','NFLX','IBM','NVDA','INTC']

@login_required(login_url= 'login')
def index(request):
    #redirects user to a stock page corresponding to one of the tickers above
    return redirect(reverse("stock",kwargs={'pk':random.choice(tickers)}))

@login_required(login_url= 'login')
def stock(request,pk):
    #gets object Ticker from the ticker given in the url and gets the info and last close for it.
    stock = yf.Ticker(pk)
    close = "{:.2f}".format(stock.history(period='1d').Close.values.tolist()[0])
    #sends the current day and day corresponding to a week ago to load the plot (could be done in js)
    today = datetime.date.today().strftime('%m-%d-%Y')
    week_ago = (datetime.date.today() - datetime.timedelta(days=21)).strftime('%m-%d-%Y')
    context = { 'ticker': pk,'today': today, 'week_ago': week_ago, 'stock':stock.info, 'close':close}
    return render(request,'stocks.html',context)

@login_required(login_url= 'login')
def loadstock(request):
    #function to handle ajax request for the plot of price history
    pk = request.GET.get("ticker", None)
    start = datetime.datetime.strptime(request.GET.get("start", None), '%m-%d-%Y')
    finish = datetime.datetime.strptime(request.GET.get("finish", None), '%m-%d-%Y')
    if(start > finish):
        return JsonResponse({'error':'Finish date is sooner than start date'},status=400) 
    stock = yf.Ticker(pk)
    if stock is None:
        return JsonResponse({'error':'Ticker not found'},status=404)
    data = stock.history(start = start.strftime('%Y-%m-%d'), end = finish.strftime('%Y-%m-%d'))
    index = list(data.index.strftime('%Y-%m-%d %H'))
    print(index)
    close = data.Close.values.tolist()
    print(close)
    open = data.Open.values.tolist()
    high = data.High.values.tolist()
    low = data.Low.values.tolist()
    return JsonResponse( {pk :{'index': index, 'close': close, 'open': open,'high': high, 'low': low}}, status = 200)

@login_required(login_url= 'login')
def search(request):
    #redirects user to a stock page corresponding to the query given
    query = request.GET.get("query")
    return redirect(reverse("stock",kwargs={'pk':str(query)}))

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user= authenticate(request, username=username, password=password)
        #checks if user and password match exist in db
        if user == None:
             messages.error(request, 'Login information incorrect')
             return redirect('login')
        login(request,user)
        return redirect('index')
    context = {}
    return render(request, 'login.html',context)

@login_required(login_url='login_view')
def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account was created')
            return redirect('login')
        messages.error(request, 'Your password or user is invalid')
        return redirect('register')
    context = {'form' : form}
    return render(request, 'register.html', context)







from .forms import FeedbackForm
from .models import Feedback  # Ensure you import your Feedback model

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Create Feedback instance from form data manually
            Feedback.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                satisfaction=form.cleaned_data['satisfaction'],
                accuracy=form.cleaned_data['accuracy'],
                improvements=form.cleaned_data['improvements'],
                additional_feedback=form.cleaned_data['additional_feedback']
            )
            return redirect('index')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback_form.html', {'form': form})



from django.shortcuts import render
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, LSTM


from plotly.offline import plot
import plotly.graph_objs as go

# views.py
from django.shortcuts import render
from .forms import StockPredictionForm
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras import Sequential
from keras.layers import Dense, Embedding, LSTM
from plotly.offline import plot
import plotly.graph_objs as go

def predict_stock(request):
    if request.method == "POST":
        form = StockPredictionForm(request.POST)
        if form.is_valid():
            ticker_value = form.cleaned_data['ticker']
            number_of_days = form.cleaned_data['number_of_days']

            df = yf.download(ticker_value, period='1y', interval='1d')
            
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(df['Adj Close'].values.reshape(-1,1))

            prediction_days = 60
            x_test = []
            for x in range(prediction_days, len(scaled_data)):
                x_test.append(scaled_data[x-prediction_days:x, 0])

            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            model = Sequential([
                LSTM(units=50, return_sequences=True, input_shape=(x_test.shape[1], 1)),
                LSTM(units=50),
                Dense(units=25),
                Dense(units=1)
            ])

            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(x_test, scaled_data[prediction_days:], epochs=25, batch_size=32)

            test_data = scaled_data[-prediction_days:].reshape(1, prediction_days, 1)
            predicted_price = model.predict(test_data)
            predicted_price = scaler.inverse_transform(predicted_price)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pd.date_range(start=df.index[-1], periods=number_of_days + 1, freq='D'), y=[df['Adj Close'].iloc[-1]] + list(predicted_price.ravel()), mode='lines', name='Predicted Price'))
            plot_div = plot(fig, output_type='div', include_plotlyjs=False)

            return render(request, 'result.html', context={'plot_div': plot_div, 'ticker': ticker_value})
    else:
        form = StockPredictionForm()

    return render(request, 'predict_stock.html', {'form': form})
