from flask import Flask, render_template #pip3 install flask
from database import storage
import json
import datetime
app = Flask(__name__)

conn = storage.connect()
cursor = conn.cursor()


@app.route("/")
def home():
    cursor.execute("SELECT DATE_FORMAT(DATE_ADD('01-01-01', INTERVAL (month-1) MONTH), '%b') AS MONTHNAME, MONTH, COUNT(*) AS flightNumbe FROM flights GROUP BY month") # some SQL command
    flightDetail = cursor.fetchall()  # cursor.fetchall() contains the response from the SQL server
    months = []
    flights = []
    for flight in flightDetail:
        months.append(flight[0])
        flights.append(flight[2])
    return render_template('home.html', title='Total number of flights per month', labels=months, values=flights)


@app.route('/part2')
def part2():
    cursor.execute("SELECT DATE_FORMAT(DATE_ADD('01-01-01', INTERVAL (month-1) MONTH), '%b') AS MONTHNAME,  month, origin,COUNT(*) AS flightNumber FROM flights GROUP BY month, origin ORDER BY month ASC") # some SQL command
    flightDetail=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    months = []
    flight1 = []
    flight2 = []
    flight3 = []
    for flight in flightDetail:
        if (flight[2]) == "EWR":
            flight1.append(flight[3])
            months.append(flight[0])
        elif (flight[2]) == "JFK":
            flight2.append(flight[3])
        else:
            flight3.append(flight[3])
    return render_template('part2.html', title='Total number of flights per month from the three origins Frequency, Frequency stacked', labels=months, values1=flight1, values2=flight2, values3=flight3)


@app.route('/part2b')
def part2b():
    cursor.execute("SELECT DATE_FORMAT(DATE_ADD('01-01-01', INTERVAL (month-1) MONTH), '%b') AS MONTHNAME,  month, origin,COUNT(*) AS flightNumber FROM flights GROUP BY month, origin ORDER BY month ASC") # some SQL command
    flightDetail=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    months = []
    flight1 = []
    flight2 = []
    flight3 = []
    newlist= []
    for flight in flightDetail:
        if (flight[2]) == "EWR":
            flight1.append(flight[3])
            months.append(flight[0])
        elif (flight[2]) == "JFK":
            flight2.append(flight[3])
        else:
            flight3.append(flight[3])
    for m, f1, f2, f3 in zip(months, flight1, flight2, flight3):
        newlist.append({"category": m, 'value1': f1, 'value2': f2, 'value3': f3 })  
    return render_template('part2b.html', title='Total number of flights per month from the three origins Frequency stacked 100%', data1=newlist, labels=months, values1=flight1, values2=flight2, values3=flight3)


@app.route('/part3')
def part3():
    cursor.execute("SELECT dest,COUNT(*) AS flightNumber FROM flights GROUP BY dest ORDER BY flightNumber DESC LIMIT 10") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part3.html', title='The top-10 destinations and how many flights',flightDetails=flightDetails)    


@app.route('/part4')
def part4():
    cursor.execute("SELECT avg(cast(air_time AS SIGNED)) AS mean, origin   FROM flights WHERE air_time  <> 'NA' GROUP BY origin") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part4.html', title='The mean airtime of each of the origins',flightDetails=flightDetails) 


@app.route('/part4b')
def part4b():
    cursor.execute("SELECT * FROM (SELECT  count(flight) as numberOfFlights , a.dest from flights AS a group by  dest order by numberOfFlights DESC LIMIT 10) AS a  JOIN (select count(flight) as numberOfFlights, origin, dest from flights where origin = 'EWR' group by origin, dest order by numberOfFlights DESC LIMIT 10) as b ON a.dest = b.dest left JOIN (select count(flight) as numberOfFlights, origin, dest from flights where origin = 'LGA' group by origin, dest order by numberOfFlights DESC LIMIT 10) as c ON c.dest = a.dest left JOIN (select count(flight) as numberOfFlights, origin, dest from flights where origin = 'JFK' group by origin, dest order by numberOfFlights DESC LIMIT 10) as d ON d.dest = a.dest order by a.numberOfFlights DESC") # some SQL command
    flightDetail=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    dest = []
    flight1 = []
    flight2 = []
    flight3 = []
    for flight in flightDetail:
            flight1.append(flight[2])
            dest.append(flight[4])
            flight2.append(flight[5])
            flight3.append(flight[8])
    return render_template('part4b.html', title='make a visualization of the number of flights from the three origins to the top-10 destination', 
    labels=dest, values1=flight1, values2=flight2, values3=flight3)


@app.route('/part5')
def part5():
    cursor.execute("SELECT COUNT(*), origin FROM weather GROUP BY origin") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part5.html', title='How many weather observations there are for the origins',flightDetails=flightDetails)


@app.route('/part6')
def part6():
    cursor.execute("select cast(time_hour as datetime) as date, (CAST(temp AS signed) *9/5  + 32) AS tempInC,origin FROM weather WHERE temp  <> 'NA' order by time_hour") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    months = []
    temp1 = []
    temp2 = []
    temp3 = []
    newlist1=[]
    newlist2=[]
    newlist3=[]
    for weather in flightDetails:
        if (weather[2]) == "EWR":
            temp1.append(float(weather[1]))
            months.append(json.dumps(weather[0], default=default))
        elif (weather[2]) == "JFK":
           temp2.append(float(weather[1]))
        else:
            temp3.append(float(weather[1]))
    for m, t1 in zip(months, temp1):
        newlist1.append({'x': m, 'y': t1})
    data1 = str(newlist1).replace('\'', '')
    for m1, t2 in zip(months, temp2):
            newlist2.append({'x': m1, 'y': t2})
    data2 = str(newlist2).replace('\'', '')
    for m2, t3 in zip(months, temp3):
            newlist3.append({'x': m2, 'y': t3})
    data3 = str(newlist3).replace('\'', '')

    return render_template('part6.html', 
    title='For each of the three origins, all temperature attributes in degree Fahrenheit (i.e. you need to convert from  Celsius to Fahrenheit', 
    data1=data1, data2=data2, data3=data3) 


