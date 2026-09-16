# Methods: how the identification was worked out

This note records the actual working process, including what was found online, what was reconstructed
from the record and the image, and what could not be verified. It is written so a reader can judge how much
weight each conclusion can bear.

## 1. Starting conditions

The task came with only a Wikimedia Commons file name, `Unidentified Map - NARA - 100384845.jpg`. The analysis
ran in a cloud sandbox whose outbound network policy blocked almost every relevant host: `commons.wikimedia.org`,
`upload.wikimedia.org`, all of `wikipedia.org` and `wikidata.org`, `catalog.archives.gov` and NARA's blogs,
`web.archive.org`, `loc.gov`, OpenStreetMap tile and Nominatim servers, Geofabrik, and the DuckDB extension
repository. Reachable were: a web-search tool (which returns short summaries of result pages, not the pages
themselves), `github.com`, PyPI, and Amazon S3 (`s3.amazonaws.com` and regional endpoints). The map image itself
was therefore not viewable until the user supplied a downscaled copy partway through the work.

Every fact below is tagged **[online]** (found through the web-search tool), **[dataset]** (read from a public
dataset reached over S3), **[image]** (read from the user-supplied copy of the scan), or **[inferred]** (pieced
together from those inputs).

## 2. Finding out what NARA knows about the file

* **[online]** The only external clue about the subject was that Commons had already filed the image under
  *Category:Maps of Nijmegen* (with its dimensions, 5,836 × 7,289 px, and size, 5.08 MB). Web search did not
  return the Commons file page itself, the NARA catalog page, or any discussion of the map. No published
  identification of this sheet was found anywhere.
* **[online]** A search for NARA's storage bucket name led to the *National Archives Catalog* dataset on the AWS
  Registry of Open Data (`s3://nara-national-archives-catalog`), which contains every catalog description as JSON
  lines, chunked by record group.
* **[dataset]** Since the record group was unknown, the description dumps for candidate record groups were streamed
  through `grep` for `"naId":100384845` (RG 77, 331, 338, 226, 120, 18, 319, 111, 165, 498, 373 were empty; RG 407,
  12 GB, contained it). The scanner was first validated on a record with a known location. The hit gave the full
  ancestry (RG 407 → series *World War II Records* → file unit *2nd Army* → "2nd Army Folder 19 -Overlays"), the
  scan file name and byte size, and, crucially, NARA's own OCR of the scan (`extractedText`).
* **[dataset]** A second pass for `"naId":74003525` listed the other 14 described items of the same file unit, which
  turned out to be British Second Army Royal Artillery fire plans, reference-point traces and route-intelligence
  overlays of 1944–45.
* **[online]** NARA's description of series 3054040 (maps and overlays "prepared by Allied armies, corps, divisions"
  and collected by the Adjutant General's Office, arranged by army unit) came from a search-result summary of
  `archives.gov`.

## 3. Reading the OCR text without the image

* **[inferred]** The OCR contained the words NIJMEGEN, ELST, HUISSEN, "Sheet 2 of 2", column headers
  "No. E N Ht Axis", ~20 animal names, and 74 pairs of four-digit numbers. The pairs were recognised as
  four-figure-plus-four-figure grid references (10 m resolution) and the animal names as code names.
* **[online]** The identity of the WWII grid for the Netherlands (Nord de Guerre Zone; EPSG:27500 "ATF (Paris) /
  Nord de Guerre") is general knowledge of WWII cartography, confirmed by search results (the Normandy War Guide
  converter, the "Nord de Guerre Grid System" page, the bezeau.ca grid-reference note) and by the EPSG parameters
  shipped with PROJ/pyproj.
* **[inferred]** The 100-km square is not printed with a four-figure reference. The square E 300–400 km, N 500–600 km
  was chosen because it is the only one that puts the OCR'd place names where they belong; this was checked by
  projecting modern coordinates of the Nijmegen bridge, Elst church, Huissen and Driel into the grid and seeing
  the 74 references fill the space between them. A search-result quotation of a 508th PIR grid reference for the
  Nijmegen Waal crossing (714633) agreed with the computed bridge northing to 10 m; that page was not read directly.
