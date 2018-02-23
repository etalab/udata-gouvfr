# Changelog

## Current (in progress)

- Make use of [udata pytest plugin](https://github.com/opendatateam/udata#1400) [#254](https://github.com/etalab/udata-gouvfr/pull/254)
- Expose new entrypoints. Plugins and theme translations are now splitted [#263](https://github.com/etalab/udata-gouvfr/pull/263)
- Align card components design [#252](https://github.com/etalab/udata-gouvfr/pull/252)
- Discourse timeout and response parse error catch [#267](https://github.com/etalab/udata-gouvfr/pull/267)
- Add tracking on home page call to action [#271](https://github.com/etalab/udata-gouvfr/pull/271)

## 1.2.5 (2018-02-05)

- Small fixes on search facets related to [opendatateam/udata#1410](https://github.com/opendatateam/udata/pull/1410) [#255](https://github.com/etalab/udata-gouvfr/pull/255)

## 1.2.4 (2018-01-24)

- Licenses: Update SHOM attachment + fix BAN URL [#249](https://github.com/etalab/udata-gouvfr/pull/249)

## 1.2.3 (2018-01-17)

- Add the homologation of CC-BY-SA for SHOM [#244](https://github.com/etalab/udata-gouvfr/pull/244/files)
- Dataset recommendations [#243](https://github.com/etalab/udata-gouvfr/pull/243)
- Move some discussions style into `udata` core [#251](https://github.com/etalab/udata-gouvfr/pull/251)

## 1.2.2 (2017-12-14)

- Export CSS dropdown behavior to `udata` [#234](https://github.com/etalab/udata-gouvfr/pull/234)
- Remove internal FAQ and switch to [doc.data.gouv.fr](https://doc.data.gouv.fr) [#236](https://github.com/etalab/udata-gouvfr/issues/236)

## 1.2.1 (2017-12-06)

- Export community resource avatar style to udata [#233](https://github.com/etalab/udata-gouvfr/pull/233)
- Drop the `terms.html` template. Terms and conditions are now externalized and use the udata core template. (See [udata#1285](https://github.com/opendatateam/udata/pull/1285)) [#232](https://github.com/etalab/udata-gouvfr/pull/232)

## 1.2.0 (2017-10-20)

- Use new search blueprint from uData [#224](https://github.com/etalab/udata-gouvfr/pull/224)

## 1.1.2 (2017-09-04)

- Fixes some spacing issues on dataset and reuses page buttons
  [#209](https://github.com/etalab/udata-gouvfr/pull/209)
- Fix some wrong spatial coverages
  [#213](https://github.com/etalab/udata-gouvfr/pull/213)
- Fix translations collision on contact [#211](https://github.com/etalab/udata-gouvfr/pull/211) [#212](https://github.com/etalab/udata-gouvfr/pull/212)
- Updated some translations

## 1.1.1 (2017-07-31)

- Updated translations

## 1.1.0 (2017-07-05)

- Use the new entrypoint-based theme management
  [#164](https://github.com/etalab/udata-gouvfr/pull/164)
- Adjust the dataset reuses title overflow for proper display
  [#172](https://github.com/etalab/udata-gouvfr/pull/172)
- Drop glyphicons, remove some useless classes and upgrade to bootstrap 3.3.7
  [#177](https://github.com/etalab/udata-gouvfr/pull/177)
- Use the core publish action modal
  [#178](https://github.com/etalab/udata-gouvfr/pull/178)
- Fix the deuil header not being an SVG
  [#180](https://github.com/etalab/udata-gouvfr/pull/180)
- Integrating latest versions of GeoZones and GeoLogos for territories.
  Especially using history of towns, counties and regions from GeoHisto.
  [#499](https://github.com/opendatateam/udata/issues/499)
- Add the missing placeholders
  [#194](https://github.com/etalab/udata-gouvfr/pull/194)
- Use the `udata.harvesters` entrypoint
  [#195](https://github.com/etalab/udata-gouvfr/pull/195)
- Revamp actionnable tabs
  [#189](https://github.com/etalab/udata-gouvfr/pull/189)
- Remove `.btn-more` class
  [#191](https://github.com/etalab/udata-gouvfr/pull/191)

## 1.0.9 (2017-06-28)

- Nothing yet

## 1.0.8 (2017-06-21)

- Fixed a typo
  [#182](https://github.com/etalab/udata-gouvfr/pull/182)

## 1.0.7 (2017-06-20)

- Added a Licences page
  [#181](https://github.com/etalab/udata-gouvfr/pull/181)

## 1.0.6 (2017-04-18)

- Fixed numbering in system integrator FAQ (thanks to Bruno Cornec)
  [#174](https://github.com/etalab/udata-gouvfr/pull/174)
- Added a footer link to the SPD page
  [#176](https://github.com/etalab/udata-gouvfr/pull/176)

## 1.0.5 (2017-04-06)

- Added a missing translation
- Alphabetical ordering on SPD datasets

## 1.0.4 (2017-04-05)

- Introduce SPD page and badge

## 1.0.3 (2017-02-27)

- Translations update
- Switch `udata-js` link to `metaclic` [#161](https://github.com/etalab/udata-gouvfr/pull/161)

## 1.0.2 (2017-02-21)

- Optimize png images from theme [#159](https://github.com/etalab/udata-gouvfr/issues/159)
- Optimize png images sizes for territory placeholders [#788](https://github.com/opendatateam/udata/issues/788)

## 1.0.1 (2017-02-20)

- Ensure missing FAQ sections raises a 404 [#156](https://github.com/etalab/udata-gouvfr/issues/156)
- Provide deep PyPI versions links into the footer [#155](https://github.com/etalab/udata-gouvfr/pull/155)
- Provide proper cache versionning for theme assets [#155](https://github.com/etalab/udata-gouvfr/pull/155)

## 1.0.0 (2017-02-16)

- Remove some main menu entries (events, CADA, Etalab)
- Use a new SVG logo
- Apply changes from [uData 1.0.0](https://pypi.python.org/pypi/udata/1.0.0#changelog)

## 0.9.1 (2017-01-10)

- First published release
