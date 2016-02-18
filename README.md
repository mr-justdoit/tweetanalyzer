# tweetanalyzer

## Command Examples

1, Get words from tweets and generate simple statistics as YAML. 

```
$ ./tweetanalyzer -q "from:@NASA" -t t -c 100
```

2, Get media files from @NASA.

```
$ ./tweetanalyzer.py -q "from:@NASA" -t m -c 100 | parallel --gnu "wget {}"
```

3, Get japanese words from tweets and generate simple statistics.
```
$ ./tweetanalyzer.py -q "japan" -t j -c 100
```


## License
This software is released under the MIT License, see LICENSE.