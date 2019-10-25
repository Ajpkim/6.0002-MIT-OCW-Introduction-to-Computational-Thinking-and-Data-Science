# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Alex Kim
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
#                Raw data composed of cities at highest layer
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
#                Within cities is yearly data
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
#               Within yearly data is monthly data....
                self.rawdata[city][year][month] = {}
#                Within monthly data is actual daily temperature data
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

# Lots of data scaffolding

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    
    for d in degs:
        m = pylab.polyfit(x, y, d)
        models.append(m)
        
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    
#   1 - predicted errors / variability
    estimated_error = ((y - estimated)**2).sum()
    mean_error = estimated_error / len(y)
    rsq = 1 - (mean_error / pylab.var(y))
    
    return rsq
    
## Implementation strictly to the standard formula:
#    ee = ((y - estimated)**2).sum()
#    variability = ((y - pylab.mean(y))**2).sum()
#    rsq = 1 - (ee / variability)
#    
#    return rsq


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    

    def plot(x, y, estimates, rsq, degree, model):
        pylab.figure()
        if degree == 1:
#           Need to include SE/slope for degree 1 models   
            SE_over_slope = se_over_slope(x, y, estimates, model)   
            pylab.title('Degree ' + str(degree) + ' linear regression model:' + '\n'
                        'r-squared = ' + str(round(rsq, 4)) + ', SE/slope = ' + str(round(SE_over_slope, 4)))
        else:
            pylab.title('Degree ' + str(degree) + ' linear regression model:' + '\n'
                        'r-squared = ' + str(round(rsq, 4)))
        
        pylab.xlabel('Date')
        pylab.ylabel('Temperature (C)')
        pylab.plot(x, y, 'bo', label = 'Training Data')
        pylab.plot(x, estimates, 'r', label = 'Model')
        pylab.legend(loc = 'best')
        
        
    for model in models:
#        Define variables for model, will pass to plot function
        degree = len(model) - 1
        estimates = pylab.polyval(model, x)
        rsq = r_squared(y, estimates)
#        Create plot for each model
        plot(x, y, estimates, rsq, degree, model)
        

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    
#    Need to return an array of yearly avgs across cities
#    Going to create an array for each city of len years and calc the avgs for each city
#    Add all these city yearly avgs together in yearly tots avgs array
#    Then get the yearly multi cities avg by dividing yearly tots avgs array by len multi cities


#    Initialize array to hold sums of the yearly avgs for all cities 
    yearly_total_avgs = pylab.array(0.0) * range(len(years))
    
#    Add the yearly avgs for each city to the yearly_total_avgs array
    for city in multi_cities:
        
        city_yearly_avgs = []
    
        for year in years:

            city_yearly_avgs.append(pylab.mean(climate.get_yearly_temp(city, year)))
            
        yearly_total_avgs += pylab.array(city_yearly_avgs)
        
#      return yearly avgs across all cities  
    return yearly_total_avgs / len(multi_cities)
    

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    
    moving_avgs = []
            
    for e in range(len(y)):
        
        moving_average = 0
        divide_by = 0
        
        for i in range(window_length):
            
            if e - i >= 0:
            
                moving_average += y[e - i]
                divide_by += 1
                
        moving_average /= divide_by
        
        moving_avgs.append(moving_average)
        
    return pylab.array(moving_avgs)
        
### Testing:
#y = pylab.array([1,2,3,4,5])
#window_length = 2
#print(moving_average(y, window_length))
    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    
    EE = ((y - estimated)**2).sum()
    return (EE / len(y))**0.5


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
#    For each year create array to hold the sum of the temperatures for all cities in given year
#    Loop through each city and add the daily temperatures from the city for the year to the array
#    Divide this tot_year_data array by len(multi_cities) to get the yearly average
#    Take the std of this tot_year_data array and add that value to the std_devs list
#    convert stds to array and return value
    
    stdevs = []

    for year in years:
        
        tot_year_data = pylab.array(0.0) * range(len(climate.get_yearly_temp(multi_cities[0], year)))        
        
        for city in multi_cities:
            
            tot_year_data += climate.get_yearly_temp(city, year)

        tot_year_data /= len(multi_cities)
        
        stdevs.append(pylab.std(tot_year_data))
    
    return pylab.array(stdevs)
    

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
##    Copied and edited code from function evaluate_models_on_training:
    
    #    Helper function
    def plot(x, y, estimates, rmse, degree):
        pylab.figure()
        pylab.title('Degree ' + str(degree) + ' linear regression model:' + '\n'
                        'rmse = ' + str(round(rmse, 4)))
        pylab.xlabel('Date')
        pylab.ylabel('Temperature (C)')
        pylab.plot(x, y, 'bo', label = 'Training Data')
        pylab.plot(x, estimates, 'r', label = 'Model')
        pylab.legend(loc = 'best')
        
        
    for model in models:
