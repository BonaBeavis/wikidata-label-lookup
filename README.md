# Wikidata Label Lookup

A short script to replace Wikidata URLs with their label.

#### Before

```sparql
SELECT ?item ?pic
WHERE {
    ?item wdt:P31 wd:Q146 .
    ?item wdt:P18 ?pic
}
```

#### After

```sparql
SELECT ?item ?pic
WHERE {
    ?item <instance of> <house cat> .
    ?item <image> ?pic
}
```

## Usage

### Terminal
```sh
echo wdt:P31 | ./wikidata-label-lookup.py
```

### Vim

To replace all URLs in current buffer:

```vim
:%!./wikidata-label-lookup.py
```
