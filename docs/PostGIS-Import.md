## postgis setup

#### prerequisites:
- postgresql & postgis
- [imposm](https://github.com/omniscale/imposm3)
- [data](https://download.geofabrik.de/) to import

#### why imposm?
ram usage: (rpi3b+) <br>

|    tool   |                   cmd                                                                          | usage         |
|-----------|------------------------------------------------------------------------------------------------|---------------|
| osm2pgsql | osm2pgsql -c -s -C 500 -d gis bayern-latest.osm.pbf                                            | 100%          |
| osm2pgsql | osm2pgsql -c -s -C 25 -d gis bayern-latest.osm.pbf                                             | 100%          |
| imposm    | imposm --read --write --optimize -h localhost -p 5432 -U postgres -d gis bayern-latest.osm.pbf | ~25%          |

#### setup:

1. create user and database [(from the imposm3 documentation)](https://imposm.org/docs/imposm3/latest/tutorial.html)
```shell
sudo su postgres
createuser --no-superuser --no-createrole --createdb osm
createdb -E UTF8 -O osm osm
psql -d osm -c "CREATE EXTENSION postgis; CREATE EXTENSION hstore;"
echo "ALTER USER osm WITH PASSWORD 'osm';" |psql -d osm
```

2. import data 
```shell
# this should be executed in screen or tmux session since it can take a while
# you might need to append -overwritecache or -appendcache if the data has been already imported

imposm import -optimize -deployproduction -write -connection postgis://osm:osm@localhost/osm -read /path/to/my/mapexport.osm.pbf -mapping mappings/example-mapping.yml

[2021-12-28T14:29:24+01:00] 0:00:00 [info] removing existing cache /tmp/imposm3
[2021-12-28T14:29:24+01:00] 0:00:00 [step] Starting: Imposm
[2021-12-28T14:29:24+01:00] 0:00:00 [step] Starting: Reading OSM data
[2021-12-28T14:29:24+01:00] 0:00:00 [info] reading /media/safe/maps/germany-latest.osm.pbf with data till 2021-10-09 22:21:28 +0200 CEST
[2021-12-28T14:30:24+01:00] 0:01:00 [progress]   1m0s C: 2055000/s (123200000) N:   39600/s (2378688) W:       0/s (0) R:      0/s (0)
[2021-12-28T14:31:24+01:00] 0:02:00 [progress]   2m0s C: 2732000/s (327792000) N:   52400/s (6291237) W:       0/s (0) R:      0/s (0)
[2021-12-28T14:32:07+01:00] 0:02:43 [progress]  2m43s C: 2917000/s (349953025) N:   55800/s (6701417) W:       0/s (57145484) R:      0/s (524106)
[2021-12-28T14:32:07+01:00] 0:02:43 [step] Finished: Reading OSM data in 2m43.390308461s
[2021-12-28T14:32:07+01:00] 0:02:43 [step] Starting: Importing OSM data
[2021-12-28T14:32:07+01:00] 0:02:43 [step] Starting: Writing OSM data
[2021-12-28T14:33:07+01:00] 0:03:43 [progress]   1m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:       0/s ( 0.0%) R:    440/s ( 5.0%)
[2021-12-28T14:34:07+01:00] 0:04:43 [progress]   2m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:       0/s ( 0.0%) R:    820/s (18.7%)
[2021-12-28T14:35:07+01:00] 0:05:43 [progress]   3m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:       0/s ( 0.0%) R:   1000/s (34.4%)
[2021-12-28T14:36:07+01:00] 0:06:43 [progress]   4m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:       0/s ( 0.0%) R:   1310/s (59.7%)
[2021-12-28T14:37:07+01:00] 0:07:43 [progress]   5m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:       0/s ( 0.0%) R:   1500/s (85.8%)
[2021-12-28T14:38:07+01:00] 0:08:43 [progress]   6m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   28000/s ( 1.5%) R:   1460/s (100.0%)
[2021-12-28T14:39:07+01:00] 0:09:43 [progress]   7m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   33400/s ( 5.3%) R:   1460/s (100.0%)
[2021-12-28T14:40:07+01:00] 0:10:43 [progress]   8m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   40200/s (10.6%) R:   1460/s (100.0%)
[2021-12-28T14:41:07+01:00] 0:11:43 [progress]   9m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   48800/s (18.0%) R:   1460/s (100.0%)
[2021-12-28T14:42:07+01:00] 0:12:43 [progress]  10m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   54600/s (25.9%) R:   1460/s (100.0%)
[2021-12-28T14:43:07+01:00] 0:13:43 [progress]  11m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   61600/s (35.6%) R:   1460/s (100.0%)
[2021-12-28T14:44:07+01:00] 0:14:43 [progress]  12m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   68700/s (47.0%) R:   1460/s (100.0%)
[2021-12-28T14:45:07+01:00] 0:15:43 [progress]  13m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   74800/s (59.0%) R:   1460/s (100.0%)
[2021-12-28T14:46:07+01:00] 0:16:43 [progress]  14m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   78700/s (70.3%) R:   1460/s (100.0%)
[2021-12-28T14:47:07+01:00] 0:17:43 [progress]  15m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   80200/s (80.1%) R:   1460/s (100.0%)
[2021-12-28T14:48:07+01:00] 0:18:43 [progress]  16m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   81500/s (89.9%) R:   1460/s (100.0%)
[2021-12-28T14:49:07+01:00] 0:19:43 [progress]  17m0s C:       0/s ( 0.0%) N:       0/s ( 0.0%) W:   82700/s (100.0%) R:   1460/s (100.0%)
[2021-12-28T14:49:26+01:00] 0:20:01 [step] Finished: Writing OSM data in 17m18.269062285s
[2021-12-28T14:49:26+01:00] 0:20:01 [step] Starting: Creating generalized tables
[2021-12-28T14:49:26+01:00] 0:20:01 [progress] 17m18s C:       0/s ( 0.0%) N:       0/s (100.0%) W:   82700/s (100.0%) R:   1460/s (100.0%)
[2021-12-28T14:49:26+01:00] 0:20:01 [step] Starting: Generalizing osm_roads into osm_roads_gen1
[2021-12-28T14:49:26+01:00] 0:20:01 [step] Starting: Generalizing osm_waterareas into osm_waterareas_gen1
[2021-12-28T14:49:26+01:00] 0:20:01 [step] Starting: Generalizing osm_waterways into osm_waterways_gen1
[2021-12-28T14:49:26+01:00] 0:20:01 [step] Starting: Generalizing osm_landusages into osm_landusages_gen1
[2021-12-28T14:49:28+01:00] 0:20:04 [step] Finished: Generalizing osm_waterareas into osm_waterareas_gen1 in 2.701102161s
[2021-12-28T14:49:34+01:00] 0:20:10 [step] Finished: Generalizing osm_waterways into osm_waterways_gen1 in 8.527418944s
[2021-12-28T14:50:01+01:00] 0:20:37 [step] Finished: Generalizing osm_roads into osm_roads_gen1 in 35.793931767s
[2021-12-28T14:50:17+01:00] 0:20:53 [step] Finished: Generalizing osm_landusages into osm_landusages_gen1 in 51.282162484s
[2021-12-28T14:50:17+01:00] 0:20:53 [step] Starting: Generalizing osm_waterareas into osm_waterareas_gen0
[2021-12-28T14:50:17+01:00] 0:20:53 [step] Starting: Generalizing osm_waterways into osm_waterways_gen0
[2021-12-28T14:50:17+01:00] 0:20:53 [step] Starting: Generalizing osm_landusages into osm_landusages_gen0
[2021-12-28T14:50:17+01:00] 0:20:53 [step] Starting: Generalizing osm_roads into osm_roads_gen0
[2021-12-28T14:50:17+01:00] 0:20:53 [step] Finished: Generalizing osm_waterareas into osm_waterareas_gen0 in 204.272702ms
[2021-12-28T14:50:21+01:00] 0:20:57 [step] Finished: Generalizing osm_waterways into osm_waterways_gen0 in 4.178242281s
[2021-12-28T14:50:22+01:00] 0:20:58 [step] Finished: Generalizing osm_roads into osm_roads_gen0 in 5.423770635s
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Finished: Generalizing osm_landusages into osm_landusages_gen0 in 7.34924557s
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Finished: Creating generalized tables in 58.631682719s
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry indices
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_barrierpoints
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_housenumbers_interpolated
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_amenities
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_roads_gen1
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_waterways
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_places
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_buildings
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_admin
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_transport_areas
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_barrierways
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_landusages
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_transport_points
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_housenumbers
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_roads
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_waterareas
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_aeroways
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_waterareas_gen0
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_waterareas_gen1
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_waterways_gen1
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_landusages_gen0
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_roads_gen0
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_landusages_gen1
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating OSM id index on osm_waterways_gen0
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Finished: Creating OSM id index on osm_waterareas_gen0 in 38.882576ms
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_waterareas_gen0
[2021-12-28T14:50:24+01:00] 0:21:00 [step] Finished: Creating geometry index on osm_waterareas_gen0 in 98.939833ms
[2021-12-28T14:50:25+01:00] 0:21:00 [step] Finished: Creating geometry index on osm_aeroways in 330.980048ms
[2021-12-28T14:50:25+01:00] 0:21:00 [step] Finished: Creating geometry index on osm_housenumbers_interpolated in 331.090053ms
[2021-12-28T14:50:25+01:00] 0:21:00 [step] Finished: Creating OSM id index on osm_waterareas_gen1 in 398.755541ms
[2021-12-28T14:50:25+01:00] 0:21:00 [step] Starting: Creating geometry index on osm_waterareas_gen1
[2021-12-28T14:50:27+01:00] 0:21:02 [step] Finished: Creating OSM id index on osm_landusages_gen0 in 2.483546181s
[2021-12-28T14:50:27+01:00] 0:21:02 [step] Starting: Creating geometry index on osm_landusages_gen0
[2021-12-28T14:50:27+01:00] 0:21:03 [step] Finished: Creating geometry index on osm_transport_areas in 2.825939542s
[2021-12-28T14:50:27+01:00] 0:21:03 [step] Finished: Creating geometry index on osm_amenities in 2.883932044s
[2021-12-28T14:50:27+01:00] 0:21:03 [step] Finished: Creating geometry index on osm_waterareas_gen1 in 2.500098593s
[2021-12-28T14:50:28+01:00] 0:21:03 [step] Finished: Creating geometry index on osm_admin in 3.390390089s
[2021-12-28T14:50:29+01:00] 0:21:04 [step] Finished: Creating OSM id index on osm_landusages_gen1 in 4.446908407s
[2021-12-28T14:50:29+01:00] 0:21:04 [step] Starting: Creating geometry index on osm_landusages_gen1
[2021-12-28T14:50:29+01:00] 0:21:05 [step] Finished: Creating geometry index on osm_places in 4.633089237s
[2021-12-28T14:50:29+01:00] 0:21:05 [step] Finished: Creating OSM id index on osm_waterways_gen1 in 4.698706742s
[2021-12-28T14:50:29+01:00] 0:21:05 [step] Starting: Creating geometry index on osm_waterways_gen1
[2021-12-28T14:50:29+01:00] 0:21:05 [step] Finished: Creating OSM id index on osm_roads_gen1 in 5.017040359s
[2021-12-28T14:50:29+01:00] 0:21:05 [step] Starting: Creating geometry index on osm_roads_gen1
[2021-12-28T14:50:30+01:00] 0:21:06 [step] Finished: Creating geometry index on osm_landusages_gen0 in 3.333258575s
[2021-12-28T14:50:30+01:00] 0:21:06 [step] Finished: Creating OSM id index on osm_waterways_gen0 in 6.324461324s
[2021-12-28T14:50:30+01:00] 0:21:06 [step] Starting: Creating geometry index on osm_waterways_gen0
[2021-12-28T14:50:31+01:00] 0:21:06 [step] Finished: Creating OSM id index on osm_roads_gen0 in 6.449893853s
[2021-12-28T14:50:31+01:00] 0:21:06 [step] Starting: Creating geometry index on osm_roads_gen0
[2021-12-28T14:50:47+01:00] 0:21:22 [step] Finished: Creating geometry index on osm_transport_points in 22.377044531s
[2021-12-28T14:50:47+01:00] 0:21:22 [step] Finished: Creating geometry index on osm_barrierpoints in 22.377148465s
[2021-12-28T14:50:47+01:00] 0:21:23 [step] Finished: Creating geometry index on osm_waterareas in 23.020657471s
[2021-12-28T14:50:52+01:00] 0:21:28 [step] Finished: Creating geometry index on osm_barrierways in 27.600896963s
[2021-12-28T14:51:18+01:00] 0:21:53 [step] Finished: Creating geometry index on osm_waterways_gen1 in 48.719712709s
[2021-12-28T14:51:22+01:00] 0:21:57 [step] Finished: Creating geometry index on osm_waterways_gen0 in 51.237533455s
[2021-12-28T14:51:23+01:00] 0:21:58 [step] Finished: Creating geometry index on osm_waterways in 58.554052626s
[2021-12-28T14:51:23+01:00] 0:21:59 [step] Finished: Creating geometry index on osm_landusages_gen1 in 54.637028611s
[2021-12-28T14:51:26+01:00] 0:22:02 [step] Finished: Creating geometry index on osm_roads_gen1 in 57.035952835s
[2021-12-28T14:51:28+01:00] 0:22:04 [step] Finished: Creating geometry index on osm_roads_gen0 in 57.308829528s
[2021-12-28T14:51:47+01:00] 0:22:22 [step] Finished: Creating geometry index on osm_housenumbers in 1m22.400824192s
[2021-12-28T14:52:34+01:00] 0:23:10 [step] Finished: Creating geometry index on osm_landusages in 2m10.208765155s
[2021-12-28T14:54:25+01:00] 0:25:01 [step] Finished: Creating geometry index on osm_roads in 4m1.26585781s
[2021-12-28T14:58:13+01:00] 0:28:48 [step] Finished: Creating geometry index on osm_buildings in 7m48.48312274s
[2021-12-28T14:58:13+01:00] 0:28:48 [step] Finished: Creating geometry indices in 7m48.483252052s
[2021-12-28T14:58:13+01:00] 0:28:48 [step] Finished: Importing OSM data in 26m5.384070362s
[2021-12-28T14:58:13+01:00] 0:28:48 [step] Finished: Imposm in 28m48.774442783s
```