from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

from langchain_community.embeddings.bedrock import BedrockEmbeddings
import argparse
import os
import shutil
import constants
from get_embedding_function import get_embedding_function

DATA_PATH = "data/"

def main():
  documents = load_documents()
  chunks = split_documents(documents)
  add_to_chroma(chunks)

def load_documents():
  loader = PyPDFDirectoryLoader(DATA_PATH)
  documents = loader.load()
  return documents


def split_documents(documents: list[Document]):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
    length_function=len,
    is_separator_regex=False,
  )
  return text_splitter.split_documents(documents)


def calculate_chunk_ids(chunks: list[Document]):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
      source = chunk.metadata.get("source")
      page = chunk.metadata.get("page")
      current_page_id = f"{source}:{page}"

      # If the page ID is the same as the last one, increment the index.
      if current_page_id == last_page_id:
        current_chunk_index += 1
      else:
        current_chunk_index = 0

      # Calculate the chunk ID.
      chunk_id = f"{current_page_id}:{current_chunk_index}"
      last_page_id = current_page_id

      # Add it to the page meta-data.
      chunk.metadata["id"] = chunk_id

    return chunks

def add_to_chroma(chunks: list[Document]):
  db = Chroma(persist_directory=constants.CHROMA_PATH, embedding_function=get_embedding_function())
  chunks_with_ids = calculate_chunk_ids(chunks)

  existing_items = db.get(include=[])  # IDs are always included by default
  existing_ids = set(existing_items["ids"])
  print(f"Number of existing documents in DB: {len(existing_ids)}")

  # Only add documents that don't exist in the DB.
  new_chunks = []
  for chunk in chunks_with_ids:
    if chunk.metadata["id"] not in existing_ids:
      new_chunks.append(chunk)

  if len(new_chunks):
    print(f"👉 Adding new documents: {len(new_chunks)}")
    new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    db.add_documents(new_chunks, ids=new_chunk_ids)
  else:
    print("✅ No new documents to add")

  return chunks_with_ids

def clear_database():
    if os.path.exists(constants.CHROMA_PATH):
      shutil.rmtree(constants.CHROMA_PATH)


if __name__ == "__main__":
    main()


