from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # home route
    return render_template("home.html")

@app.route('/search/')
def search():
    # search route
    return render_template("search.html")

@app.route('/get_data', methods = ["POST"])
def get_data():
    # route to deal with form data
    # make pandas dataframe with csv data
    df = pd.read_csv('./data/patient_tb.csv')

    # remove duplicates (patient took same test on same day)
    df_new = df.drop_duplicates(subset = ["PatientID", "MostRecentTestDate", "TestName"], keep="first", inplace=False, ignore_index=True)

    # get user request from form
    query = request.form["firstName"].lower()

    results = []

    # for every value in df_new, check if PatientFirstName equals query
    # and if it does, add it to our result array
    for field in df_new:
        counter = 0
        for value in df_new[field]:
            if field == "PatientFirstName" and value.lower() == query:
                results.append([df_new["PatientID"][counter], 
                                df_new["PatientLastName"][counter]+ ", "+
                                df_new["PatientFirstName"][counter], 
                                df_new["Gender"][counter], 
                                df_new["MostRecentTestDate"][counter], 
                                df_new["TestName"][counter], 
                                df_new["MostRecentLabResult"][counter]])
            counter += 1


    # if results is empty, patient does not exist
    if not results: return render_template("search.html", data="Patient Not found")
    
    
    results.insert(0,["Patient ID", "Name (Last, First)",
                      "Gender", "Most Recent Test Date", "Test Name", "Most Recent Lab Result"])

    return render_template("search.html", data=results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)