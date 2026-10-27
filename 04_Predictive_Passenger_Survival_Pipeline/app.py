import streamlit as st
import pandas as pd

from joblib import load

#load the data
model = load('tree.joblib')

train_cols = load('columns.joblib')
data = load('data.joblib')

#page settings
st.set_page_config(page_title="First User Interface ", layout="wide")

#title
st.title("🚢 🛳️Titanic Streamlit")
st.markdown("## *Interactive ML Dashboard with Titanic UI*")
st.write("Enter passenger details to predict survival chances")

st.divider()

st.sidebar.header("🎯 Paseenger Details")

PCLass = st.sidebar.radio("Passenger class",[1,2,3])

Sex = st.sidebar.radio("Sex",["Male","Female"])
Sex = 1 if Sex == "Male" else 0

Embarked = st.sidebar.selectbox("Embarked",["Cherbourg","Queenstown","Southampton"])
emb_map = {"Cherbourg":0,"Queenstown":1,"Southampton":2}
Embarked = emb_map[Embarked]

Age_cat = st.sidebar.slider("Age Category (0:Child 1:Teen 2:Youth  3:Senior)", 0,3,1)
Fare_cat = st.sidebar.slider("Fare Fategory (0:Low 1:Medium 2:High 3:Expensive)",0,3,1)

Family = st.sidebar.radio("Family Onboard?",["No","Yes"])
Family = 1 if Family == "Yes" else 0


#charts based on X
st.subheader("📊 Dataset Insights")

col1,col2,col3 = st.columns(3)
with col1 :
    st.write("Passenger Class Distribution")
    st.bar_chart(data["Pclass"].value_counts())

with col2 :
    male_count = int((data["Sex"]==1).sum())
    female_count = int((data["Sex"]==0).sum())

    m1,m2 = st.columns(2)

    with m1: 
      st.metric("Female",female_count)
    with m2: 
      st.metric("Male",male_count)
    st.bar_chart(data['Sex'].value_counts())
    
with col3 :
    st.metric("Unique Embarked",data["Embarked"].nunique())
    st.bar_chart(data["Embarked"].value_counts())

st.divider()    




Pclass =st.selectbox("Pclass",[1,2,3,],key="pclass")

Sex = st.selectbox('Sex',["Male","Female"],key="sex")
Sex = 1 if Sex =='Male' else 0

Embarked = st.selectbox("Embarked",["Cherbourg","Queenstown","Southampton"],key="embarked")
emb_map = {"Cherbourg":0,"Queenstown":1,"Southampton":2}
Embarked = emb_map[Embarked]


Age_cat = st.selectbox("Age Category",[0,1,2,3],key="age")
age_map = {0:0,1:1,2:2,3:3}
Age_cat = age_map[Age_cat]

Fare_cat = st.selectbox("Fare Category",[0,1,2,3],key="fare")
fare_map = {0:0,1:1,2:2,3:3}
Fare_cat = fare_map[Fare_cat]

Family = st.selectbox("Family",[0,1])
fam_map = {0:0,1:1,2:2,3:3}
Family = fam_map[Family]



#converting to dataframe

input_df = pd.DataFrame({
    'Pclass' : [Pclass],
    'Sex' : [Sex],
    'Embarked': [Embarked],
    'Age Category': [Age_cat],
    'Fare Category': [Fare_cat],
    'Family': [Family]
})

input_df = input_df.reindex(columns = train_cols,fill_value=0)


col_pred,col_prob = st.columns(2)
#predict
st.subheader("Prediction Panel")
with col_pred:
 if st.button("Predict"):
  result =  model.predict(input_df)
 
  prob = model.predict_proba(input_df)
 
  if result[0] ==1:
   st.success("Survived✅")
  else:
   st.error("Did not survived❌")
 
   st.session_state['Prob'] = [prob]
 
 with col_prob:
     if 'prob' in st.session_state:
      st.metric("Survival Probability",f"{round(prob[0][1]*100,2)}%")

#reset button
if st.button("Reset"):
 st.session_state.clear()
 st.rerun()

st.divider()     

 #input summary
st.subheader("📜 Input Summary")
st.write(input_df)



#st.write("Survival Probability:",prob[0][1])

st.subheader("Input Data")

st.write(input_df)


#Make a list for all categorical columns similar to embarked and sex

st.divider()

col1, col2 =st.columns(2)

with col1:
 Pclass = st.selectbox("Passenger Class",[1,2,3])
 Sex = st.selectbox("Sex",["Male","Female"])

 with col2:
  Embarked = st.selectbox("Embarked",["Cheerbourg","Queenstown","Southampton"])
  Family = st.selectbox("Family",["No","Yes"])
