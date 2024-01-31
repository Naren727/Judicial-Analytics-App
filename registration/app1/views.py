from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from joblib import load
import pandas as pd
import numpy as np

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    if request.method =='POST':
         p1 = request.POST.get('parameter 1')
         p2 = request.POST.get('parameter 2')
         p3 = request.POST.get('parameter 3')
         p4 = request.POST.get('parameter 4')
         p5 = request.POST.get('parameter 5')
         new_data = [p1,p2,p3,p4,p5]
         
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your entered password and confirmed password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def ResultPage(request):
        predictions = getResults()
        # Print the predictions
        context = {"predictions": int(predictions[0])}
        print(predictions)

        return render(request, 'result.html',context)

def LogoutPage(request):
    logout(request)
    return redirect('login')

def getResults():
        loaded_model = load('Judicial_Data_RFmodel.pkl')
        columns = {'state_code': int,'judge_position': float,'type_name': float,'purpose_name': float,'disp_name': int
        }

        # Create an empty DataFrame with the specified columns
        new_df = pd.DataFrame(columns=columns.keys())

        no_rows = 1
        # Generate random data for each column
        random_state_codes = np.random.randint(0, 100,size=no_rows)
        random_judge_positions = float(np.random.randint(0, 100,size=no_rows))
        random_type_names = float(np.random.randint(0, 100,size=no_rows))
        random_purpose_names = float(np.random.randint(0, 100,size=no_rows))
        random_disp_names = np.random.randint(0, 100,size=no_rows)

        # Add the random data to the DataFrame
        new_df['state_code'] = random_state_codes
        new_df['judge_position'] = random_judge_positions
        new_df['type_name'] = random_type_names
        new_df['purpose_name'] = random_purpose_names
        new_df['disp_name'] = random_disp_names

        predictions = loaded_model.predict(new_df)
        return predictions
