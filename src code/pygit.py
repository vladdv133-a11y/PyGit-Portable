import sys
import argparse
from repo import GitRepo

parser = argparse.ArgumentParser(
    prog="Pygit", description="A simple git client written in Python"
)
commands_parser = parser.add_subparsers(title="Commands", dest="command")
commands_parser.required = True

init_parser = commands_parser.add_parser("init")
init_parser.add_argument("path", metavar="directory", nargs="?", default=".")

cat_parser = commands_parser.add_parser("cat-file")
cat_parser.add_argument(
    "type", metavar="type", choices=["blob", "commit", "tag", "tree"]
)
cat_parser.add_argument("object", metavar="object")

log_parser = commands_parser.add_parser("log")
log_parser.add_argument("commit", default="HEAD", nargs="?")

hash_object_parser = commands_parser.add_parser(
    "hash-object",
    help="Computes an objects ID and optionally creates a blob from a file",
)
hash_object_parser.add_argument(
    "-t",
    metavar="type",
    dest="type",
    choices=["blob", "commit", "tag", "tree"],
    default="blob",
)
hash_object_parser.add_argument("-w", dest="write", action="store_true")
hash_object_parser.add_argument("path", help="Read object from <file>")


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    match args.command:
        case "init":
            GitRepo(args.path, create=True)
        case "add":
            pass
        case "cat-file":
            repo = GitRepo(".")
            repo.cat_file(args.object, args.type.encode())
        case "hash-object":
            repo = GitRepo(".")
            hash = repo.hash_object(args.path, args.type.encode(), args.write)
            print(hash)
        case "log":
            repo = GitRepo(".")
            repo.print_log(repo.find_object(args.commit), set())
        case _:
            print(f"Unrecognized git command '{args.commands}'")
