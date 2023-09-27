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
            "CR3Const": CR3['Const'],
            "CR3Manu": CR3['Manu'],
            "CR3Nonbank": CR3['Nonbank'],
            "CR3Other": CR3['Other'],
            "CR3Provis": CR3['Provis'],
            "CR3Tour": CR3['Tour'],
            "CR3Trade": CR3['Trade'],
            "CR4_LEtoNPL": CR4['letonpl'],
            "CR4_Provisioning": CR4['leprovisioning'],
            "FX_ChangeRate": FX['changerate'],
            "FX_NewNPL": FX['depreciationtonpl'],
            "FX_Provisioning": FX['fxprovisioning'],
            "LR_AssetsAvailable": LR['assetsavailable'],
            "LR_Domestic": LR['domesticcurrency'],
            "LR_Foreign": LR['foreigncurrency']
          }
       },
        "request_meta": {
        }
    })

    # url = "https://excel.staging.coherent.global/coherentflex/api/v3/folders/Spark FE Demos/services/banking-stress-test-2/Execute"

    # headers = {
    #    'Content-Type': 'application/json',
    #    'x-tenant-name': 'coherentflex',
    #    'x-synthetic-key': '302041c0-6c2b-4567-8b3a-ae21cbf9671c'
    # }

    url = "https://excel.uat.us.coherent.global/coherent/api/v3/folders/Spark FE Demos/services/banking-stress-test-4/Execute"

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

def truncate_text(text, max_words):
    words = text.split()
    truncated_words = words[:max_words]
    truncated_text = ' '.join(truncated_words) + '...'
    return truncated_text

# Start of UI
image_path = "coherent-logo.png"
st.image(image_path, caption="", width=32)

st.write("## Banking Stress Test")

tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Bank Data Modelling', 'Stess Test Simulation', 'API Details'])
with tab1:
   st.text("‎")
   st.write('### About this demo')
   st.markdown('This demo showcases different advanced ways to leverage Spark in banking and risk management:  \n* **Data Consolidation** - Taking banking data from different sources and creating a consolidated format  \n* **Interactive Simulation** - developing simulation models and testing with real input in real-time  \n* **Download the model** [here](https://spark.uat.us.coherent.global/coherent/products/Spark%20FE%20Demos/banking-stress-test-4/apiTester/test)')

   st.text("‎")
   st.write('### About Stress Testing')
   with st.expander("**Why Stress Testing Liquidity is Critical Before a Potential Recession**", expanded=True):
      col1, col2 = st.columns([8,1])
      with col1: 
         st.write('Testing model simulations are essential for helping banks and financial institutions test different scenarios to evaluate how changes in market conditions, such as interest rates and inflation assumptions, can impact a bank’s investment decisions, balance sheet, income statement, or liquidity...')
         st.write('[Read More](https://www.coherent.global/blog/why-stress-testing-liquidity-is-critical-before-a-recession)')
      with col2:   
         image = "article-1.png"
         st.image(image, caption='')
   with st.expander("**Why Testing Model Simulations are Critical for Reducing Risk**", expanded=True):
      col1, col2 = st.columns([8,1])
      with col1: 
         st.write('While many major banks recently reported positive earnings announcements, the news certainly hasn’t been all good. Numerous market indicators point to possible signs of a recession. Some banks are proactively taking steps to prepare for a potential recession and it’s critical that all banks take a closer look at enterprise-wide liquidity...')
         st.write('[Read More](https://www.coherent.global/blog/testing-model-simulations-risk-reduction)')
      with col2:   
         image = "article-2.png"
         st.image(image, caption='')

   st.text("‎")
   st.write('### About Coherent')
   with st.expander("**Coherent for Banking and Capital Markets**", expanded=True):
      col1, col2 = st.columns([8,1])
      with col1:   
         st.write('Coherent transforms businesses, starting with a single cell. We unify developers and non-developers to redefine how business and IT teams work together. We transform spreadsheets into APIs, end-users into developers, and risk into control.')
         st.write('[Learn More About Coherent for Banking and Capital Markets](https://resources.coherent.global/znglist/banking-and-capital-markets/?c=cG9zdDo5OTE4OTY%3D)  /  [Learn More About Coherent](https://www.coherent.global/)')
      with col2: 
         image = "coherent-logo-round.png"
         st.image(image, caption='')


