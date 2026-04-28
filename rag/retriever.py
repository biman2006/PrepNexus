def retrieve_role_info(role,vectorstore,k=1):
    results=vectorstore.similarity_search(role,k=k)

    return results