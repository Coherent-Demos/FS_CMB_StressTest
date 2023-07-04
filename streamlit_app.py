import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import plotly.graph_objects as go

@st.cache_data
def callSparkModel(selectedbank, CR1, CR2, CR3, LR, CR4, FX):

    url = "https://excel.uat.us.coherent.global/coherent/api/v3/folders/Spark FE Demos/services/banking-stress-test/Execute"

    payload = json.dumps({
       "request_data": {
          "inputs": {
            "Bank": selectedbank,
            "CR1_DoubtfulLoans": CR1['doubtfulloans'],
            "CR1_Haircut": CR1['haircut'],
            "CR1_LossLoans": CR1['lossloans'],
            "CR1_SubstandardLoans": CR1['substandardloans'],
            "CR2_IncreaseNPL": CR2['increaseNPL'],
            "CR2_ProvisioningNPL": CR2['provisionNPL'],
            "CR3Agri": CR3['Agri'],
            "CR3Manu": CR3['Manu'],
            "CR3Const": CR3['Const'],
            "CR3Trade": CR3['Trade'],
            "CR3Tour": CR3['Tour'],
            "CR3Nonbank": CR3['Nonbank'],
            "CR3Other": CR3['Other'],
            "CR3Provis": CR3['Provis'],
            "LR_Domestic": LR['domesticcurrency'],
            "LR_Foreign": LR['foreigncurrency'],
            "LR_AssetsAvailable": LR['assetsavailable'],
            "CR4_LEtoNPL": CR4['letonpl'],
            "CR4_Provisioning": CR4['leprovisioning'],
            "FX_ChangeRate": FX['changerate'],
            "FX_NewNPL": FX['depreciationtonpl'],
            "FX_Provisioning": FX['fxprovisioning']
          }
       },
        "request_meta": {
            "compiler_type": "Neuron",
        }
    })
    headers = {
       'Content-Type': 'application/json',
       'x-tenant-name': 'coherent',
       'SecretKey': '2277565c-9fad-4bf4-ad2b-1efe5748dd11'
    }


    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    return response

#Generate Charts
def generate_pie_chart(fig, data_df, config):
    fig.add_trace(go.Pie(labels=data_df[config['labels_column']], values=data_df[config['values_column']], hole=0.5, domain=dict(x=[0.1, 0.9], y=[0.1, 0.9])))
    fig.update_layout(
        title=config['title'],
        legend=dict(orientation='h', yanchor='bottom', y=-0.2),
        margin=dict(t=0, b=0)
    )

def generate_bar_chart(fig, data_df, config):
    for column in data_df.columns:
        if column != config['label_column']:
            fig.add_trace(go.Bar(name=column, x=data_df[column], y=data_df[config['label_column']], orientation='h'))    
    fig.update_layout(title=config['title'])

def generate_line_chart(fig, data_df, config):
    for column in data_df.columns:
        if column != config['x_column']:
            fig.add_trace(go.Scatter(
                x=data_df[config['x_column']],
                y=data_df[column],
                mode='lines',
                name=column
            ))
    fig.update_layout(title=config['title'])   

# Start of UI
st.write("## Banking Stress Test")

defaultbank = 'SB1'
selectedbank = st.selectbox('Choose a Bank', ['SB1', 'SB2', 'SB3', 'DB1', 'DB2', 'DB3', 'DB4', 'DB5', 'FB1', 'FB2', 'FB3', 'FB4'])

#default stress parameters substandardloans=20, doubtfulloans=50, lossloans=75, haircut=75
# Check if sliders have been changed
if 'substandardloans' not in st.session_state:
    # Set default values for sliders
    st.session_state.substandardloans = 20
    st.session_state.doubtfulloans = 50
    st.session_state.lossloans = 75
    st.session_state.haircut = 75

st.text("‎")

with st.expander("**Balance Sheet**", expanded=True):
   col11, col12, col13 = st.columns([1, 1, 1])
   with col11:
      st.info("Assets")
      assets_placeholder = st.empty()
   with col12:
      st.info("Loans") 
      loans_placeholder = st.empty()
   with col13:
      st.info("Liabilities")
      liabilities_placeholder = st.empty()