with tab2:   
   st.info(":information_source:  **Model 1 - Bank Data Consolidation:** Here we are using Spark to call 3 external sources (fiance data, balance sheet, income statement), then consolidate, enrich and format this data. With Spark we are able to model this transformation in any way we want, allowing us to combine data from multiple sources without extra data processing steps")

   st.text("‎")
   defaultbank = 'Citigroup Inc.'
   selectedbank = st.selectbox('Choose a Bank', ['Associated Banc-Corp', 'Atlantic Union Bankshares Corporation', 'Banc of California Inc.', 'Bank of America Corporation', 'Bank of Hawaii Corporation', 'BankUnited Inc.', 'Bar Harbor Bankshares Inc.', 'Berkshire Hills Bancorp Inc.', 'Blue Ridge Bankshares Inc.', 'Byline Bancorp Inc.', 'Cadence Bank', 'Central Pacific Financial Corp', 'Citigroup Inc.', 'Citizens Financial Group Inc.', 'Comerica Incorporated', 'Community Bank System Inc.', 'Cullen/Frost Bankers Inc.', 'Customers Bancorp Inc', 'Evans Bancorp Inc.', 'F.N.B. Corporation', 'FB Financial Corporation', 'First Commonwealth Financial Corporation', 'First Horizon Corporation', 'Glacier Bancorp Inc.', 'Guaranty Bancshares Inc.', 'Hilltop Holdings Inc.', 'Home BancShares Inc.', 'JP Morgan Chase & Co.', 'KeyCorp', 'Live Oak Bancshares Inc.', 'M&T Bank Corporation', 'Metropolitan Bank Holding Corp.', 'National Bank Holdings Corporation', 'Nicolet Bankshares Inc.', 'Park National Corporation', 'PNC Financial Services Group Inc.', 'Prosperity Bancshares Inc.', 'Provident Financial Services Inc', 'Regions Financial Corporation', 'ServisFirst Bancshares Inc.', 'Synovus Financial Corp.', 'Tompkins Financial Corporation', 'Truist Financial Corporation', 'U.S. Bancorp', 'Webster Financial Corporation', 'Wells Fargo & Company', 'Western Alliance Bancorporation', 'York Community Bancorp Inc.'])
   st.write('***')
   col1, col2, col3 = st.columns([1,2,5])
   with col1:
      TICKER = st.empty()
   with col2:
      SECTOR = st.empty()
   with col3:
      st.write('Description')
      Description = st.empty()  

   st.text("‎")

   #default stress parameters substandardloans=20, doubtfulloans=50, lossloans=75, haircut=75
   # Check if sliders have been changed
   if 'substandardloans' not in st.session_state:
       # Set default values for sliders
       st.session_state.substandardloans = 20
       st.session_state.doubtfulloans = 50
       st.session_state.lossloans = 75
       st.session_state.haircut = 75


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

   st.text("‎")
   st.write("**Data Source 1: Finance Book of Records (Loans & Deposits)**")
   DATA_SOURCE3 = st.empty()
   st.write('***')
   col1, col2, col3 = st.columns([1,1,1])
   with col1:
      st.write("**Data Source 2: Balance Sheet**")
      DATA_SOURCE1 = st.empty()
   with col2:
      st.write("**Data Source 3: Income Statement**")
      DATA_SOURCE2 = st.empty()
   with col3:
      st.write("**Consolidated Data**")
      DATA_CONSOLIDATION = st.empty()

with tab3:
   st.success(":gear:  **Model 2 - Risk Simulation:** Here we are are using consolidated bank data from **Model 1** to test different Risk scenarios. For example, an increase in NPL for the bank. Because this is API-driven, we get instant response by changing any of the scenario variables. Below you will see 4 types of risk modelling where you can adjust the scenarios in real time.")

   st.text("‎")
   with st.expander("**Credit Risk**"):
      tab31, tab32, tab33, tab34 = st.tabs(['Underprovisioning', 'Increase in NPL', 'Sectoral Shock to NPL', 'Large Exposure'])

      with tab31:
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

      with tab32:
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


      with tab33:
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

      with tab34:
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

with tab4:

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


   st.write('API details')
   col41, col42 = st.columns([1,1])
   with col41:
      with st.expander("**API Input**", expanded=True):
         st.json({
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
                  "CR3Const": CR3['Const'],
                  "CR3Manu": CR3['Manu'],
                  "CR3Nonbank": CR3['Nonbank'],
                  "CR3Other": CR3['Other'],
                  "CR3Provis": CR3['Provis'],
                  "CR3Tour": CR3['Tour'],
                  "CR3Trade": CR3['Trade'],
                  "CR4_LEtoNPL": CR4['letonpl'],
                  "CR4_Provisioning": CR4['leprovisioning'],
                  "FX_ChangeRate": FX['changerate'],
                  "FX_NewNPL": FX['depreciationtonpl'],
                  "FX_Provisioning": FX['fxprovisioning'],
                  "LR_AssetsAvailable": LR['assetsavailable'],
                  "LR_Domestic": LR['domesticcurrency'],
                  "LR_Foreign": LR['foreigncurrency']
                }
             },
              "request_meta": {
              }
          })
   with col42:
      with st.expander("**API Output**", expanded=True):
         API_OUTPUT = st.empty()   

   #Assets Data
   TICKER_value = outputs["Ticker"]
   TICKER.metric(label="Ticker", value=TICKER_value)

   SECTOR_value = outputs["Sector"]
   SECTOR.metric(label="Sector", value=SECTOR_value)
   
   Description_value = truncate_text(outputs["Description"], max_words=100)
   Description.write(Description_value)

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

   DATA_SOURCE1df = pd.DataFrame(outputs['DataSource1'])
   DATA_SOURCE2df = pd.DataFrame(outputs['DataSource2'])
   DATA_SOURCE3df = pd.DataFrame(outputs['SampleFinanceBOR'])
   DATA_CONSOLIDATIONdf = pd.DataFrame(outputs['bankdata'])

   DATA_SOURCE1.dataframe(DATA_SOURCE1df)
   DATA_SOURCE2.dataframe(DATA_SOURCE2df)
   DATA_SOURCE3.dataframe(DATA_SOURCE3df)
   DATA_CONSOLIDATION.dataframe(DATA_CONSOLIDATIONdf)

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

   API_OUTPUT.json(outputs)