@app.route('/part7')
def part7():
    cursor.execute("select cast(time_hour as datetime) as date, (CAST(temp AS signed) *9/5  + 32) AS tempInC,origin FROM weather WHERE temp  <> 'NA' and origin='JFK' order by time_hour") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    months = []
    temp1 = []
    newlist1=[]
    for weather in flightDetails:
        temp1.append(float(weather[1]))
        months.append(json.dumps(weather[0], default=default))
    for m, t1 in zip(months, temp1):
        newlist1.append({'x': m, 'y': t1})
    data1 = str(newlist1).replace('\'', '')
    
    return render_template('part7.html', 
    title='The temperature (in Fahrenheit) at JFK', 
    data1=data1)  


@app.route('/part8')
def part8():
    cursor.execute("select year, month, day, origin, AVG((CAST(temp AS signed) *9/5  + 32)) AS meanTemp FROM weather WHERE temp  <> 'NA' and origin='JFK' GROUP BY year, month, day, origin order by month, day") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    months = []
    temp1 = []
    newlist1=[]
    for weather in flightDetails:
            temp1.append(float(weather[4]))
            months.append(datetime.datetime(weather[0],weather[1],weather[2],0,0,0))
    for m, t1 in zip(months, temp1):
        newlist1.append({'x': json.dumps(m,default=default), 'y': t1})
    data1 = str(newlist1).replace('\'', '')

    return render_template('part8.html', 
    title='The daily mean temperature (in Fahrenheit) at JFK', 
    data1=data1) 


@app.route('/part9')
def part9():
    cursor.execute("select year, month, day, origin, AVG((CAST(temp AS signed) *9/5  + 32)) AS meanTemp FROM weather WHERE temp  <> 'NA' GROUP BY year, month, day, origin order by month, day") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    months = []
    temp1 = []
    temp2 = []
    temp3 = []
    newlist1=[]
    newlist2=[]
    newlist3=[]
    for weather in flightDetails:
        if (weather[3]) == "EWR":
            temp1.append(float(weather[4]))
            months.append(datetime.datetime(weather[0],weather[1],weather[2],0,0,0))
        elif (weather[3]) == "JFK":
            temp2.append(float(weather[4]))
        else:
            temp3.append(float(weather[4]))
    for m, t1 in zip(months, temp1):
        newlist1.append({'x': json.dumps(m,default=default), 'y': t1})
    data1 = str(newlist1).replace('\'', '')
    for m1, t2 in zip(months, temp2):
        newlist2.append({'x': json.dumps(m1,default=default), 'y': t2})
    data2 = str(newlist2).replace('\'', '')
    for m2, t3 in zip(months, temp3):
        newlist3.append({'x': json.dumps(m2,default=default), 'y': t3})
    data3 = str(newlist3).replace('\'', '')
    
    return render_template('part9.html', 
    title='The daily mean temperature (in Fahrenheit) for each origin', 
    data1=data1, data2=data2, data3=data3)


@app.route('/part10')
def part10():
    cursor.execute("SELECT AVG(CAST(dep_delay AS signed)) AS meanDepDelay, AVG(CAST(arr_delay AS signed)) AS meanArrDelay,origin FROM flights WHERE dep_delay  <> 'NA' AND arr_delay  <> 'NA' GROUP BY origin") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part10.html', title='Mean departure and arrival delay for each origin',flightDetails=flightDetails)     


@app.route('/part11')
def part11():
    cursor.execute("SELECT manufacturer,count(tailnum) as numberOfPlanes FROM planes GROUP BY manufacturer  HAVING count(tailnum) > 200 ORDER BY numberOfPlanes DESC") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part11.html', title='The manufacturers that have more than 200 planes',flightDetails=flightDetails)     


@app.route('/part12')
def part12():
    cursor.execute("SELECT  a.manufacturer, COUNT(b.flight) AS number_of_flights FROM planes AS a INNER JOIN flights AS b ON a.tailnum = b.tailnum INNER JOIN (SELECT manufacturer,COUNT(tailnum) AS numberOfPlanes FROM planes GROUP BY manufacturer  HAVING count(tailnum) > 200 ) as d ON a.manufacturer = d.manufacturer GROUP BY a.manufacturer ORDER BY number_of_flights DESC") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part12.html', title='The number of flights each manufacturer with more than 200 planes',flightDetails=flightDetails)  


@app.route('/part13')
def part13():
    cursor.execute("SELECT  model, COUNT(tailnum) AS number_of_planes FROM planes WHERE manufacturer = 'AIRBUS'  GROUP BY model") # some SQL command
    flightDetails=cursor.fetchall()  #cursor.fetchall() contains the response from the SQL server
    return render_template('part13.html', title='The number of planes of each Airbus Model',flightDetails=flightDetails)


def default(obj): #Serialize the data
        """Default JSON serializer."""
        import calendar, datetime
        if isinstance(obj, datetime.date):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
            millis = int(
                calendar.timegm(obj.timetuple()) * 1000 +
                obj.microsecond / 1000
            )
            return millis
        raise TypeError('Not sure how to serialize %s' % (obj,)) 


if __name__ == "__main__" :
    app.run( host='127.0.0.1', port=5000, debug=False)