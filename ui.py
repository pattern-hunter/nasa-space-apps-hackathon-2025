import streamlit as st
import classes as cls
import graph as grp
import agent, textwrap
import base64, csv, pickle
import pandas as pd

st.title("Exoplanet Chatbot")

st.header("Upload new data")
st.write("Download this template file, add your data, upload it, and we will tell you if that data represents an exoplanet!")
st.markdown(f"""
    <a href="data:application/octet-stream;charset=utf-8;base64,{base64.b64encode(open("template.csv", 'rb').read()).decode()}" 
        id="download-button" download="{"template.csv"}">
        Download {"template.csv"}
    </a>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file")
    
if uploaded_file is not None:
    # Save the uploaded file in the temporary directory
    with open("temp_data.csv", 'wb') as f:
        f.write(uploaded_file.getbuffer())

    with open("temp_data.csv", "r") as datafile:
        X = []
        csvlines = list(csv.DictReader(datafile))
        count = 0
        accepted_keys = []
		
        m = csvlines[0]
        for key, val in m.items():
            if key != "rowid":
                try:
                    t = float(val)
                    accepted_keys.append(key)
                except ValueError:
                    pass
                
        row_ids = []
        for line in csvlines:
            x = []
            row_ids.append(line['rowid'])
            for key in accepted_keys:
                if line[key] == "":
                    x.append(0.0)
                else:
                    x.append(float(line[key]))
            X.append(x)

        with open("model.pkl", "rb") as pklfile:
            rf = pickle.load(pklfile)
            y_pred = rf.predict(X)

            koi_dispositions = {1:'CONFIRMED', 2:'CANDIDATE', 3:'FALSE POSITIVE'}
            data = {"Result": list(map(lambda x: koi_dispositions[x], y_pred))}
            df = pd.DataFrame(data, index=row_ids)
            st.table(df)

st.header("OR")

st.header("Ask questions about the data:")

# Get user input
user_input = st.text_area("Message", height=100, key="user_input")

# generate_chart = st.checkbox("Generate chart", value=False)

# initialize user prompt
prompt = agent.init_prompt()

# initialize database connection
db = agent.init_db()

# initialization LLM connection
llm = agent.init_llm("llama3.1")

# initialize state for graph to use
state = agent.init_state(prompt=prompt, db=db, llm=llm)

if st.button("Send"):
    # Get the chatbot's response
    state["question"] = user_input
    graph = grp.build_graph()
    state = grp.execute_graph(graph=graph, state=state)
    # Display the response
    with st.spinner("Generating response..."):
        st.write("Query\n")
        st.code(textwrap.fill(state["query"], width=80), language="sql")
        st.write("Result\n")
        lresult = []
        for line in state["result"].split("\n"):
            lresult.append(textwrap.fill(line, width=80))
        st.code("\n".join(lresult), language="markdown")
        st.write("Answer\n")
        lanswer = []
        for line in state["answer"].split("\n"):
            lanswer.append(textwrap.fill(line, width=80))
        st.code("\n".join(lanswer), language="markdown")

        # st.code(state['code'], language="markdown")

        # if generate_chart:
        #     stmd.st_mermaid("\n".join(state['code'].split("\n")[1:-1]))