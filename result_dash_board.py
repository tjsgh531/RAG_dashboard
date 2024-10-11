import pandas as pd
import json
import streamlit as st

def load_jsonl(file):
    data = []
    for line in file:
        data.append(json.loads(line))
    
    df = pd.DataFrame(data)
    return df

def search_docs(id):
    with open('data/documents.jsonl', 'r') as f:
        for line in f:
            doc = json.loads(line)
            if doc['docid'] == id:
                return doc['content']

def search_docs(id):
    data = load_data()
    for doc in data:
        if doc['docid'] == id:
            return doc['content']
    return None

def display_results(df, index, answer_show):
    st.subheader(f"Query {index + 1}")
    st.write(f"Standalone Query: {df.iloc[index]['standalone_query']}")

    if answer_show:
        st.write(f"Answer : {df.iloc[index]['answer']}")

    references = df.iloc[index]['references']
    topk = df.iloc[index]['topk']
    topk_df = pd.DataFrame([
        {"rank": 1, "id": topk[0], "score" : references[0]['score'], "content": references[0]['content']},
        {"rank": 2, "id": topk[1], "score" : references[1]['score'], "content": references[1]['content']},
        {"rank": 3, "id": topk[2], "score" : references[2]['score'], "content": references[2]['content']}
    ])


    st.table(topk_df)

def main():
    st.title("검색 결과 결과 대시보드")
    upload_file = st.file_uploader("검색 결과 csv 파일 업로드 ['standalone_query', 'topk', 'references']")
    answer_show = st.checkbox("생성 답변 보기")

    if upload_file is not None:
        df = load_jsonl(upload_file)

        total_queries = len(df)
        query_index = st.slider("Select Query", 0, total_queries - 1, 0)        

        display_df = df[["standalone_query","topk", "references", 'answer']]

        display_results(display_df, query_index, answer_show)

if __name__ == "__main__":
    main()