#        Define variables for model, will pass to plot function
        degree = len(model) - 1
        estimates = pylab.polyval(model, x)
        RMSE = rmse(y, estimates)
#        Create plot for each model
        plot(x, y, estimates, RMSE, degree)
    

if __name__ == '__main__':



#    # Part A.4
#
#    climate_data = Climate('data.csv')
#    training_data = []
#    x_training = []
#    city = 'BOSTON'
#    month = 1
#    day = 10
#    
#    
#    for year in TRAINING_INTERVAL:
#        training_data.append(pylab.mean(climate_data.get_daily_temp(city, month, day, year)))
#        x_training.append(year)
#        
#    training_data = pylab.array(training_data)
#    x_training = pylab.array(x_training)
#    
#    
#    model = generate_models(x_training, training_data, [1])
#    evaluate_models_on_training(x_training, training_data, model)
### 
##    
##    
##   ###### 2nd part of Part A 
##    
#    climate_data = Climate('data.csv')
#    training_data = []
#    x_training = []
#    city = 'BOSTON' 
#
#    for year in TRAINING_INTERVAL:
#        training_data.append(climate_data.get_yearly_temp(city, year).mean())
#        x_training.append(year)
#        
#    training_data = pylab.array(training_data)
#    x_training = pylab.array(x_training)
#
#    model = generate_models(x_training, training_data, [1])
#    evaluate_models_on_training(x_training, training_data, model)
#
#############
#    
#### Training on national yearly averages across cities
##    # Part B
#
#    climate_data = Climate('data.csv')
#    training_data = []
#    year_list = []    
#    
##    Gen cities avg asks for range of years as list of int .. doesn't actually matter
#    for year in TRAINING_INTERVAL:
#        year_list.append(year)
#    
#    
#    training_data = gen_cities_avg(climate_data, CITIES, year_list)
#   
##      need to convert to array now     
#    x_training = pylab.array(year_list)    
#    
#    model = generate_models(x_training, training_data, [1])
#    evaluate_models_on_training(x_training, training_data, model)   
##    
#
############
#### Training on 5yr moving avg of national yearly avgs    
#    # Part C
#    
#    climate_data = Climate('data.csv')
#    training_years = []    
#
#    for year in TRAINING_INTERVAL:
#        training_years.append(year)
#
##   Get yearly avgs and then the 5 yr moving avgs
#    training_avgs = gen_cities_avg(climate_data, CITIES, training_years)
#    training_data = moving_average(training_avgs, 5)
#    
#    training_years = pylab.array(training_years)
#    
#    model = generate_models(training_years, training_data, [1])
#    evaluate_models_on_training(training_years, training_data, model)       
    


###############
#    # Part D.2
#    climate_data = Climate('data.csv')
#    training_years = []    
#
##   Get list of years that make up training set
#    for year in TRAINING_INTERVAL:
#        training_years.append(year)
#
##   Get yearly national avgs and then the 5 yr national moving avgs
#    training_avgs = gen_cities_avg(climate_data, CITIES, training_years)
#    training_data = moving_average(training_avgs, 5)
#
##    Convert years to array
#    training_years = pylab.array(training_years)
##   Generate models and evaluate    
#    model = generate_models(training_years, training_data, [1,2,20])
#    evaluate_models_on_training(training_years, training_data, model)  
    
    
### Next steps of D:

#    test_years = []
#    for year in TESTING_INTERVAL:
#        test_years.append(year)
#    
#
##    Not sure whether to calc 5 yr moving avgs from entire data set or just from test year range
#    test_avgs = gen_cities_avg(climate_data, CITIES, test_years)
#    test_data = moving_average(test_avgs, 5)
#
#    evaluate_models_on_testing(test_years, test_data, model)

######################
    # Part E
#    Training on std data
    
    climate_data = Climate('data.csv')
    training_years = []  
    
    for year in TRAINING_INTERVAL:
        training_years.append(year)
        
    training_data = gen_std_devs(climate_data, CITIES, training_years)
    training_data = moving_average(training_data, 5)
    
    training_years = pylab.array(training_years)
    
    model = generate_models(training_years, training_data, [1])

    evaluate_models_on_training(training_years, training_data, model)    
#    
    
    
    
    