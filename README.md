# everlance2quickbooks

Convert an Everlance trip log into MileIQ format for import to QuickBooks Self Employment

- Inspired by https://rickmacgillis.com/import-everlance-mileage-quickbooks/2017/07/22/
- Experiment with a few personal trips, because QuickBooks will ignore them

- IMPORTANT: Update the "IRS_MILES = 0.535" (as of 2017)


## Disclaimer

Use at your own risk.  Double check all your entries.

Copyright 2017 Darren Weber

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this repository content except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


# Usage

```bash
cat Everlance-trips.csv | ./everlance2mileIQ.py
```

Filter results with `grep`, e.g.
```
cat Everlance-trips.csv | ./everlance2mileIQ.py > MileIQ-trips.csv
cat Everlance-trips.csv | ./everlance2mileIQ.py | grep 'Personal' > MileIQ-trips-personal.csv
cat Everlance-trips.csv | ./everlance2mileIQ.py | grep 'Business' > MileIQ-trips-business.csv
# Add the header back to the filtered files
cat fixtures/mileIQ_header.csv MileIQ-trips-personal.csv > tmp.csv
mv tmp.csv MileIQ-trips-personal.csv 
cat fixtures/mileIQ_header.csv MileIQ-trips-business.csv > tmp.csv
mv tmp.csv MileIQ-trips-business.csv 
```


## Data Interpretation

- From https://rickmacgillis.com/import-everlance-mileage-quickbooks/2017/07/22/
  - paraphrased here in case the blog post disappears
  - the python utility does these conversions


"START_DATE" and "END_DATE" – The starting date-time and ending date-time for a
trip. Everlance uses a single date for all trips, and two time columns for the
start and stop times.

"CATEGORY" – This column needs to say "Business" for any trips marked as
"Work".

"START" and "STOP" – These are your starting address and ending address. You can
use any address format for them.

"MILES" – This column shows how many miles were driven. It must be a number.

"MILES_VALUE" – This column shows how many dollars credit the IRS will give you
for the miles. It must be a number, and must not include the "$" or other text.

"PARKING” – This column shows the cost paid for parking, if any. In most cases,
it is assumed to be zero, as Everlance export has no value for this.
Quickbooks Self employed doesn't take that into account, but it could
be added later as a transaction (not a trip).

"TOLLS" – As with "PARKING," it can be all 0s, and Quickbooks ignores it.

"TOTAL" – This column is the total of "MILES_VALUE" + "PARKING" + "TOLLS."

"VEHICLE" – Quickbooks Self employed only imports this
data into your existing car, so the name of the car is not important.

"PURPOSE" – This column needs to match "CATEGORY" exactly.

"NOTES" – Just leave it blank, as Quickbooks doesn’t use it.

