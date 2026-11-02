# Data Dictionary: General International Airport operations database (fictional)

Period: 1 October 2025 to 30 September 2026. Currency: AED. Database file: `airport_ops.db` (SQLite). Same tables are in `airport_ops.xlsx` and in the `csv` folder.

## Read this first

- passenger_journeys is a 4 percent random sample. Counts must be multiplied by 25 to estimate the full population. Averages and percentages need no scaling.
- Waiting-time analysis by time of day should use immigration_hour (when the passenger was at immigration), not the scheduled flight hour.
- staffing_roster has no rows for a few hours on days when the roster system was down (see incidents with type 'Roster system outage').
- feedback can contain duplicate submissions. The view v_feedback_clean removes exact duplicates.
- daily_revenue shopping and dining figures are estimates built from the passenger sample (sample spend x 25).
- All airlines, outlets, people and policies are fictional. Currency is UAE dirham (AED).

## Tables and row counts

| Table | Rows | Purpose |
|---|---:|---|
| `meta` | 9 | Facts about the dataset itself: period covered, sampling rate, currency. Read this first. |
| `dim_date` | 365 | Calendar table, one row per day, with weekend, holiday and event flags. Join on date_key. |
| `dim_terminals` | 2 | The two terminals. T1 serves full-service airlines, T2 serves low-cost and regional airlines. |
| `dim_checkpoints` | 8 | Processing points in each terminal (check-in, security, immigration) with installed and standard counter numbers. |
| `dim_airlines` | 6 | The six airlines operating at the airport. All airline names are fictional. |
| `dim_routes` | 15 | The 15 routes served. Each route is a destination city, flown in both directions. |
| `dim_concessions` | 17 | Shops, restaurants and services that pay the airport rent. Names are fictional. |
| `flights` | 19,775 | One row per scheduled flight, arrivals and departures, 1 Oct 2025 to 30 Sep 2026. Full population, not a sample. |
| `passenger_journeys` | 108,488 | A 4 percent random sample of passengers with their measured waiting times and spend. Multiply counts by 25 to estimate the full population. |
| `staffing_roster` | 69,984 | Counters open per hour at every checkpoint, every day. Some hours are missing on days of a roster system outage (see incidents). |
| `feedback` | 13,116 | Passenger survey responses linked to a journey. One row per rated category. May contain duplicate submissions. |
| `complaints` | 1,428 | Formal complaints raised through the complaints process, with resolution time against the 10-day target. |
| `incidents` | 153 | Operational incidents and disruptions: system outages, equipment faults, weather, security alerts. |
| `daily_revenue` | 365 | Daily airport revenue by stream in AED. Shopping and dining figures are estimated from the passenger sample (sample spend x 25). |
| `concession_monthly_sales` | 204 | Monthly sales and rent per outlet. Outlet sales add up to the category totals in daily_revenue. |
| `airline_incentive_ledger` | 72 | Monthly landing-charge rebates paid to airlines under the standard incentive scheme. |

## Views (ready-made queries, read-only)

- `v_departure_immigration_hourly`: Departure immigration by date, hour and terminal: sampled journeys, average wait, share waiting more than 30 minutes, and counters open. Filter on journey_date, weekday or immigration_hour.
- `v_airline_month_delay`: Monthly delayed-flight percentage per airline (cancelled flights excluded from the denominator).
- `v_route_month_performance`: Monthly flights, passengers and average load factor per route and direction.
- `v_feedback_clean`: Feedback with exact duplicate submissions removed (same journey, category, score and comment).

## Relationships

- `flights.airline_code` -> `dim_airlines`; `flights.route_code` -> `dim_routes`; `flights.terminal_id` -> `dim_terminals`; `flights.flight_date` -> `dim_date`
- `passenger_journeys.flight_id` -> `flights`; `passenger_journeys.journey_date` -> `dim_date`
- `staffing_roster.checkpoint_id` -> `dim_checkpoints`; join to journeys on date, hour and checkpoint (`terminal_id || '-IMM-DEP'`)
- `feedback.journey_id` -> `passenger_journeys`; `complaints.journey_id` -> `passenger_journeys` (optional)
- `concession_monthly_sales.outlet_id` -> `dim_concessions`; `airline_incentive_ledger.airline_code` -> `dim_airlines`

## `meta`

Facts about the dataset itself: period covered, sampling rate, currency. Read this first.

| Column | Type | Description |
|---|---|---|
| `key` | TEXT | Name of the setting. |
| `value` | TEXT | Value of the setting. |
| `note` | TEXT | Plain-language explanation. |

## `dim_date`