with st.expander("**Credit Risk**"):
   tab1, tab2, tab3, tab4 = st.tabs(['Underprovisioning', 'Increase in NPL', 'Sectoral Shock to NPL', 'Large Exposure'])

   with tab1:
      st.text("‎") 
      col20, col21, col22, col23, col24, = st.columns([1, 12, 2, 32, 1])
      with col20:
         st.text("‎") 
      with col21:
         st.write("Assumed Provisioning Rates")
         substandardloans = st.slider(
             'Substandard Loans (%)',
             0, 100, (20))
         doubtfulloans = st.slider(
             'Doubtful Loans (%)',
             0, 100, (50))
         lossloans = st.slider(
             'Loss Loans (%)',
             0, 100, (100))
         haircut = st.slider(
             'Assumed Haircut on Collateral (%)',
             0, 100, (75))
         st.text("‎") 
      with col22:
         st.text("‎") 
      with col23:  
         st.write("Post-Shock Data")
         st.markdown('***')
         col231, col232 = st.columns([1,1])
         with col231:
            CR1CARB = st.empty()
         with col232:
            CR1CARPS = st.empty()
         st.markdown('***')
         CR1loanvalues_placeholder = st.empty()
         st.markdown('***')
         CR1assetquality_placeholder = st.empty()
      with col24:
         st.text("‎") 

   with tab2:
      st.text("‎") 
      col20, col21, col22, col23, col24, = st.columns([1, 12, 2, 32, 1])
      with col20:
         st.text("‎") 
      with col21:
         st.write("Assumptions")
         increaseNPL = st.slider(
             'Assumed Increase in NPL',
             0, 100, (25))
         provisionNPL = st.slider(
             'Assumed provisioning of the new NPL (%)',
             0, 100, (25))
         st.text("‎")
      with col22:
         st.text("‎")  
      with col23:  
         st.write("Post Shock Data")
         st.markdown('***')
         col231, col232 = st.columns([1,1])
         with col231:
            CR2CARB = st.empty()
         with col232:
            CR2CARPS = st.empty()
         st.markdown('***')
         CR2assetvalues_placeholder = st.empty()


   with tab3:
      st.text("‎") 
      col20, col21, col22, col23, col24, = st.columns([1, 12, 2, 32, 1])
      with col20:
         st.text("‎") 
      with col21:
         st.write("Assumed shocks (% of performing loans in the sector becoming NPLs)")
         Agri = st.slider(
             'Agriculture',
             0, 100, (0))
         Manu = st.slider(
             'Manufacturing',
             0, 100, (0))
         Const = st.slider(
             'Construction',
             0, 100, (0))
         Trade = st.slider(
             'Trade',
             0, 100, (0))
         Tour = st.slider(
             'Tourism',
             0, 100, (0))
         Nonbank = st.slider(
             'Non-bank Financial',
             0, 100, (0))
         Other = st.slider(
             'Other',
             0, 100, (0))
         Provis = st.slider(
             'Assumed Provisioning Rate',
             0, 100, (0))
         st.text("‎")
      with col22:
         st.text("‎")  
      with col23:  
         st.write("Post Shock Data")
         st.markdown('***')
         col231, col232 = st.columns([1,1])
         with col231:
            CR3CARB = st.empty()
         with col232:
            CR3CARPS = st.empty()
         col231, col232 = st.columns([1,1])
         with col231:
            CR3NPLB = st.empty()
         with col232:
            CR3NPLPS = st.empty()
         st.markdown('***')
         CR3assetvalues_placeholder = st.empty()

   with tab4:
      st.text("‎") 
      col20, col21, col22, col23, col24, = st.columns([1, 12, 2, 32, 1])
      with col20:
         st.text("‎") 
      with col21:
         st.write("Assumptions")
         st.text("Largest Exposures")
         CR4exposures_placeholder = st.empty()
         letonpl = st.slider(
             'Number of Large Exposures to NPL',
             0, 5, (4))
         leprovisioning = st.slider(
             'Assumed Provisioning Rate',
             0, 100, (100))
         st.text("‎")
      with col22:
         st.text("‎")  
      with col23:  
         st.write("Post Shock Data")
         st.markdown('***')
         col231, col232 = st.columns([1,1])
         with col231:
            CR4CARB = st.empty()
         with col232:
            CR4CARPS = st.empty()
         st.markdown('***')
         CR4assetvalues_placeholder = st.empty()