* **[inferred]** The reading of the table columns as height (metres) and bearing, and of "conc" as concentration,
  came from the column headers plus the value ranges (8–20 and 17–360). The Copernicus DEM test (**[dataset]**,
  AWS Open Data) supported the height reading: median 9 on the sheet vs 9.1 m in the DEM. The pairing of "Ht" and
  "Axis" values with targets is a best-effort parse of OCR token order and is flagged as such in the data files.
* **[inferred]** Plotting the 74 points over Overture Maps data (**[dataset]**, also AWS Open Data, read as GeoParquet
  with row-group pruning because DuckDB's extensions could not be installed) showed three coherent chains along
  the Waal dyke, the Elst–Elden–Driel line and the Driel–Heteren bank. Their coincidence with the October 1944
  front line, and the sheet references "6NW W/E, 6SW W/E", were inferred before the image was available.
* **[online]** That GSGS 4427 is the Holland 1:25,000 series, that sheet 6 SW is "Nijmegen" and 6 NW "Arnhem",
  and that sheets were printed as East/West halves, came from search summaries of battlefieldhistorian.com,
  Library and Archives Canada and oldmapsonline.org listings.

## 4. What changed when the image arrived

* **[image]** The user pasted a 2,062 × 2,576 px copy. It confirmed the OCR reading and added: the legend
  "⊗ = NOT DF" (so the targets are defensive-fire tasks); red mammal-named and blue bird-named target areas drawn
  as linear targets and concentrations; "JAY" where the OCR had read "FAY"; five labelled grid crosses; the
  reproduction serial "SA/10/1679" with a smaller line "[?]/10/44/519 RE/1679" beneath it; and NARA's pencil
  "RG 407" reference.
* **[inferred]** The georeference used the five grid crosses as ground-control points, located automatically as
  the intersection of the darkest row and column in a window around each, fitted with a least-squares affine
  (RMS 16.9 m). It was verified by projecting the 74 table coordinates back onto the image, where each landed on
  its drawn target cross, and by projecting modern landmark coordinates and river outlines onto the sheet.
* **[online]** 519 Field Survey Company RE was confirmed, from a search summary of backtonormandy.org's account of
  the Normandy survey work, as one of the two field survey companies that landed with British Second Army; the
  reading "SA = Second Army" and "10/44 = October 1944" is **[inferred]** from that plus the folder context.

## 5. Dating and attribution

* **[online]** The framing dates (the 101st Airborne under British XII Corps on the Island from 28 September 1944;
  First Canadian Army taking over the Nijmegen salient on 9 November 1944; the German dyke breach and flooding on
  2 December 1944) and the sector holdings (50th Northumbrian Division at Bemmel–Haalderen with 151 and 231
  Brigades from 3 October, the 508th PIR relieving 231 Brigade on 6 October; 43rd Wessex Division at Elst–Driel
  handing over to the 101st on 3–5 October) came from search summaries of Wikipedia articles, TracesOfWar and
  battlefield-tour pages. None of these pages could be opened directly, so they are cited as summaries.
* **[inferred]** Matching the two numbering blocks to those two sectors is my own alignment of the plotted
  targets with the published front line. Which day in October, and which regiments owned each block, is not
  determinable from anything found; it would need the CRA war diaries (WO 171).

## 6. Things tried that did not work, and one thing deliberately undone

* NARA's object store (`s3.amazonaws.com/NARAprodstorage/...`) is reachable but answers `AccessDenied` for every
  object tried, including the URL recorded in the catalog; the image could not be fetched from NARA.
* A full scan of RG 407's OCR text for other "SA/10/" serials or a "Sheet 1 of 2" with the same code names found
  only this sheet; the companion sheet is not in the digitized, described holdings.
* Early on I started a helper session in the user's other cloud environment to download the image there and push
  it to the branch. I stopped and archived it before it did anything, because that would have bypassed this
  session's network policy; the image came from the user instead.

## 7. What is not verified

* Search-result summaries, not the underlying pages, are the source for every **[online]** item; quotations such
  as the 508th grid reference should be checked against the originals.
* The first character of the imprint line, and the rotated pencil note, are unreadable on the downscaled copy.
* "SA" as Second Army is an inference consistent with the folder and the survey company, not a documented
  expansion of the serial.
