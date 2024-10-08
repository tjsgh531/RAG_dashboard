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
    with open('/upstage-ai-advanced-ir7/data/documents.jsonl', 'r') as f:
        for line in f:
            doc = json.loads(line)
            if doc['docid'] == id:
                return doc['content']

def search_contents(topk_ids):

    doc_contents = []
    for id in topk_ids:
        content = search_docs(id)
        doc_contents.append(content)

    return doc_contents 

def display_results(df, index):
    st.subheader(f"Query {index + 1}")
    st.write(f"Standalone Query: {df.iloc[index]['standalone_query']}")

    contents = df.iloc[index]['topk_content']
    topk = df.iloc[index]['topk']
    topk_df = pd.DataFrame([
        {"rank": 1, "id": topk[0], "content": contents[0]},
        {"rank": 2, "id": topk[1], "content": contents[1]},
        {"rank": 3, "id": topk[2], "content": contents[2]}
    ])

    st.table(topk_df)

def main():
    st.title("검색 결과 결과 대시보드")
    upload_file = st.file_uploader("검색 결과 csv 파일 업로드 ['standalone_query', 'topk']")

    if upload_file is not None:
        df = load_jsonl(upload_file)

        total_queries = len(df)
        query_index = st.slider("Select Query", 0, total_queries - 1, 0)        

        df["topk_content"] = df["topk"].apply(search_contents)
        display_df = df[["standalone_query","topk", "topk_content"]]

        display_results(display_df, query_index)

if __name__ == "__main__":
    main()