with st.expander("**Liquidity Risk**"):
      st.text("‎") 
      col20, col21, col22, col23, col24, = st.columns([1, 12, 2, 32, 1])
      with col20:
         st.text("‎") 
      with col21:
         st.write("Withdrawals per Day (m$)")
         domesticcurrency = st.slider(
             'Domestic Currency',
             0, 100, (15))
         foreigncurrency = st.slider(
             'Foreign Currency',
             0, 100, (10))
         assetsavailable = st.slider(
             'Liquid Assets Available',
             0, 100, (95))
         st.text("‎") 
      with col22:
         st.text("‎") 
      with col23:  
         st.write("Post-Shock Data")
         st.markdown('***')
         LRisliquid = st.empty()
         st.markdown('***')
         LRliquiditychart_placeholder = st.empty()
         LRliquiditytable_placeholder = st.empty()

with st.expander("**FX Risk**"):
      st.text("‎") 
      col20, col21, col22, col23, col24, = st.columns([1, 12, 2, 32, 1])
      with col20:
         st.text("‎") 
      with col21:
         st.write("Assumptions")
         changerate = st.slider(
             'Assumed Exchange Rate Change (%)',
             0, 100, (55))
         depreciationtonpl = st.slider(
             '100 percent depreciation leads to x percent of FX loans becoming NPL. x=',
             0, 100, (10))
         fxprovisioning = st.slider(
             'Assumed Provisioning of new NPL (%)',
             0, 100, (50))
         st.text("‎") 
      with col22:
         st.text("‎") 
      with col23:  
         st.write("Post-Shock Data")
         st.markdown('***')
         col231, col232 = st.columns([1,1])
         with col231:
            FXCARB = st.empty()
         with col232:
            FXCARPS = st.empty()
         col231, col232 = st.columns([1,1])
         with col231:
            FXPOS = st.empty()
         with col232:
            FXLoan = st.empty()
         st.markdown('***')
         FXDirect_placeholder = st.empty()
         FXIndirect_placeholder = st.empty()

with st.expander("**Interest Risk**"):
      st.error("under construction")

CR1 = {
    'substandardloans': substandardloans,
    'doubtfulloans': doubtfulloans,
    'lossloans': lossloans,
    'haircut': haircut
}

CR2 = {
    'increaseNPL': increaseNPL,
    'provisionNPL': provisionNPL
}

CR3 = {
    'Agri': Agri,
    'Manu': Manu,
    'Const': Const,
    'Trade': Trade,
    'Tour': Tour,
    'Nonbank': Nonbank,
    'Other': Other,
    'Provis': Provis
}

LR = {
    'domesticcurrency': domesticcurrency,
    'foreigncurrency': foreigncurrency,
    'assetsavailable': assetsavailable
}

CR4 = {
    'letonpl': letonpl,
    'leprovisioning': leprovisioning
}

FX = {
    'changerate': changerate,
    'depreciationtonpl': depreciationtonpl,
    'fxprovisioning': fxprovisioning
}

alldata = callSparkModel(selectedbank, CR1, CR2, CR3, LR, CR4, FX)
outputs = alldata.json()['response_data']['outputs']

#Assets Data
df_assets = pd.DataFrame(outputs['BalanceSheetAssets'])
fig_assets = go.Figure()
config_assets = {
    'labels_column': 'Assets (m$)',
    'values_column': 'Value',
    'title': ''
}
generate_pie_chart(fig_assets, df_assets, config_assets)
assets_placeholder.plotly_chart(fig_assets, use_container_width=True)

#Liabilities Data
df_loans = pd.DataFrame(outputs['BalanceSheetLoans'])
fig_loans = go.Figure()
config_loans = {
'labels_column': 'Loans Breakdown (m$)',
'values_column': 'Value',
'title': ''
}
generate_pie_chart(fig_loans, df_loans, config_loans)
loans_placeholder.plotly_chart(fig_loans, use_container_width=True)

#Liabilities Data
df_liabilities = pd.DataFrame(outputs['BalanceSheetLiabilities'])
fig_liabilities = go.Figure()
config_liabilities = {
'labels_column': 'Liabilities (m$)',
'values_column': 'Value',
'title': ''
}
generate_pie_chart(fig_liabilities, df_liabilities, config_liabilities)
liabilities_placeholder.plotly_chart(fig_liabilities, use_container_width=True)