Calendar table, one row per day, with weekend, holiday and event flags. Join on date_key.

| Column | Type | Description |
|---|---|---|
| `date_key` | TEXT | Date as YYYY-MM-DD. |
| `year` | INTEGER | Calendar year. |
| `quarter` | INTEGER | Calendar quarter 1-4. |
| `month` | INTEGER | Month number 1-12. |
| `month_name` | TEXT | Month name, for example January. |
| `year_month` | TEXT | YYYY-MM, convenient for monthly grouping. |
| `day_of_month` | INTEGER | Day of the month. |
| `weekday` | TEXT | Monday to Sunday. |
| `weekday_num` | INTEGER | 1 = Monday ... 7 = Sunday. |
| `iso_week` | INTEGER | ISO week number. |
| `is_weekend` | INTEGER | 1 for Saturday and Sunday (UAE working week), else 0. |
| `is_public_holiday` | INTEGER | 1 on a public holiday or holiday break day. |
| `is_school_holiday` | INTEGER | 1 during school holidays. |
| `event_name` | TEXT | Name of the holiday, break or event, if any. |

## `dim_terminals`

The two terminals. T1 serves full-service airlines, T2 serves low-cost and regional airlines.

| Column | Type | Description |
|---|---|---|
| `terminal_id` | TEXT | T1 or T2. |
| `terminal_name` | TEXT | Terminal name. |
| `terminal_type` | TEXT | Full-service or Low-cost and regional. |
| `opened_year` | INTEGER | Year the terminal opened. |

## `dim_checkpoints`

Processing points in each terminal (check-in, security, immigration) with installed and standard counter numbers.

| Column | Type | Description |
|---|---|---|
| `checkpoint_id` | TEXT | Terminal plus point, for example T1-IMM-DEP. |
| `terminal_id` | TEXT | Terminal the checkpoint belongs to. |
| `checkpoint_type` | TEXT | Check-in, Security, Immigration Departure or Immigration Arrival. |
| `counters_installed` | INTEGER | Physical counters, desks or lanes installed. |
| `standard_peak_counters` | INTEGER | Minimum counters that must be open in peak hours (17:00-22:59) per the staffing standard. |
| `standard_offpeak_counters` | INTEGER | Typical counters open outside peak hours per the staffing standard. |

## `dim_airlines`

The six airlines operating at the airport. All airline names are fictional.

| Column | Type | Description |
|---|---|---|
| `airline_code` | TEXT | Three-letter airline code. |
| `airline_name` | TEXT | Airline name. |
| `airline_type` | TEXT | Full-service, Low-cost or Regional. |
| `flight_prefix` | TEXT | Two-letter prefix used in flight numbers. |
| `terminal_id` | TEXT | Terminal the airline uses. |
| `contract_start_date` | TEXT | Date the airline agreement started. |
| `incentive_scheme_member` | INTEGER | 1 if the airline is in the standard landing-charge rebate scheme. |

## `dim_routes`

The 15 routes served. Each route is a destination city, flown in both directions.

| Column | Type | Description |
|---|---|---|
| `route_code` | TEXT | Three-letter code of the destination city. |
| `destination_city` | TEXT | Destination city. |
| `destination_country` | TEXT | Destination country. |
| `region` | TEXT | South Asia, Middle East and Africa, Europe, Southeast Asia or GCC. |
| `distance_km` | INTEGER | Approximate great-circle distance in km. |
| `typical_aircraft` | TEXT | Typical aircraft type on the route. |
| `seats` | INTEGER | Seats on the typical aircraft. |
| `planned_weekly_departures` | INTEGER | Planned departures per week for the whole route, all airlines together. |
| `launch_date` | TEXT | Date the route launched. |

## `dim_concessions`

Shops, restaurants and services that pay the airport rent. Names are fictional.

| Column | Type | Description |
|---|---|---|
| `outlet_id` | TEXT | Outlet identifier. |
| `outlet_name` | TEXT | Outlet name. |
| `category` | TEXT | Duty Free, Food & Beverage, Retail or Car Rental. |
| `terminal_id` | TEXT | Terminal where the outlet is. |
| `area_sqm` | INTEGER | Floor area in square metres. |
| `lease_type` | TEXT | Revenue share or Fixed rent. |
| `revenue_share_pct` | REAL | Share of sales paid to the airport as rent (0 for fixed-rent outlets). |

## `flights`

One row per scheduled flight, arrivals and departures, 1 Oct 2025 to 30 Sep 2026. Full population, not a sample.

