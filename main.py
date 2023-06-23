import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from nptdms import TdmsFile



def plot_data_graph(Time, data, title):
    fig_abs = go.Figure()
    fig_abs.add_trace(go.Scatter(x=Time, y=np.abs(data)))
    fig_abs.update_layout(
        title=title,
        xaxis_title='Time Series (Sec)',
        yaxis_title='Acceleration (g)',
    )
    return fig_abs

def perform_analysis(file_path):
    tdms_file = TdmsFile.read(file_path)
    group = tdms_file['log']

    channel1 = group['X[0]'] 
    channel2 = group['Y[1]']
    channel3 = group['Z[2]']

    data_x = channel1[:]
    data_y = channel2[:]
    data_z = channel3[:]


    sampling_rate = 200
    Time = np.arange(len(data_x)) / sampling_rate

    # Interpolate NaN values
    data_x = pd.Series(data_x).interpolate().values
    data_y = pd.Series(data_y).interpolate().values
    data_z = pd.Series(data_z).interpolate().values

    # X-axis FFT
    data_x, Time
    fig_x = plot_data_graph(Time, data_x, 'Channel 1: X-Axis Acceleration Time Series Data')

    # Y-axis FFT
    data_y, Time
    fig_y = plot_data_graph(Time, data_y, 'Channel 2: Y-Axis Acceleration Time Series Data')

    # Z-axis FFT
    data_z, Time
    fig_z = plot_data_graph(Time, data_z, 'Channel 3: Z-Axis Acceleraion Time Series Data')

    return fig_x, fig_y, fig_z


# Streamlit app code
def main():
    st.title('dinamikanaliz.io')
    st.header('Acceleration Data Visualization')

    # File upload section
    file = st.file_uploader("Upload TDMS file", type=["tdms"])

    if file is not None:
        # Save the uploaded file to the "Data" folder
        with open('Data/uploaded_file.tdms', 'wb') as f:
            f.write(file.getbuffer())

        file_path = 'Data/uploaded_file.tdms'

        # Perform analysis and generate graphs
        fig_x, fig_y, fig_z = perform_analysis(file_path)

        # Display the graphs using Streamlit
        st.plotly_chart(fig_x, use_container_width=True)
        st.plotly_chart(fig_y, use_container_width=True)
        st.plotly_chart(fig_z, use_container_width=True)

if __name__ == '__main__':
    main()