#CR1Data
df_CR1loanvalues = pd.DataFrame(outputs['CR1_LoanValues'])
fig_CR1loanvalues = go.Figure()
config_CR1loanvalues = {
    'label_column': 'Loan Values (m$)',
    'title': '      Loan Values (m$)'
}
generate_bar_chart(fig_CR1loanvalues, df_CR1loanvalues, config_CR1loanvalues)
CR1loanvalues_placeholder.plotly_chart(fig_CR1loanvalues, use_container_width=True)

CR1CARB_value = "{:,.2f}".format(outputs['CR1_CAR'][0]['Baseline'])
CR1CARPS_value = "{:,.2f}".format(outputs['CR1_CAR'][0]['Post Shock'])
CR1CARdelta = "{:,.2f}".format(outputs['CR1_CAR'][0]['Post Shock'] - outputs['CR1_CAR'][0]['Baseline'])

CR1CARB.metric(label="CAR Baseline", value=CR1CARB_value)
CR1CARPS.metric(label="CAR Post-Shock", value=CR1CARPS_value, delta=CR1CARdelta)


df_CR1assetquality = pd.DataFrame(outputs['CR1_AssetQuality'])
fig_CR1assetquality = go.Figure()
config_CR1assetquality = {
    'label_column': 'Asset Quality (m$)',
    'title': '      Asset Quality (m$)'
}
generate_bar_chart(fig_CR1assetquality, df_CR1assetquality, config_CR1assetquality)
CR1assetquality_placeholder.plotly_chart(fig_CR1assetquality, use_container_width=True)

#CR2Data
CR2CARB_value = "{:,.2f}".format(outputs['CR2_CAR'][0]['Baseline'])
CR2CARPS_value = "{:,.2f}".format(outputs['CR2_CAR'][0]['Post Shock'])
CR2CARdelta = "{:,.2f}".format(outputs['CR2_CAR'][0]['Post Shock'] - outputs['CR2_CAR'][0]['Baseline'])

CR2CARB.metric(label="CAR Baseline", value=CR2CARB_value)
CR2CARPS.metric(label="CAR Post-Shock", value=CR2CARPS_value, delta=CR2CARdelta)

df_CR2assetvalues = pd.DataFrame(outputs['CR2_AssetValues'])
fig_CR2assetvalues = go.Figure()
config_CR2assetvalues = {
    'label_column': 'Asset Values (m$)',
    'title': '      Asset Values (m$)'
}
generate_bar_chart(fig_CR2assetvalues, df_CR2assetvalues, config_CR2assetvalues)
CR2assetvalues_placeholder.plotly_chart(fig_CR2assetvalues, use_container_width=True)

#CR3 Data
CR3CARB_value = "{:,.2f}".format(outputs['CR3_CAR'][0]['Baseline'])
CR3CARPS_value = "{:,.2f}".format(outputs['CR3_CAR'][0]['Post Shock'])
CR3CARdelta = "{:,.2f}".format(outputs['CR3_CAR'][0]['Post Shock'] - outputs['CR3_CAR'][0]['Baseline'])
CR3NPLB_value = "{:,.2f}".format(outputs['CR3_NPL'][0]['Baseline'])
CR3NPLPS_value = "{:,.2f}".format(outputs['CR3_NPL'][0]['Post Shock'])
CR3NPLdelta = "{:,.2f}".format(outputs['CR3_NPL'][0]['Post Shock'] - outputs['CR3_NPL'][0]['Baseline'])

CR3CARB.metric(label="CAR Baseline", value=CR3CARB_value)
CR3CARPS.metric(label="CAR Post-Shock", value=CR3CARPS_value, delta=CR3CARdelta)
CR3NPLB.metric(label="NPL Baseline (m$)", value=CR3NPLB_value)
CR3NPLPS.metric(label="NPL Post-Shock (m$)", value=CR3NPLPS_value, delta=CR3NPLdelta)

df_CR3assetvalues = pd.DataFrame(outputs['CR3_NPLSector'])
fig_CR3assetvalues = go.Figure()
config_CR3assetvalues = {
    'label_column': 'NPLs by Sector (m$)',
    'title': '      NPLs by Sector (m$)'
}
generate_bar_chart(fig_CR3assetvalues, df_CR3assetvalues, config_CR3assetvalues)
CR3assetvalues_placeholder.plotly_chart(fig_CR3assetvalues, use_container_width=True)

