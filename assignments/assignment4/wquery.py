from whoosh.index import open_dir

ix = open_dir("indexdir")

q = raw_input("Enter Query: ")
q = q.strip()
print q