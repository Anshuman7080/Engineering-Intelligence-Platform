from app.git.git_history_parser import GitHistoryParser

parser = GitHistoryParser()
print("loading commits")

commits = parser.parse(
    "data/repositories/langchain.git"
)

print(f"Total Commits : {len(commits)}")
print()

first = commits[0]

print("Hash :", first["hash"])
print("Author :", first["author"])
print("Email :", first["email"])
print("Date :", first["date"])
print("Message :", first["message"])

print()

print("Changed Files:")

for file in first["files"]:
    print(file)