# routetools-cli

- [routetools-cli](#routetools-cli)
  - [:warning: Information](#warning-information)
  - [Install](#install)
  - [Options](#options)
  - [Usage](#usage)
    - [Convert](#convert)
      - [Examples](#examples)
    - [Add POI -- using other route file](#add-poi----using-other-route-file)
      - [Examples](#examples-1)
    - [Add POI -- using csv file](#add-poi----using-csv-file)
      - [Examples](#examples-2)
    - [Add POI -- using Google My Maps](#add-poi----using-google-my-maps)
      - [1. Import route file to the new layer on Google My Maps](#1-import-route-file-to-the-new-layer-on-google-my-maps)
      - [2. Add POI to the layer](#2-add-poi-to-the-layer)
      - [3. Export the layer with KML or KMZ](#3-export-the-layer-with-kml-or-kmz)
      - [4. Convert the file with `routetools-cli`](#4-convert-the-file-with-routetools-cli)
  - [File Format](#file-format)
    - [CSV](#csv)
      - [Examples](#examples-3)
  - [License](#license)

`routetools-cli` is tool for route files, it enables us to convert, add POI, remove POI.

We use it via `routetools` or `routetools-cli` in terminal.

---

## :warning: Information

This project is under development and I'm testing on Pioneer SGX-CA600 only.

I would like to test it on other hardware such as Garmin, Wahoo, Bryton, etc.

I would be grateful if you could help me with the test.

Thank you.

---

## Install

```bash
git clone https://github.com/ysait0/routetools-cli.git
pip install ./routetools-cli
```

or

```bash
pip install git+https://github.com/ysait0/routetools-cli.git
```

## Options

|            Options            | Description                                                                       |
| :---------------------------: | --------------------------------------------------------------------------------- |
|      `-v`, `--version`        | Show version.                                                                     |
|       `-i`, `--input`         | Input base route filepath (*.gpx, *.kml, *.kmz, *.tcx).                          |
| `-r`, `--remove-original-poi` | Remove original POI from base route. Default is False.                            |
|         `-p`, `--poi`         | POI source filepath to import (*.csv, *.gpx, *.kml, *.kmz, *.tcx).              |
|      `-t`, `--out-type`       | Output type. Default is TCX.                                                      |
|         `--tolerance`         | Tolerance to add POI. Default is 100 m.                                           |
|       `-f`, `--force`         | Force POI add nearest point on route. If out-type is TCX, it is always force.     |
|          `--indent`           | Number of spaces for indentation. Default is 1.                                   |
|       `-o`, `--output`        | Output route filepath.                                                            |
|        `--output-poi`         | Output POI in csv format.                                                         |

## Usage

### Convert

Convert file formats to each other using `routetools-cli`.

Available Input Types:

- GPX
- KML
- KMZ
- TCX

Available Output Types:

- GPX
- TCX

#### Examples

```bash
### GPX -> TCX
routetools -i route.gpx -o route_new.tcx

### TCX -> GPX -- Remove POI
routetools -i route.tcx -r -t GPX -o route_new.gpx

### KML -> GPX
routetools -i route.kml -t GPX -o route_new.gpx
```

### Add POI -- using other route file

Import POI from other route file and Add them into base route file.

#### Examples

```bash
### Add POI imported from route_ref.gpx to route_base.tcx
routetools -i route_base.tcx -p route_ref.gpx -o route_new.tcx

### Remove original POI in base route file and Add POI imported from route_ref.kml
routetools -i route_base.gpx -r -p route_ref.kml -t GPX -o route_new.gpx
```

### Add POI -- using csv file

Import POI from csv file and Add them into base route file.

#### Examples

```bash
### TCX -> TCX -- Add POI imported from csv file
routetools -i route_base.tcx -p poi.csv -o route_new.tcx

### GPX -> TCX -- Remove original POI and ADD POI imported from csv file
routetools -i route_base.gpx -r -p poi.csv -o route_new.tcx
```

### Add POI -- using Google My Maps

The easiest way to add POI is using Google My Maps.

Please follow the steps below.

#### 1. Import route file to the new layer on Google My Maps

Google My Maps doesn't support TCX.

Please convert first when you only have TCX file.

```bash
### TCX -> GPX
routetools -i route_base.tcx -t GPX -o route_new.gpx
```

#### 2. Add POI to the layer

#### 3. Export the layer with KML or KMZ

#### 4. Convert the file with `routetools-cli`

```bash
### KML -> TCX
routetools -i route_base.kml -o route_new.tcx --tolerance 150

### KMZ -> GPX
routetools -i route_base.kmz -t GPX -o route_new.gpx
```

## File Format

### CSV

```csv
(Latitude),(Longitude),(Name of POI),(Description),(Type)
```

|    keys     |  value   |
| :---------: | :------: |
|  Latitude   | required |
|  Longitude  | required |
| Name of POI | required |
| Description | required |
|    Type     | optional |

#### Examples

```csv
35.68249921156559,139.77653207620816,PC1,セブンイレブン日本橋１丁目昭和通り店
35.54219882219259,139.76194900229007,通過チェック1,多摩川スカイブリッジ,Generic
```

## License

This repository is released under the MIT License, see LICENSE.