| Column | Type | Description |
|---|---|---|
| `flight_id` | TEXT | Unique flight identifier, for example F000123. |
| `flight_number` | TEXT | Airline prefix plus number. |
| `flight_date` | TEXT | Scheduled date, YYYY-MM-DD. |
| `weekday` | TEXT | Weekday of the scheduled date. |
| `scheduled_time` | TEXT | Scheduled time HH:MM. |
| `scheduled_hour` | INTEGER | Hour of the scheduled time, 0-23. |
| `airline_code` | TEXT | Operating airline. |
| `route_code` | TEXT | Route (destination city). |
| `terminal_id` | TEXT | Terminal used. |
| `direction` | TEXT | Arrival or Departure. |
| `aircraft_type` | TEXT | Aircraft type flown. |
| `seats` | INTEGER | Seats on the aircraft. |
| `passengers` | INTEGER | Passengers carried (0 if cancelled). |
| `load_factor` | REAL | passengers / seats, 0 to 1. |
| `delay_min` | INTEGER | Minutes late (0 if on time or cancelled). |
| `delay_reason` | TEXT | Reason code text for delays over 15 minutes, otherwise empty. |
| `status` | TEXT | On time, Delayed (more than 15 minutes late) or Cancelled. |
| `landing_charge_aed` | REAL | Landing charge billed for arrivals in AED; empty for departures. |
| `gate` | TEXT | Gate used. |

## `passenger_journeys`

A 4 percent random sample of passengers with their measured waiting times and spend. Multiply counts by 25 to estimate the full population.

| Column | Type | Description |
|---|---|---|
| `journey_id` | TEXT | Unique journey identifier. |
| `flight_id` | TEXT | Flight the passenger took. |
| `journey_date` | TEXT | Date the passenger was processed at immigration (can differ from the flight date for early-morning flights). |
| `weekday` | TEXT | Weekday of journey_date. |
| `immigration_hour` | INTEGER | Hour of day (0-23) when the passenger was at immigration. Use this for time-of-day analysis and to join to staffing_roster. |
| `direction` | TEXT | Arrival or Departure. |
| `terminal_id` | TEXT | Terminal used. |
| `airline_code` | TEXT | Airline flown. |
| `route_code` | TEXT | Route flown. |
| `nationality` | TEXT | Passenger nationality. |
| `visa_type` | TEXT | Tourist, Visit, Residence, Work Permit or Transit. |
| `cabin_class` | TEXT | Economy or Business. |
| `age_band` | TEXT | 18-34, 35-54, 55+ or Under 18. |
| `check_in_wait_min` | REAL | Departures only: minutes waited at check-in. Empty for arrivals. |
| `security_wait_min` | REAL | Departures only: minutes waited at security. Empty for arrivals. |
| `immigration_wait_min` | REAL | Minutes waited at immigration (departure or arrival). |
| `baggage_wait_min` | REAL | Arrivals only: minutes waited for baggage. Empty for departures. |
| `total_processing_min` | REAL | Departures: check-in + security + immigration. Arrivals: immigration + baggage. |
| `used_smart_gate` | INTEGER | 1 if the passenger used an automated smart gate (Terminal 1 departures, from 1 July 2026). |
| `spend_aed` | REAL | Spend in shops, food and beverage in AED (0 if the passenger bought nothing). |
| `missed_flight` | INTEGER | 1 if the passenger missed the flight (departures only). |

## `staffing_roster`

Counters open per hour at every checkpoint, every day. Some hours are missing on days of a roster system outage (see incidents).

| Column | Type | Description |
|---|---|---|
| `roster_date` | TEXT | Date of the roster. |
| `hour` | INTEGER | Hour of day, 0-23. |
| `checkpoint_id` | TEXT | Checkpoint. |
| `counters_open` | INTEGER | Counters, desks or lanes open and staffed in that hour. |
| `staff_on_shift` | INTEGER | Staff on shift at the checkpoint in that hour. |
| `roster_template` | TEXT | Roster template used for the day: Standard, Weekend or Friday-B. |

## `feedback`

Passenger survey responses linked to a journey. One row per rated category. May contain duplicate submissions.

| Column | Type | Description |
|---|---|---|
| `feedback_id` | TEXT | Unique feedback identifier. |
| `journey_id` | TEXT | Journey the feedback refers to. |
| `feedback_date` | TEXT | Date of the journey. |
| `weekday` | TEXT | Weekday. |
| `hour` | INTEGER | Hour of the journey (same as immigration_hour). |
| `direction` | TEXT | Arrival or Departure. |
| `terminal_id` | TEXT | Terminal. |
| `channel` | TEXT | Survey channel: Kiosk, QR code, Mobile app or SMS. |
| `category` | TEXT | What the passenger rated: Waiting time, Staff, Cleanliness, Shops & dining, Wi-Fi, Signage, Security, Baggage or Parking & transport. |
| `score` | INTEGER | Score from 1 (very poor) to 5 (excellent). |
| `language` | TEXT | Language of the comment: en or ar. |
| `comment` | TEXT | Free-text comment in English or Arabic. |

