#!/usr/bin/env python
# coding: utf-8

# <h1>Data Upload Website - created July 2020</h1>
# 
# This is a test web app that I have created which:
#     
#     (i) asks users to upload a csv file to a website 
#         - The csv file must contain  a column called 'address'
#     (ii) calculates the lat/long of the addresses provided
#     (iv) displays a dataframe containing the lat/long of the given addresses.
#     
# I am using flash for rendering the website and xxx to calculate lat/long
# 
# The webpages are named:
# 
#     (i) templates/upload.html (main page) and 
#     (ii) The css stylesheet is called static/main.css
# 
# The working app can be seen and used at:
#     bourneupload.herokuapp.com
#     
# Mike Bourne

# In[ ]:


from flask import Flask,render_template,request
import pandas as pd
from geopy.geocoders import ArcGIS
from IPython.display import HTML


#Initial the Flask appllication called 'app'
app=Flask(__name__)



#definition the main starting page of the webapp - 'upload.html'
@app.route("/")
def index():
    return render_template("upload.html")

#definition the second page of the webapp - 'success.html'
#This is where the user is sent when thy click UPLOAD on the index.html page
@app.route("/success", methods=['POST'])
def success(): 
    
    if request.method == 'POST':
        #gather the data from the upload.html page. Asign to a panda dataframe
        file = request.files['file']
        print(file)
        df = pd.read_csv(file)
        print(df)
        try:
            df = df[['Address']]

            nom=ArcGIS()

            df['Coordinates']=df['Address'].apply(nom.geocode)  
            df['Latitude']=df['Coordinates'].apply(lambda x: x.latitude)
            df['Long']=df['Coordinates'].apply(lambda x: x.longitude)
            del df['Coordinates']
            
                        
            return render_template("upload.html", 
                text_box="file uploaded - see table below" ,
                tables=[df.to_html(classes="table-bordered", header="true")] )

        except:
            return render_template("upload.html", 
            text_box="Error - no 'Address' column in csv file")            
        
    # inform user that there is an error
    else: 
        return render_template("upload.html", 
        text_box="Error - no data uploaded")

if __name__ == '__main__':
    app.debug = True
    app.run()

