import pandas as pd;
import numpy as np;
import streamlit as st;
import pickle as pk;

def modelPredict(input_data):
    model = pk.load(open("../model/model.pkl", "rb"))
    scaler = pk.load(open("../model/scaler.pkl", "rb"))

    inputArray = np.array(input_data).reshape(1, -1)

    inputArrayScaled = scaler.transform(inputArray)
  
    pred = model.predict(inputArrayScaled)
    
    # print(type(inputArray))
    print(pred)
    return pred;


def main():
    st.header("House Price :red[Prediction]", divider='green')

    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.number_input("Area in square", placeholder="5000", step=1)
        bedroom = st.number_input("Number of bedroom", placeholder='4', step=1)

        
        basement = st.checkbox("have basement")
        ariCond = st.checkbox("having air conditioning")

    with col2:
        bathroom = st.number_input("Insert a bathroom", placeholder='2', step=1)
        stories = st.number_input("Insert a stories", placeholder='2', step=1)
        
        guestroom = st.checkbox("have guestroom")
        hotWater = st.checkbox("having  hotwater heating option")

    with col3:
        furnishedStatus = st.selectbox(
            "Select the furnished status",
            ("furnished", "semi-furnished", "unfurnished"),
            index=0,
        )
        parkingOption = st.number_input("No. of parkingOption", placeholder='2', step=1)
        prefarea = st.checkbox("present in prefarea")
        mainRoad = st.checkbox("House in main road")

    myArray = pd.DataFrame(
        [area, bedroom, bathroom, stories, int(mainRoad), int(guestroom), int(basement), int(hotWater), int(ariCond), parkingOption, int(prefarea), int(furnishedStatus == 'furnished'), int(furnishedStatus == 'semi-unfurnished'), int(furnishedStatus == 'unfurnished')]
    )


    if(st.button('Predict')):
        pred = modelPredict(myArray)
        pred[0] = max(0, pred[0])
        # st.write(myArray)
        st.write(":blue[Cost of house : ]", round(pred[0], 3))



if __name__ == "__main__":
    main()