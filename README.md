# PyVCF. What are you doing?


### Requirements

* `python3.9`
* `pipenv`


### Install
```
# In the project directory
python3.9 -m pipenv install
```

### Test
```
pipenv run pytest
```


### Inconsistent `vcf.Reader.fetch()`?

See `test_vcf_record_fetch.py`


#### Description

If the VCF has no records for a specified range, but has records for that contig outside that range, `vcf.Reader.fetch()` returns an empty iterator, indicating zero records were found.

If the VCF has no records at all for that contig, the same `vcf.Reader.fetch()` will raise a `ValueError` with message `could not create iterator for Region '<CHROM>:<START>-<END>'`...

```
  File "pysam/libctabix.pyx", line 509, in pysam.libctabix.TabixFile.fetch
ValueError: could not create iterator for region 'Chr10:100000-100000'
```

