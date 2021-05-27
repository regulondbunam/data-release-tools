import identifiers_api

identifiers_api.connect("mongodb://pablo:pablo@localhost:27017/identifiers")

identifiers_api.multigenomic.get_identifiers("multigenomic", "gene")

new_dicct = {
    "hola": "adios"
}

print(new_dicct.popitem())