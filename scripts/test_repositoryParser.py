from app.parsing.repository_parser import RepositoryParser


def main():

    parser = RepositoryParser()

    result = parser.parse_repository(
        "data/repositories/langchain.git"
    )

    print(f"Files Parsed: {len(result['files'])}")

    print(result["files"][0])


if __name__ == "__main__":
    main()