def formatDocstr(docstr: str) -> str:
    return "".join([x.replace("    ", "") for x in docstr.split("\t")])
