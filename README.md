Write the [pytorch_pfn_extras](https://github.com/pfnet/pytorch-pfn-extras/blob/master/docs/config.md)'s config in Python syntax.

For example, the following yaml config

```yaml
name:
  type: concat
  x0: 'First'
  x1:
    type: concat
    x0: 'Middle'
    x1: 'Last'
```

will be

```python
name = concat(x0="First", x1=concat(x0="Middle", x1="Last"))
```
