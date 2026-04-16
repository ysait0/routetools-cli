# routetools-cli

[English](README.md)

- [routetools-cli](#routetools-cli)
  - [インストール](#インストール)
  - [オプション](#オプション)
  - [使い方](#使い方)
    - [フォーマット変換](#フォーマット変換)
      - [例](#例)
    - [POI追加 -- 他のルートファイルから](#poi追加----他のルートファイルから)
      - [例](#例-1)
    - [POI追加 -- CSVファイルから](#poi追加----csvファイルから)
      - [例](#例-2)
    - [POI追加 -- Google My Mapsを使う](#poi追加----google-my-mapsを使う)
      - [1. Google My Mapsの新しいレイヤーにルートファイルをインポート](#1-google-my-mapsの新しいレイヤーにルートファイルをインポート)
      - [2. レイヤーにPOIを追加](#2-レイヤーにpoiを追加)
      - [3. KMLまたはKMZでエクスポート](#3-kmlまたはkmzでエクスポート)
      - [4. `routetools-cli` で変換](#4-routetools-cli-で変換)
  - [ファイルフォーマット](#ファイルフォーマット)
    - [CSV](#csv)
      - [例](#例-3)
  - [ライセンス](#ライセンス)

`routetools-cli` はルートファイル用のCLIツールです。Garmin、Wahoo、Bryton、Pioneerなどのサイクリング用GPSデバイス向けに、フォーマット変換やPOIの追加・削除ができます。

ターミナルで `routetools` または `routetools-cli` コマンドとして使用します。

> **ブラウザ版もあります**: [routetools-webapp](https://ysait0.github.io/routetools-webapp/) — インストール不要でブラウザから直接利用できます。([リポジトリ](https://github.com/ysait0/routetools-webapp))

## インストール

```bash
git clone https://github.com/ysait0/routetools-cli.git
pip install ./routetools-cli
```

または

```bash
pip install git+https://github.com/ysait0/routetools-cli.git
```

## オプション

|          オプション           | 説明                                                                               |
| :---------------------------: | ---------------------------------------------------------------------------------- |
|      `-v`, `--version`        | バージョンを表示。                                                                  |
|       `-i`, `--input`         | 入力ルートファイル (*.gpx, *.kml, *.kmz, *.tcx)。                                  |
| `-r`, `--remove-original-poi` | 元のPOIを削除。デフォルトは False。                                                  |
|         `-p`, `--poi`         | インポートするPOIソースファイル (*.csv, *.gpx, *.kml, *.kmz, *.tcx)。              |
|      `-t`, `--out-type`       | 出力タイプ。デフォルトは TCX。                                                       |
|         `--tolerance`         | POI追加時の許容距離。デフォルトは 100 m。                                            |
|       `-f`, `--force`         | ルート上の最近傍点にPOIを強制配置。出力タイプがTCXの場合は常に強制。                   |
|          `--indent`           | インデントのスペース数。デフォルトは 1。                                              |
|       `-o`, `--output`        | 出力ルートファイルパス。                                                             |
|        `--output-poi`         | POIをCSV形式で出力。                                                                |

## 使い方

### フォーマット変換

`routetools-cli` を使ってファイルフォーマットを変換できます。

対応入力フォーマット:

- GPX
- KML
- KMZ
- TCX

対応出力フォーマット:

- GPX
- TCX

#### 例

```bash
### GPX -> TCX
routetools -i route.gpx -o route_new.tcx

### TCX -> GPX -- POI削除
routetools -i route.tcx -r -t GPX -o route_new.gpx

### KML -> GPX
routetools -i route.kml -t GPX -o route_new.gpx
```

### POI追加 -- 他のルートファイルから

他のルートファイルからPOIをインポートして、ベースのルートファイルに追加します。

#### 例

```bash
### route_ref.gpx のPOIを route_base.tcx に追加
routetools -i route_base.tcx -p route_ref.gpx -o route_new.tcx

### 元のPOIを削除し、route_ref.kml からPOIをインポートして追加
routetools -i route_base.gpx -r -p route_ref.kml -t GPX -o route_new.gpx
```

### POI追加 -- CSVファイルから

CSVファイルからPOIをインポートして、ベースのルートファイルに追加します。

#### 例

```bash
### TCX -> TCX -- CSVファイルからPOIを追加
routetools -i route_base.tcx -p poi.csv -o route_new.tcx

### GPX -> TCX -- 元のPOIを削除し、CSVファイルからPOIを追加
routetools -i route_base.gpx -r -p poi.csv -o route_new.tcx
```

### POI追加 -- Google My Mapsを使う

Google My Maps を使うと簡単にPOIを追加できます。

以下の手順に従ってください。

#### 1. Google My Mapsの新しいレイヤーにルートファイルをインポート

Google My Maps は TCX をサポートしていません。

TCXファイルしかない場合は、先に変換してください。

```bash
### TCX -> GPX
routetools -i route_base.tcx -t GPX -o route_new.gpx
```

#### 2. レイヤーにPOIを追加

#### 3. KMLまたはKMZでエクスポート

#### 4. `routetools-cli` で変換

```bash
### KML -> TCX
routetools -i route_base.kml -o route_new.tcx --tolerance 150

### KMZ -> GPX
routetools -i route_base.kmz -t GPX -o route_new.gpx
```

## ファイルフォーマット

### CSV

```csv
(緯度),(経度),(POI名),(説明),(タイプ)
```

|  キー  |   値     |
| :----: | :------: |
|  緯度  | 必須     |
|  経度  | 必須     |
| POI名  | 必須     |
|  説明  | 必須     |
| タイプ | 任意     |

#### 例

```csv
35.68249921156559,139.77653207620816,PC1,セブンイレブン日本橋１丁目昭和通り店
35.54219882219259,139.76194900229007,通過チェック1,多摩川スカイブリッジ,Generic
```

## ライセンス

このリポジトリは MIT License のもとで公開されています。詳細は LICENSE を参照してください。
