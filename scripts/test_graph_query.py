from app.graph.neo4j_query_service import Neo4jQueryService


service = Neo4jQueryService()

# symbols = service.find_symbol("invoke")

# for s in symbols:
#     print(s)


# callers = service.find_callers("invoke")

# print()

# print("Callers")

# print("--------")

# for caller in callers[:20]:

#     print(caller)  
 
# callees = service.find_callees("search")

# print()

# print("Callees")

# print("--------")

# for callee in callees[:20]:
#     print(callee) 



# commits = service.find_commits_for_file(
#     "libs/partners/anthropic/langchain_anthropic/chat_models.py"
# )

# for commit in commits[:5]:
#     print(commit)


# files = service.find_files_for_commit(
#     "a07356f8397f6ccb8f9a613ed945f8f4a3c36bfe"
# )

# for file in files:
#     print(file)   


commitss = service.find_issue_commits(38686)

for commit in commitss:
    print(commit)     


# filess = service.find_issue_changes(38686)

# for file in filess:
#     print(file)    