## `complaints`

Formal complaints raised through the complaints process, with resolution time against the 10-day target.

| Column | Type | Description |
|---|---|---|
| `complaint_id` | TEXT | Unique complaint identifier. |
| `received_date` | TEXT | Date the complaint was received. |
| `received_hour` | INTEGER | Hour the complaint was received. |
| `journey_date` | TEXT | Date of the journey complained about, if known. |
| `journey_hour` | INTEGER | Hour of the journey complained about, if known. |
| `terminal_id` | TEXT | Terminal concerned. |
| `channel` | TEXT | App, Website, Call centre, Email, Social media or Walk-in. |
| `category` | TEXT | Immigration queue, Missed flight, Staff conduct, Baggage, Cleanliness, Facilities, Wi-Fi, Signage, Flight information or Other. |
| `severity` | TEXT | Low, Medium or High. |
| `journey_id` | TEXT | Linked journey when the complainant was in the survey sample, otherwise empty. |
| `status` | TEXT | Closed, Open or Escalated. |
| `days_to_resolve` | INTEGER | Days from receipt to closure; empty if not yet closed. |
| `sla_met` | INTEGER | 1 if closed within the 10-day target, 0 if closed late, empty if open. |
| `rebooking_help_offered` | INTEGER | 1 if the passenger was offered rebooking help (relevant after a missed flight). |

## `incidents`

Operational incidents and disruptions: system outages, equipment faults, weather, security alerts.

| Column | Type | Description |
|---|---|---|
| `incident_id` | TEXT | Unique incident identifier. |
| `start_date` | TEXT | Date the incident started. |
| `start_hour` | INTEGER | Hour the incident started. |
| `duration_min` | INTEGER | Duration in minutes. |
| `terminal_id` | TEXT | Terminal affected, or ALL. |
| `incident_type` | TEXT | Baggage system fault, Smart gate outage, Roster system outage, Power fluctuation, Weather disruption, Security alert, IT outage or HVAC failure. |
| `severity` | TEXT | Low, Medium or High. |
| `passengers_affected_est` | INTEGER | Estimated number of passengers affected. |
| `flights_affected` | INTEGER | Number of flights affected. |
| `root_cause` | TEXT | Short root-cause description. |

## `daily_revenue`

Daily airport revenue by stream in AED. Shopping and dining figures are estimated from the passenger sample (sample spend x 25).

| Column | Type | Description |
|---|---|---|
| `revenue_date` | TEXT | Date. |
| `passengers` | INTEGER | Total passengers that day (from flights). |
| `aeronautical_aed` | REAL | Landing, passenger and airline charges. |
| `duty_free_aed` | REAL | Duty-free sales (estimated). |
| `food_beverage_aed` | REAL | Food and beverage sales (estimated). |
| `other_retail_aed` | REAL | Other retail sales (estimated). |
| `parking_aed` | REAL | Parking revenue. |
| `car_rental_aed` | REAL | Car rental concession sales. |
| `advertising_aed` | REAL | Advertising revenue. |
| `total_revenue_aed` | REAL | Sum of all streams. |

## `concession_monthly_sales`

Monthly sales and rent per outlet. Outlet sales add up to the category totals in daily_revenue.

| Column | Type | Description |
|---|---|---|
| `year_month` | TEXT | Month, YYYY-MM. |
| `outlet_id` | TEXT | Outlet. |
| `sales_aed` | REAL | Sales in the month in AED. |
| `transactions` | INTEGER | Number of transactions. |
| `rent_paid_aed` | REAL | Rent paid to the airport (revenue share). |

## `airline_incentive_ledger`

Monthly landing-charge rebates paid to airlines under the standard incentive scheme.

| Column | Type | Description |
|---|---|---|
| `year_month` | TEXT | Month, YYYY-MM. |
| `airline_code` | TEXT | Airline. |
| `landing_charges_aed` | REAL | Total landing charges billed to the airline in the month. |
| `rebate_rate` | REAL | Rebate rate applied (0.05 = 5 percent). |
| `rebate_paid_aed` | REAL | Rebate actually paid in AED. |
| `status` | TEXT | Paid or Withheld. |
