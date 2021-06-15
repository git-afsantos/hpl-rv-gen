# HPL Runtime Monitor Generator

This package provides a runtime monitor generator for [HPL properties](https://github.com/git-afsantos/hpl-specs/).

## Installing

Installing a pre-packaged release:

```bash
pip install hpl-rv-gen
```

Installing from source:

```bash
git clone https://github.com/git-afsantos/hpl-rv-gen.git
cd hpl-rv-gen
pip install -e .
```

## Usage

When used as a library, you can generate Python code for a runtime monitor class with a few simple steps.
For example:

```python
from hpl.parser import property_parser
from hplrv.rendering import TemplateRenderer

p = property_parser()
r = TemplateRenderer()
input_property = 'globally: no (/a or /b)'
hpl_property = p.parse(input_property)
code = r.render_monitor(hpl_property)
print(code)
```

## Bugs, Questions and Support

Please use the [issue tracker](https://github.com/git-afsantos/hpl-rv-gen/issues).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md).

## Acknowledgment

Until March 2021, this work was financed by the ERDF – European Regional Development Fund through the Operational Programme for Competitiveness and Internationalisation - COMPETE 2020 Programme and by National Funds through the Portuguese funding agency, FCT - Fundação para a Ciência e a Tecnologia within project PTDC/CCI-INF/29583/2017 (POCI-01-0145-FEDER-029583).