#CR4 Data
CR4CARB_value = "{:,.2f}".format(outputs['CR4_CAR'][0]['Baseline'])
CR4CARPS_value = "{:,.2f}".format(outputs['CR4_CAR'][0]['Post Shock'])
CR4CARdelta = "{:,.2f}".format(outputs['CR4_CAR'][0]['Post Shock'] - outputs['CR4_CAR'][0]['Baseline'])

CR4CARB.metric(label="CAR Baseline", value=CR4CARB_value)
CR4CARPS.metric(label="CAR Post-Shock", value=CR4CARPS_value, delta=CR4CARdelta)

df_CR4Exp = pd.DataFrame(outputs['CR4_Exposures'])
df_CR4assetvalues = pd.DataFrame(outputs['CR4_AssetValues'])
fig_CR4assetvalues = go.Figure()
config_CR4assetvalues = {
    'label_column': 'Asset Values (m$)',
    'title': '      Asset Values (m$)'
}
generate_bar_chart(fig_CR4assetvalues, df_CR4assetvalues, config_CR4assetvalues)
CR4assetvalues_placeholder.plotly_chart(fig_CR4assetvalues, use_container_width=True)
CR4exposures_placeholder.dataframe(df_CR4Exp)

#LR Data
LRisliquid_value = outputs['LR_LiquidityFiveDays']
LRisliquid.metric(label="Liquidity in 5 days", value=LRisliquid_value)

df_LRliquiditytable = pd.DataFrame(outputs['LiquidutyTable2'])
fig_LRliquiditytable = go.Figure()
config_LRliquiditytable = {
    'x_column': 'Simple liquidity test (run on all banks, fire-sale of assets)',
    'title': '      Simple liquidity test (run on all banks, fire-sale of assets)'
}
generate_line_chart(fig_LRliquiditytable, df_LRliquiditytable, config_LRliquiditytable)
LRliquiditychart_placeholder.plotly_chart(fig_LRliquiditytable, use_container_width=True)
LRliquiditytable_placeholder.dataframe(df_LRliquiditytable)


#FX Data
FXCARB_value = "{:,.2f}".format(outputs['FX_CAR'][0]['Baseline'])
FXCARPS_value = "{:,.2f}".format(outputs['FX_CAR'][0]['Post Shock'])
FXCARdelta = "{:,.2f}".format(outputs['FX_CAR'][0]['Post Shock'] - outputs['FX_CAR'][0]['Baseline'])

FXPOS_value = "{:,.2f}".format(outputs['FX_NetPosition'])
FXLoan_value = "{:,.2f}".format(outputs['FX_Loans'])


FXCARB.metric(label="CAR Baseline", value=FXCARB_value)
FXCARPS.metric(label="CAR Post-Shock", value=FXCARPS_value, delta=FXCARdelta)
FXPOS.metric(label="Net Open FX Pos (m$)", value=FXPOS_value)
FXLoan.metric(label="FX Loans (m$)", value=FXLoan_value)

df_FXassetvaluesdirect = pd.DataFrame(outputs['FX_AssetValues'])
fig_FXassetvaluesdirect = go.Figure()
config_FXassetvaluesdirect = {
    'label_column': 'Asset Values - Direct FX (m$)',
    'title': '      Asset Values - Direct FX (m$)'
}
df_FXassetvaluesindirect = pd.DataFrame(outputs['FX_AssetValues2'])
fig_FXassetvaluesindirect = go.Figure()
config_FXassetvaluesindirect = {
    'label_column': 'Asset Values - Indirect FX (m$)',
    'title': '      Asset Values - Indirect FX (m$)'
}
generate_bar_chart(fig_FXassetvaluesdirect, df_FXassetvaluesdirect, config_FXassetvaluesdirect)
FXDirect_placeholder.plotly_chart(fig_FXassetvaluesdirect, use_container_width=True)

generate_bar_chart(fig_FXassetvaluesindirect, df_FXassetvaluesindirect, config_FXassetvaluesindirect)
FXIndirect_placeholder.plotly_chart(fig_FXassetvaluesindirect, use_container_width=True)


