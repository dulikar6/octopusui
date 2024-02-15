import json

import pandas as pd
import requests
import streamlit as st


def call_apis(vehicle_type, vehicle_model, vehicle_year_one, vehicle_year_two, city, mileage):

    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'N62YeXd0u3yMLX7NjLKVleNKqV4gFuOMF5a0a0eEMSlwXLGbh5GB3mH3TRSd1nlN',
    }

    params = {
        'vehicle_type': vehicle_type,
        'vehicle_model': vehicle_model.lower(),
        'vehicle_year_one': vehicle_year_one,
        'vehicle_year_two': vehicle_year_two,
        'city': city,
        'mileage': mileage
    }

    response = requests.get('https://ocotopus.azurewebsites.net/load_car_details/', params=params, headers=headers)

    if response.status_code == 200:
        result = json.loads(response.text)
        result = json.loads(result)
        print(type(result))
        df = pd.DataFrame(result.get('extracted_df'))
        print("Average Price:", result.get('average_price'))
        print("Based on City:", result.get('based_on_city'))
        print("Based on Mileage:", result.get('based_on_mileage'))
    else:
        print("Error:", response.text)

    return df, result['average_price'], result['based_on_city'], result['based_on_mileage']


# Function to display Matplotlib tables
def display_table(data):
    # fig, ax = plt.subplots()
    # ax.axis('tight')
    # ax.axis('off')
    # ax.table(cellText=data.values, colLabels=data.columns, loc='center')
    # st.pyplot(fig)
    st.table(data)


# Function to display description
def display_description(description):
    st.write(description)


# Main function for Streamlit app
def main():
    st.title("Vehicle Details Collection App")

    # Collecting vehicle details
    st.header("Enter Vehicle Details")
    vehicle_type = st.text_input("Vehicle Type")
    vehicle_model = st.text_input("Vehicle Model")
    vehicle_year_one = st.text_input("Year of Manufacture From")
    vehicle_year_two = st.text_input("Year of Manufacture To")
    city = st.text_input("City")
    mileage = st.text_input("Mileage")

    # Collecting multiple vehicle images
    st.header("Upload Vehicle Images")
    uploaded_images = st.file_uploader("Upload Images", accept_multiple_files=True)

    # Collecting vehicle insurance picture
    st.header("Upload Vehicle Insurance Picture")
    insurance_image = st.file_uploader("Upload Insurance Picture", type=['jpg', 'png', 'jpeg'])

    # Submit button
    if st.button("Submit"):
        extracted_df, average_price, based_on_city, based_on_mileage = call_apis(vehicle_type, vehicle_model,
                                                                                 vehicle_year_one, vehicle_year_two,
                                                                                 city, mileage)
        st.success("Details submitted successfully!")

        # Process uploaded images
        if uploaded_images:
            st.header("Uploaded Vehicle Images:")
            for img in uploaded_images:
                st.image(img, caption='Uploaded Image', use_column_width=True)

        # Display vehicle insurance picture
        if insurance_image:
            st.header("Uploaded Vehicle Insurance Picture:")
            st.image(insurance_image, caption='Insurance Image', use_column_width=True)

        # Mock data for tables
        # data1 = pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])
        # data2 = pd.DataFrame(np.random.randn(5, 3), columns=['X', 'Y', 'Z'])

        # Display tables
        st.header("Table 1")
        display_table(extracted_df)

        # st.header("Table 2")
        # display_table(data2)

        # Display description
        st.header("Description")
        average_price = eval(average_price)
        display_description(f"Average Price : {average_price[0]} to {average_price[1]}")
        display_description(f"Based on City : {based_on_city}")
        display_description(f"Based on Mileage: {based_on_mileage}")



if __name__ == '__main__':
    main()
