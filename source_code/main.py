# importing libraries
import streamlit as st
import math
import matplotlib.pyplot as plt

# operating weight = basic empty weight + fuel weight + crew weight + passenger weight + luggage/cargo weight + other variale items weight

# code for sidebar
with st.sidebar:
    # aircraft specifications 
    st.header('Aircraft Specifications')
    basic_empty_weight       = st.number_input('Basic Empty Weight of Aircraft(in lbs)', value = 0)
    number_of_seats          = st.number_input('Total Number of Passenger Seats in Aircraft', value = 0)
    maximum_payload_capacity = st.number_input('Maximum Payload Capacity of Aircraft(in lbs)', value = 0)

    # flight details
    st.header('Flight Details')
    fuel_weight             = st.number_input('Fuel Weight of Aircraft(in lbs)', value = 0)
    crew_weight             = st.number_input('Total Crew Weight in Aircraft(in lbs)', value = 0)
    other_variable_weight   = st.number_input('Other Variable Item Weight in Aircraft(in lbs)', value = 0)

    # max payload condition
    st.header('Max Payload Condition')
    max_payload_total_fuel_consumed     = st.number_input('Fuel Consumed by Aircraft under Max. Payload(in lbs)', value = 0)
    max_payload_fuel_consumption_rate   = st.number_input('Max. Payload Fuel Consumption of Aircraft(in lbs/NM)', value = 0.0)
    max_payload_lift_drag_ratio         = st.number_input('Max. Payload Lift-Drag Ratio of Aircraft', value = 0.0)

    # test payload condition
    st.header('Test Payload Condition')
    test_payload_fuel_consumption_rate  = st.number_input('Test Payload Fuel Consumption of Aircraft(in lbs/NM)', value = 0.0)
    test_payload_lift_drag_ratio        = st.number_input('Test Payload Lift-Drag Ratio of Aircraft', value = 0.0)

st.header('Aviation Costing')

st.write('##### Test Case Inputs:')

# code for main panel
distance_col, avg_passenger_weight_cols, total_seats_filled_col, luggage_weight_col = st.columns(4)
with distance_col:
    distance             = st.number_input('Total Flight Distance(in NM)', value = 0)

with avg_passenger_weight_cols:
    avg_passenger_weight = st.number_input('Avg. Passenger Wt.(in lbs)', value = 180)

with total_seats_filled_col:
    total_seats_filled   = st.number_input('Total Number of Filled Seats', value = 0)
    
with luggage_weight_col:
    luggage_weight       = st.number_input('Total Luggage Weight(in lbs)', value = 0)

# calculating initial and final weight
# maximum payload condition
max_payload_initial_weight  = basic_empty_weight + fuel_weight + crew_weight + number_of_seats*avg_passenger_weight +  maximum_payload_capacity + other_variable_weight
max_payload_final_weight    = max_payload_initial_weight - max_payload_fuel_consumption_rate*distance
# test payload condition
test_payload_initial_weight = basic_empty_weight + fuel_weight + crew_weight + total_seats_filled*avg_passenger_weight + luggage_weight + other_variable_weight
test_payload_final_weight   = test_payload_initial_weight - test_payload_fuel_consumption_rate*distance

# show initial and final weight
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# maximum payload condition
with row1_col1:
    st.write(f'Full Payload Initial Weight: {max_payload_initial_weight}')

with row1_col2:
    if max_payload_final_weight >= 0:
        st.write(f'Full Payload Final Weight: {max_payload_final_weight}')
    else:
        st.write('Full Payload Final Weight: invalid inputs')

# test payload condition
with row2_col1:
    st.write(f'Test Payload Initial Weight: {test_payload_initial_weight}')

with row2_col2:
    if test_payload_final_weight >= 0:
        st.write(f'Test Payload Final Weight: {test_payload_final_weight}')
    else:
        st.write('Test Payload Final Weight: invalid inputs')

st.markdown('----')

# calculating fuel consumed under test payload condition
test_payload_total_fuel_consumed = 0.0  # Default value

if (max_payload_fuel_consumption_rate != 0 and max_payload_lift_drag_ratio != 0 and max_payload_final_weight != 0 and test_payload_initial_weight != 0 and test_payload_final_weight != 0 and max_payload_initial_weight != 0 and test_payload_initial_weight != test_payload_final_weight):  
    # Avoid log(0)
    test_payload_total_fuel_consumed = (test_payload_fuel_consumption_rate / max_payload_fuel_consumption_rate)*(test_payload_lift_drag_ratio / max_payload_lift_drag_ratio)*(math.log(max_payload_initial_weight / max_payload_final_weight) /math.log(test_payload_initial_weight / test_payload_final_weight))*max_payload_total_fuel_consumed

# show test_payload_total_fuel_consumed
st.write(f'###### Fuel Consumed Under Max Payload Condition : {max_payload_total_fuel_consumed:.3f}')
st.write(f'###### Fuel Consumed Under Test Payload Condition : {test_payload_total_fuel_consumed:.3f}')

if max_payload_total_fuel_consumed != 0:
    fuel_costing_factor = test_payload_total_fuel_consumed/max_payload_total_fuel_consumed
else:
    fuel_costing_factor = 0.0

# show fuel costing factor    
st.write(f'##### Fuel Costing Factor : {fuel_costing_factor:.3f}')

st.markdown('-----')

aircraft_turbine_fuel_cost = st.number_input('###### Cost of Aircraft Turbine Fuel (in $/lb)', value = 0.0)
st.write(f'###### Flight Distance : {distance} NM')

# calculating profit
cost_difference = aircraft_turbine_fuel_cost*(max_payload_total_fuel_consumed-test_payload_total_fuel_consumed)
if distance != 0:
    profit_per_NM = cost_difference/distance
else:
    profit_per_NM = 0.0

st.write(f'###### Profit per NM : ${profit_per_NM:.2f}')
st.write(f'##### Total Profit : ${cost_difference:.2f}')
st.markdown('----')

# selecting datapoints for plotting
range = [0, distance]
max_payload_costing  = [0, aircraft_turbine_fuel_cost*max_payload_total_fuel_consumed]
test_payload_costing = [0, aircraft_turbine_fuel_cost*test_payload_total_fuel_consumed]

# plotting the data
plt.figure(figsize=(10,6))
plt.plot(range, max_payload_costing, label= 'Cost at Max. Payload Condition')
plt.plot(range, test_payload_costing, label= 'Cost at Test Payload Condition')
plt.fill_between(range, max_payload_costing, test_payload_costing, color= 'green', alpha= 0.3)
plt.title('Cost Difference Between Maximum and Test Payload Condition')
plt.xlabel('Distance')
plt.ylabel('Cost')
plt.legend()
st.pyplot(plt)