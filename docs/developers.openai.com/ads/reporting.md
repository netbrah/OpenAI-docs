# Reporting

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Understand how your ads are performing, what they cost, and which outcomes they drive. Retrieve performance across your account, compare campaigns and products, or examine attributed conversions.

Examples use an ad account-scoped Advertiser API key, `${OPENAI_ADS_API_KEY}`, and sample IDs such as `cmpn_123`. Replace these with your key and resource IDs. Keep the API key on your server.

The sample reporting period is September 1–7, 2026, for an account in the `America/New_York` timezone. Use dates and the timezone appropriate to your account. See the [Insights API reference](https://developers.openai.com/ads/api-reference/insights) for complete request and response details.

## Insights API

Use Insights to retrieve delivery and performance metrics at the level you want to evaluate. The endpoint determines which entities the report covers. Aggregation determines what each row represents.

| To report on | Use                                        |
| ------------ | ------------------------------------------ |
| Your account | `GET /v1/ad_account/insights`              |
| One campaign | `GET /v1/campaigns/{campaign_id}/insights` |
| One ad group | `GET /v1/ad_groups/{ad_group_id}/insights` |
| One ad       | `GET /v1/ads/{ad_id}/insights`             |

### Retrieve daily campaign performance

This request returns impressions, clicks, spend, and CTR for each campaign, split by day:

```bash
curl -G "https://api.ads.openai.com/v1/ad_account/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'aggregation_level=campaign' \
  --data-urlencode 'time_granularity=daily' \
  --data-urlencode 'time_ranges[]={"type":"date_range","since":"2026-09-01","until":"2026-09-07","timezone":"America/New_York"}' \
  --data-urlencode 'fields[]=campaign_id' \
  --data-urlencode 'fields[]=campaign_name' \
  --data-urlencode 'fields[]=readable_time' \
  --data-urlencode 'fields[]=impressions' \
  --data-urlencode 'fields[]=clicks' \
  --data-urlencode 'fields[]=spend' \
  --data-urlencode 'fields[]=ctr'
```

Each row represents one campaign on one day. Spend is reported in the ad account's currency.

Use `time_granularity=none` when you want a total for the whole period instead of daily rows. The date-range example includes both September 1 and September 7.

To include campaigns, ad groups, or ads with no impressions, add `includes[]=zero_impression_items` to an unsegmented report.

Responses are paginated. Follow the [reference's pagination guidance](https://developers.openai.com/ads/api-reference/insights) when retrieving a complete report across many entities or dates.

You can include conversion metrics in these reports. For a dedicated attributed-conversion report, see [Conversion Reporting & Attribution](#conversion-reporting--attribution).

## Metrics & Definitions

Choose metrics that answer your reporting question: whether ads are delivering, how efficiently they generate engagement, or what outcomes they produce.

### Delivery and cost

| Metric                                | Meaning                                                |
| ------------------------------------- | ------------------------------------------------------ |
| Impressions (`impressions`)           | The number of ad impressions recorded.                 |
| Clicks (`clicks`)                     | The number of ad clicks recorded.                      |
| Spend (`spend`)                       | The amount spent, in the ad account's currency.        |
| Click-through rate (`ctr`)            | Clicks divided by impressions.                         |
| Cost per click (`cpc`)                | Average spend per click, using finalized activity.     |
| Cost per thousand impressions (`cpm`) | Spend per 1,000 impressions, using finalized activity. |

CTR is returned as a ratio: `0.04` means 4%. Spend, CPC, and CPM use major currency units, such as `12.50` for USD 12.50. These reporting values are not campaign-budget micros.

Recent delivery and cost metrics can reflect different processing stages. See [Data Freshness & Retention](#data-freshness--retention) before interpreting the newest results.

### Conversion and purchase outcomes

| Metric                                              | Meaning                                                                                                         |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Conversions (`conversions`)                         | Click-through conversions for the conversion events configured on your campaigns.                               |
| Cost per action (`cpa`)                             | Spend divided by conversions.                                                                                   |
| Post-click conversion rate (`post_click_cvr`)       | Conversions divided by clicks, returned as a ratio.                                                             |
| Attributed sales (`order_created_attributed_sales`) | The value of attributed purchase events (`order_created`), expressed in the ad account's currency.              |
| Return on ad spend (`order_created_roas`)           | Attributed purchase value divided by spend. A value of `4` means four units of attributed sales per unit spent. |

A `null` value means the metric is unavailable or cannot be calculated. It does not mean zero. For example, ROAS can be unavailable when purchase value is missing or spend is zero.

## Breakdowns & Filters

Segments show how performance varies within an entity. Filters narrow the report to the entities or results you want to evaluate.

For example, campaign aggregation gives you campaign rows. Adding a country segment splits each campaign's performance by country. Device and platform segments provide other views of delivery.

### Compare performance by country

This request segments one campaign's weekly performance by country:

```bash
curl -G "https://api.ads.openai.com/v1/campaigns/cmpn_123/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'aggregation_level=campaign' \
  --data-urlencode 'time_granularity=none' \
  --data-urlencode 'time_ranges[]={"type":"date_range","since":"2026-09-01","until":"2026-09-07","timezone":"America/New_York"}' \
  --data-urlencode 'segments[]=country' \
  --data-urlencode 'fields[]=campaign_id' \
  --data-urlencode 'fields[]=country.name' \
  --data-urlencode 'fields[]=country.impressions' \
  --data-urlencode 'fields[]=country.clicks' \
  --data-urlencode 'fields[]=country.spend' \
  --data-urlencode 'fields[]=country.ctr'
```

Each row shows that country's contribution to the campaign over the reporting period. Request segment metrics, such as `country.clicks`, when comparing segments.

Use one segment per request. To segment conversion results, use the examples in [Conversion Reporting & Attribution](#conversion-reporting--attribution).

### Focus on selected campaigns

To compare active and paused campaigns by total spend, filter their status and sort the results:

```bash
curl -G "https://api.ads.openai.com/v1/ad_account/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'aggregation_level=campaign' \
  --data-urlencode 'time_granularity=none' \
  --data-urlencode 'time_ranges[]={"type":"date_range","since":"2026-09-01","until":"2026-09-07","timezone":"America/New_York"}' \
  --data-urlencode 'fields[]=campaign_id' \
  --data-urlencode 'fields[]=campaign_name' \
  --data-urlencode 'fields[]=spend' \
  --data-urlencode 'fields[]=clicks' \
  --data-urlencode 'filters[]={"field":"campaign.status","operator":"IN","value":["active","paused"]}' \
  --data-urlencode 'sort[]={"field":"spend","direction":"desc"}'
```

Use entity filters to select the campaigns or ads you want to compare, and metric filters to focus on performance thresholds. The [Insights API reference](https://developers.openai.com/ads/api-reference/insights) lists supported filters and sorting options.

## Product & Conversion Reporting

### Product Reporting

Use product reporting to understand which items in your catalog receive ad delivery and engagement. Product-segmented Insights lets you compare individual items within a product-feed campaign.

#### Retrieve product performance

```bash
curl -G "https://api.ads.openai.com/v1/campaigns/cmpn_123/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'aggregation_level=campaign' \
  --data-urlencode 'time_granularity=none' \
  --data-urlencode 'time_ranges[]={"type":"date_range","since":"2026-09-01","until":"2026-09-07","timezone":"America/New_York"}' \
  --data-urlencode 'segments[]=product' \
  --data-urlencode 'fields[]=product.feed_id' \
  --data-urlencode 'fields[]=product.item_id' \
  --data-urlencode 'fields[]=product.title' \
  --data-urlencode 'fields[]=product.impressions' \
  --data-urlencode 'fields[]=product.clicks' \
  --data-urlencode 'fields[]=product.spend' \
  --data-urlencode 'fields[]=product.ctr'
```

Use the feed ID and item ID together to match each result to your catalog. Product titles help readers recognize items, but IDs provide the reliable link to the source data.

Compare impressions to understand delivery and clicks or CTR to understand engagement. Use daily reporting when you want to see how product performance changes over time. Product reports do not support hourly granularity.

#### Measure product-card engagement

For product-feed campaign ads with multiple product cards, you can also request `product.carousel_product_card_impressions` and `product.carousel_product_card_clicks`. These measure interactions with individual product cards. A card impression is not a billable ad impression, and card clicks are distinct from the ad click metric.

#### Include products with no delivery

When reviewing catalog coverage, you may also want products with no impressions. Request zero-impression product rows to include them. See the [zero-impression product example](https://developers.openai.com/ads/api-reference/insights) for the required grouping and request options.

For purchase value and ROAS, use [Conversion Reporting & Attribution](#conversion-reporting--attribution).

### Conversion Reporting & Attribution

Conversion reporting connects outcomes to eligible ad interactions. Before reporting, configure conversion events and attach them to your campaigns as described in Conversion Tracking. Reporting applies going forward from attachment.

Use general Insights when you want conversion outcomes alongside spend and delivery. Use `POST /v1/conversions/insights` for a focused conversion report, including click-through and view-through counts.

#### Retrieve daily conversions

Use campaign Insights to retrieve daily conversions alongside clicks and spend:

```bash
curl -G "https://api.ads.openai.com/v1/campaigns/cmpn_123/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'aggregation_level=campaign' \
  --data-urlencode 'time_granularity=daily' \
  --data-urlencode 'time_ranges[]={"type":"date_range","since":"2026-09-01","until":"2026-09-07","timezone":"America/New_York"}' \
  --data-urlencode 'fields[]=campaign_id' \
  --data-urlencode 'fields[]=readable_time' \
  --data-urlencode 'fields[]=clicks' \
  --data-urlencode 'fields[]=spend' \
  --data-urlencode 'fields[]=conversions'
```

Each row reports the campaign's results for one day. Use `time_granularity=none` for the period total.

#### View click-through and view-through conversions

Use the dedicated conversion endpoint to view click-through attribution (CTA) and view-through attribution (VTA) results for a campaign:

```bash
curl -X POST "https://api.ads.openai.com/v1/conversions/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "aggregation_level": "campaign",
    "time_granularity": "none",
    "time_ranges": [
      "{\"type\":\"unix_range\",\"start\":\"1788235200\",\"end\":\"1788840000\"}"
    ],
    "entity_ids": ["cmpn_123"]
  }'
```

This request returns totals for the same September 1–7 period, using Unix timestamps from midnight on September 1 to midnight on September 8 in the account's timezone.

To segment this report by country or device, add `"breakdown": "country"` or `"breakdown": "device"` to the request body.

#### Understand attribution

An attribution window is the period after an ad interaction during which an outcome can be credited to that interaction. Click-through attribution follows the applicable configured click window. The Conversion Tracking setup examples use 30 days.

| Reported field              | Meaning                                                                |
| --------------------------- | ---------------------------------------------------------------------- |
| `conversions`               | Click-through conversions.                                             |
| `click_through_conversions` | The same click-through count, explicitly labeled by attribution type.  |
| `view_through_conversions`  | Separately reported conversions attributed to eligible ad impressions. |

View-through attribution uses a one-day window after an eligible impression. If an outcome is eligible for both click-through and view-through attribution, the click takes precedence. View-through conversions are supplemental reporting. CPA, post-click conversion rate, and conversion optimization remain based on click-through conversions.

Daily conversion reporting uses the conversion date. An action that occurs after the ad interaction can therefore appear on a later reporting day.

#### Report purchase value and ROAS

Use general Insights to compare campaign spend with attributed purchase value:

```bash
curl -G "https://api.ads.openai.com/v1/ad_account/insights" \
  -H "Authorization: Bearer ${OPENAI_ADS_API_KEY}" \
  --data-urlencode 'aggregation_level=campaign' \
  --data-urlencode 'time_granularity=none' \
  --data-urlencode 'time_ranges[]={"type":"date_range","since":"2026-09-01","until":"2026-09-07","timezone":"America/New_York"}' \
  --data-urlencode 'fields[]=campaign_id' \
  --data-urlencode 'fields[]=campaign_name' \
  --data-urlencode 'fields[]=spend' \
  --data-urlencode 'fields[]=conversions' \
  --data-urlencode 'fields[]=order_created_attributed_sales' \
  --data-urlencode 'fields[]=order_created_attributed_sales_currency' \
  --data-urlencode 'fields[]=order_created_roas'
```

For example, USD 1,000 in attributed sales and USD 250 in spend produces a ROAS of `4`. These purchase metrics depend on the values supplied with `order_created` events.

## Data Freshness & Retention

Reporting metrics update at different speeds. Use recent delivery metrics to monitor activity, and allow processing time before drawing conclusions about cost or conversions.

### When metrics update

| Metrics                           | What to expect                                                                                                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Impressions, clicks, and CTR      | Can become available within minutes. Recent values may change as processing completes.                                                                             |
| Spend, CPC, and CPM               | Reflect finalized activity and can update later than impressions and clicks.                                                                                       |
| Conversions and purchase outcomes | Update through daily processing. Recent results can change as additional events are received and attributed. Allow at least one day for conversion data to appear. |

Because recent clicks can arrive before finalized spend, dividing the latest returned spend by the latest click count may produce a different value from the returned CPC. The same distinction applies to CPM and impressions. Use the returned cost metrics when evaluating performance.

Current-day and current-month reports can contain partial periods. Compare equivalent periods when evaluating changes, and refresh recent reporting dates to capture later updates.

### Historical availability

| Reporting type                                           | Available history         |
| -------------------------------------------------------- | ------------------------- |
| Hourly delivery reporting                                | Approximately 30 days.    |
| Non-hourly delivery reporting, excluding product reports | The most recent 365 days. |
| Product reporting                                        | Approximately 30 days.    |

Use daily or monthly reporting for longer-term trends within these retention limits. The dedicated conversion endpoint supports daily results or period totals. Daily requests can cover up to 365 days.